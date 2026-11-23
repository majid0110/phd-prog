# PhD Outreach Dashboard

Static dashboard of PhD supervisor outreach: what to do this week, live leads, deadlines, and every reply so far.
Served by GitHub Pages: https://majid0110.github.io/phd-prog/

- `index.html` renders the page from `data.js`.
- A weekly scheduled Claude task reads Gmail (read-only), updates `data.js`, validates it with
  `scripts/validate_data.py`, and pushes. See `AGENTS.md` for the exact procedure.
- The site is public, so it only shows universities, countries and statuses: no professor names, emails or message text.
