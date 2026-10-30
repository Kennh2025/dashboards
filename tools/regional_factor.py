"""Regional sales factor for every mapped store in nitori_dashboard.html.

sales_i = area_i x density_format x F_i, then rescaled so each format group
keeps the total it has today (Nitori + EXPRESS + Deco Home share one density,
Shimachu its own). Only the split between stores changes.

F_i = (pop_i / mean)^w_pop x (furn_i / mean)^w_furn x (inc_i / mean)^w_inc
      x (comp_i / mean)^(-w_comp), clipped to [F_MIN, F_MAX].

Inputs (CSV, UTF-8), one per factor; a missing file means factor = 1 for all:
  data/catchment_pop.csv    osm_id,pop          residents within RADIUS_KM of the store
  data/pref_furniture.csv   pref,value          household furniture spending (en name as in the map)
  data/pref_income.csv      pref,value          per-capita prefectural income
  data/competition.csv      osm_id,count        rival stores within RADIUS_KM (IKEA, MUJI, Cainz, ...)

Usage: python3 tools/regional_factor.py [--write]
Without --write it prints a summary and writes tools/out/regional_factor.csv only.
"""
import csv, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTML = os.path.join(ROOT, 'nitori_dashboard.html')
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'out')

# Weights are a research decision (I DECIDE); change here.
W = {'pop': 0.4, 'furn': 0.2, 'inc': 0.2, 'comp': 0.2}
F_MIN, F_MAX = 0.5, 2.0
GROUP = {0: 'nitori', 1: 'nitori', 2: 'nitori', 3: 'shimachu'}  # format index -> density group
# store row: [lat, lon, fmt, pref, name, addr, area_m2, sales_m, has_outline, footprint, floors, osm_id, fte, staff, name_derived]
I_AREA, I_SALES, I_OSM, I_FMT, I_PREF = 6, 7, 11, 2, 3


def load_store_block():
    s = open(HTML, encoding='utf8').read()
    m = re.search(r'(id=["\']?ov-storedata["\']?[^>]*>)(.*?)(</script>)', s, re.S)
    return s, m


def read_csv(name, key, val):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf8') as f:
        return {r[key]: float(r[val]) for r in csv.DictReader(f)}


def rel(values):
    """Each value divided by the mean over stores that have it; missing -> 1."""
    xs = [v for v in values if v is not None]
    if not xs:
        return [1.0] * len(values)
    mu = sum(xs) / len(xs)
    return [v / mu if v is not None else 1.0 for v in values]


def main(write):
    s, m = load_store_block()
    D = json.loads(m.group(2))
    stores, prefs = D['s'], D['p']
    src = {
        'pop': read_csv('catchment_pop.csv', 'osm_id', 'pop'),
        'furn': read_csv('pref_furniture.csv', 'pref', 'value'),
        'inc': read_csv('pref_income.csv', 'pref', 'value'),
        'comp': read_csv('competition.csv', 'osm_id', 'count'),
    }
    raw = {
        'pop': [src['pop'].get(r[I_OSM]) if src['pop'] else None for r in stores],
        'furn': [src['furn'].get(prefs[r[I_PREF]]) if src['furn'] else None for r in stores],
        'inc': [src['inc'].get(prefs[r[I_PREF]]) if src['inc'] else None for r in stores],
        # +1 so a store with no rivals nearby does not divide by zero
        'comp': [src['comp'].get(r[I_OSM], 0) + 1 if src['comp'] else None for r in stores],
    }
    R = {k: rel(v) for k, v in raw.items()}
    F = []
    for i in range(len(stores)):
        f = (R['pop'][i] ** W['pop'] * R['furn'][i] ** W['furn'] * R['inc'][i] ** W['inc']
             * R['comp'][i] ** -W['comp'])
        F.append(min(F_MAX, max(F_MIN, f)))
    # rescale within each density group so the group total is unchanged
    new = [r[I_SALES] * F[i] for i, r in enumerate(stores)]
    for g in set(GROUP.values()):
        idx = [i for i, r in enumerate(stores) if GROUP[r[I_FMT]] == g]
        old_t, new_t = sum(stores[i][I_SALES] for i in idx), sum(new[i] for i in idx)
        k = old_t / new_t if new_t else 1
        for i in idx:
            new[i] *= k
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'regional_factor.csv'), 'w', newline='', encoding='utf8') as f:
        w = csv.writer(f)
        w.writerow(['osm_id', 'name', 'pref', 'format', 'area_m2', 'sales_old_m', 'pop', 'furn', 'inc', 'comp', 'factor', 'sales_new_m'])
        for i, r in enumerate(stores):
            w.writerow([r[I_OSM], r[4], prefs[r[I_PREF]], D['f'][r[I_FMT]], r[I_AREA], r[I_SALES],
                        raw['pop'][i], raw['furn'][i], raw['inc'][i], raw['comp'][i], round(F[i], 3), round(new[i])])
    used = [k for k, v in src.items() if v is not None]
    print(f'{len(stores)} stores · factors with data: {used or "none"}')
    print(f'factor range {min(F):.2f}–{max(F):.2f}')
    for g in sorted(set(GROUP.values())):
        idx = [i for i, r in enumerate(stores) if GROUP[r[I_FMT]] == g]
        print(f'{g}: total ¥{sum(stores[i][I_SALES] for i in idx):,}m → ¥{round(sum(new[i] for i in idx)):,}m')
    if write:
        for i, r in enumerate(stores):
            r[I_SALES] = round(new[i])
        js = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
        open(HTML, 'w', encoding='utf8').write(s[:m.start(2)] + js + s[m.end(2):])
        print('wrote', HTML)


if __name__ == '__main__':
    main('--write' in sys.argv)
