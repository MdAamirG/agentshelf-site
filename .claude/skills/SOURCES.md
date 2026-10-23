# Installed skills (pinned, audited 2026-10-24)

| Skill | Source | Commit |
|---|---|---|
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill (MIT) | d14efff |
| frontend-design | anthropics/skills | dbd4588 |
| web-design-guidelines | vercel-labs/agent-skills | 063bee9 |
| hyperframes, hyperframes-cli, hyperframes-registry | heygen-com/hyperframes (Apache-2.0) | 79b57ab |

## Audit notes

- **ui-ux-pro-max:** scripts are local CSV search only. No network calls.
- **hyperframes:** scripts shell out to the HyperFrames CLI (`npx hyperframes`). `bake-basemap.mjs` fetches map tiles; it isn't used here.
- **Rendering:** runs locally with headless Chrome and FFmpeg. Pin the CLI version when rendering.
- **Updating:** do it deliberately, by re-copying from a reviewed commit.
