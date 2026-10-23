# agentshelf-site

AgentShelf's landing page: static HTML/CSS/JS, no build step, no framework, no cookies, no trackers.

Design decisions: `design-system/agentshelf/MASTER.md`. Design skills (pinned, audited): `.claude/skills/SOURCES.md`.

## Before publishing (checklist)

- [ ] `config.js`: set `email` (outreach domain inbox), `calendar` (Cal.com/Calendly link) and `linkedin`. Empty values hide those links.
- [ ] Re-read every claim against `agentshelf-growth/docs/AGENTSHELF_BUSINESS_PLAN.md`:
  - pricing (₹25k audit, ₹15k/brand agency pilot)
  - "2 brands this month"
  - India = Google only
- [ ] The sample receipt uses a fictional brand ("Arden"). Keep it fictional. Never show a real brand without written permission.
- [ ] Add a founder photo if you want one (replace `.monogram`).

## Preview locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy (recommended: Cloudflare Pages, free)

1. In the Cloudflare dashboard, go to **Workers & Pages → Create → Pages → Connect to Git**.
2. Choose `agentshelf-site`. Leave the build command empty and set the output directory to `/`.
3. Add your custom domain (the same one as the outreach inbox).
4. Optional, after launch: add cookieless analytics (Umami Cloud), then update the footer line.

Netlify and Vercel work the same way (static, no build). GitHub Pages needs a public repo or a paid plan.
