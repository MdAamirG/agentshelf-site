# SPEC: "Invisible until it's written" (AgentShelf launch film)

## GOAL
The viewer leaves thinking "if it isn't written on my page, the AI doesn't know my sofa exists, and AgentShelf fixes that with proof."

## OUTPUT
HyperFrames, 1920×1080, 30 fps. Silent master (no music source), with SFX slots documented for a later track.

## TIME
34.0 s × 30 = 1020 frames.

| Scene | Seconds | Frames |
|---|---|---|
| hook | 0–6.6 | 0–198 |
| reveal | 6.6–9.6 | 198–288 |
| proof | 9.6–22.4 | 288–672 |
| payoff | 22.4–28.4 | 672–852 |
| end | 28.4–34.0 | 852–1020 |

## LOOK
The medium is **a furniture showroom that turns into a technical drawing when the AI looks**.

**Showroom world**
- Wall `#EEF1EB` (linen) with a floor band `#E2E7DE` from y=770 down.
- Sofa in velvet green `#3F6B62`, cushions `#54857A`, walnut legs `#6B4A32`.
- Contact shadow: an ellipse in `rgba(23,32,43,0.18)` with 40 px blur.

**Drawing world**
- Ground `#FCFDFB` with a 32 px grid in `rgba(14,90,78,0.06)`.
- Line-work in evergreen `#0E5A4E` at 3 px; ghost lines `#A9B2AB` at 3 px, dashed 14/12.

**Accents**
- Ink `#17202B`. Slate `#566170` for quiet text. Missing `#9A3B2E`, only for "?" and "dropped".
- Marker yellow `rgba(246,214,74,0.62)`, **only** behind quoted evidence, as a band from 38% to 94% of line height.

**Type**
- Display: Schibsted Grotesk 800, 112–132 px, tracking −3%, line-height 1.0.
- Titles: 700, 72 px.
- Body: Schibsted Grotesk 500, 34–40 px.
- Quotes: Newsreader italic 400, 40 px.
- Code: JetBrains Mono 400, 28 px, only inside the terminal panel.

**Light and depth:** one soft shadow on cards (0 30 60 −30 `rgba(23,32,43,0.35)`). No grain, no vignette, no glow.

## OBJECTS
- **Sofa (front view):** back with 3 back cushions, 2 rolled arms, a base with 3 seat cushions, 2 walnut legs. It reads as a sofa without a label. It has 3 states:
  - solid (velvet)
  - ghost (dashed outline, no fill)
  - inked (evergreen line + mint cushion fill)
- **Product page card:** the white page the AI reads, with the real copy of the sample page.
- **Terminal panel:** the real `agentshelf audit` command and an excerpt of its real JSON and stderr (`assets/data/audit.json`, `audit.stderr.txt`).
- **Approval sheet:** real rows from `assets/data/approval.csv`, with `approve` = Y.
- **Feed panel:** real lines from `assets/data/supplemental_feed.xml`.
- **AI answer card:** ink card, white text, marker-yellow citations.
- **Swing tag:** a furniture shop tag hanging by a string from the right arm.
- **Mark:** the shelf (base bar) plus 2 blocks, as on the website.

## MOTION
**Eases**
- Arrivals: `expo.out`, 0.6–0.8 s.
- Camera and floods: `power2.inOut`, 0.5–1.2 s.
- Exits and zoom-through: `power3.in`, 0.3–0.4 s (40–50% shorter than entrances).
- Springs: only on the mark's blocks, `back.out(1.3)`.

**Titles:** per word, `blur(6px)` → 0 and opacity 0 → 1 over 0.13 s, 0.08 s apart, no translate. Once landed, a title is dead still.

**Overlap:** the next element starts when the previous one is 30–50% done. List items are staggered 0.08 s.

**Scan line:** one sweep, 1.0 s `power2.inOut`. The solid sofa is clipped away exactly behind it.

## SHOTS
| Frames | Shot | Hero move | The viewer reads | Hand-off to the next shot |
|---|---|---|---|---|
| 0–90 | Lit showroom | Solid sofa (54% of width) | "A shopper asks an AI" + the question, from 0.3 s | — |
| 48–80 | Scan | The scan line sweeps the sofa | — | Sofa becomes a ghost outline. 3 "?" chips pop at width, frame and fabric |
| 100–150 | Answer | Question card morphs taller into the AI answer card | 3 other brands' sofas | — |
| 138–198 | Title | — | "Arden isn't in the answer." held 1.5 s | — |
| 198–288 | Reveal | Colour flood (0.5 s): the showroom ground becomes the drawing sheet; the ghost sofa stays in place | "Make it legible." (marker under *legible*), then the lockup | Lockup morphs into the terminal |
| 288–372 | Terminal | Command types in, then real JSON streams line by line | The real dropped line in missing-red | Panel collapses into the page card |
| 372–540 | Page + drawing | Each verified quote highlights, then its sofa part inks: width (dimension line), frame, fabric, warranty tag | — | Then the model's claim "Perfect for homes with pets" is stamped "Not on the page. Dropped." |
| 540–612 | Approval sheet | The sheet rises; Y fills down the approve column | "Approved by your team" | — |
| 612–672 | Feed | Feed panel slides in | "Google Merchant Center feed" | Whip back to the showroom |
| 672–852 | Payoff | The inked and solid sofa with all labels, pulling back 1.10 → 1.0 | The AI answer card now recommends Arden, with [1][2] citations | Blur swap |
| 852–924 | Claim | — | "Every fact, with a receipt." | — |
| 924–1020 | End card | The mark builds: bar draws, 2 blocks drop, wordmark wipes in | CTA "Get a free AI shelf snapshot", held ≥ 2.5 s | — |

## BANNED
- **Grounds and light:** dark void grounds with floating elements; glow, neon, particles, purple or blue gradients, glass cards.
- **Generic paper look:** cream paper with a serif display; mono caps labels outside the terminal; corner labels and HUD brackets.
- **Layout and motion clichés:** everything centred; every element fading and sliding up; three cards in a row; titles that drift after landing; the logo docked in a corner.
- **Content:** any invented UI (every product screen uses the real engine output); real brand names for the competing sofas (they are "Brand B, C, D").

## QA
| Frame | Must show |
|---|---|
| 10 | Lit sofa + question card (thumbnail) |
| 75 | Scan line mid-sofa |
| 175 | Ghost sofa + answer card + title |
| 260 | "Make it legible." with marker |
| 330 | Terminal with the real dropped line |
| 470 | Frame and fabric inked, labels |
| 525 | "Dropped" stamp |
| 580 | Approval sheet with Y's |
| 650 | Feed lines |
| 780 | Payoff: full sofa + answer with citations |
| 900 | Claim |
| 1010 | End card + CTA |
