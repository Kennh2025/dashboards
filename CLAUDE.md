# dashboards (GitHub Pages: https://kennh2025.github.io/dashboards/)

## Nitori dashboard: the claude.ai artifact is the master copy
- Master: claude.ai artifact "Nitori Research Dashboard", https://claude.ai/artifact/JXCrwhHFW42M7BgK7YvQR8
- Copy: `nitori_dashboard.html` in this repo, served at https://kennh2025.github.io/dashboards/nitori_dashboard.html
  (linked from the Fukuhara Seminar agent 19 page, including `#model` for Forecast & DCF).
- Artifact -> GitHub: read the artifact (Artifact tool, action "read"), then
  `python3 -I sync_from_artifact.py <saved file> --dry`, then without `--dry`. A scheduled task
  ("nitori-dashboard-sync") does this every day at 22:00.
- Change made here or elsewhere first: also republish the artifact (Artifact tool, publish with the URL above) from the
  same page, so the two never drift. The page is published as is (it carries its own doctype/head).
- Never edit `nitori_dashboard.html` on github.com directly: the next daily sync overwrites it from the artifact.
- `skylark_dashboard.html` is not synced.
