"""Keep the GitHub Pages copy of the Nitori dashboard in step with the claude.ai artifact.

The claude.ai artifact "Nitori Research Dashboard" (https://claude.ai/artifact/JXCrwhHFW42M7BgK7YvQR8) is the
master copy. Claude reads it (Artifact tool, action "read"), which saves the published HTML to a local file; that
file carries an outer publish skeleton around the page. This script strips that skeleton, compares the page with
nitori_dashboard.html in this repository, and only when they differ writes it, commits and pushes to main.

  python3 -I sync_from_artifact.py <saved-artifact.html> --dry   # compare only, change nothing
  python3 -I sync_from_artifact.py <saved-artifact.html>         # write, commit and push if different
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
TARGET = REPO / "nitori_dashboard.html"
MARKERS = ("<title>Nitori Research Dashboard</title>", "const TABS=", "const BUILD=")


def strip_skeleton(html: str) -> str:
    """Return the page as authored: drop the publish skeleton's leading head/body and its closing tags."""
    second = html.find("<!doctype html>", 10)
    if html.lower().startswith("<!doctype html><html><head><meta charset=utf8>") and second != -1:
        html = html[second:]
        html = re.sub(r"\n*</body></html>\s*$", "", html, count=1)
    return html.rstrip("\n") + "\n"


def tab_names(html: str):
    m = re.search(r"const TABS=(\[.*?\]);", html, re.S)
    return [name for _, name in re.findall(r"\['(\w+)','([^']+)'\]", m.group(1))] if m else []


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact_file")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    page = strip_skeleton(Path(a.artifact_file).read_text(encoding="utf-8"))
    missing = [m for m in MARKERS if m not in page]
    if missing or len(page) < 100_000:
        sys.exit(f"REFUSED: this does not look like the Nitori dashboard (missing {missing}, {len(page):,} chars). Nothing changed.")

    if not a.dry:
        git("pull", "--ff-only", "-q")
    current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
    if page == current:
        print(f"IN SYNC: GitHub copy already matches the artifact ({h(page)}). Nothing to do.")
        return
    old_t, new_t = tab_names(current), tab_names(page)
    print(f"DIFFERENT: GitHub {h(current)} ({len(current.encode()):,} B) -> artifact {h(page)} ({len(page.encode()):,} B)")
    if old_t != new_t:
        print("  tabs added:", [t for t in new_t if t not in old_t], "removed:", [t for t in old_t if t not in new_t])
    if a.dry:
        print("DRY RUN: nothing written or pushed.")
        return
    TARGET.write_text(page, encoding="utf-8")
    git("add", TARGET.name)
    git("commit", "-q", "-m", "Nitori dashboard: sync from the claude.ai artifact\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    git("push", "-q", "origin", "main")
    print("PUSHED:", git("log", "--oneline", "-1"))


if __name__ == "__main__":
    main()
