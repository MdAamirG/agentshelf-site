# AgentShelf site: design system (MASTER)

## Brief

- **Audience:** founders and growth leads at high-ticket D2C sofa and mattress brands, plus the agencies that run their Shopify and Google. They're skeptical of "AI SEO" hype and have been burned by agencies before.
- **Primary job:** get them to request a free AI Shelf Snapshot.
- **What makes the page trustworthy:** showing the mechanism. That means every fact with its receipt (source quote + link), brand approval, and honest limits (no ranking promises).

## Concept: "Every fact has a receipt"

The most characteristic thing in this world is the **evidence trail**: a fact on a product page, a highlighter mark over the exact words, and a clean spec row it becomes. The page's one bold element is a **highlighter mark** (marker yellow) over source quotes. Everything else stays quiet: spec-sheet calm, generous whitespace, no card soup.

## Tokens

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#17202B` | Text, headings (true deep slate, not tinted near-black) |
| `--paper` | `#FFFFFF` | Base background |
| `--linen` | `#EEF1EB` | Alternate section background (sage-tinted linen, cool, not cream) |
| `--evergreen` | `#0E5A4E` | Primary, verified state, buttons (white text 7.6:1) |
| `--marker` | `#F6D64A` | Highlighter behind quoted evidence only, never for text |
| `--slate` | `#566170` | Secondary text (6.4:1 on white) |
| `--rule` | `#D5DBD2` | Hairlines, borders |
| `--missing` | `#9A3B2E` | "Not stated" status text only (sparingly) |

## Type

- **Schibsted Grotesk** (400/500/700) for everything UI: headings, body, buttons. Sturdy, editorial, not the default SaaS sans.
- **Newsreader italic** (400) **only for quoted source text**: evidence lifted from a brand's page. The change of voice *means* "this is a quote".
- Scale (rem): 0.875 / 1 / 1.125 / 1.375 / 1.75 / 2.5 / 3.5 (hero, clamp to 2.25 on mobile). Body 1.0625rem/1.6. Measure ≤ 68ch.

## Layout

- **Left-aligned** throughout. Max width 1160px, 12-column feel, 24px gutters (16px mobile).
- Hero: headline + sub + CTAs on the left. On the right, the **evidence panel**: a shopper's AI question, then the brand's product facts list flipping from "Not stated" to verified rows with highlighted quotes.
- Sections alternate paper and linen. Section rhythm is 112px desktop, 72px mobile.
- Corner radii by hierarchy: panels 14px, buttons 10px, chips 999px. No uniform card kit and no drop-shadow soup (one soft shadow on the hero panel only).

## Principles

1. **Show the receipt.** Quotes, sources and approval states over adjectives.
2. **Say the limits.** No ranking promises; India = Google AI Mode/Gemini only; no passwords needed.
3. **One moment of motion.** The hero panel's highlight sweep on load. Nothing else animates on scroll. Reduced motion shows the final state.
4. **Plain words, sentence case.**
   - No all-caps eyebrows, no "→" on buttons, no middle-dot meta strings, no emoji icons.
   - Numbered markers only for the real 4-step process.
5. **Quality floor:**
   - 4.5:1 contrast and visible focus rings
   - 44px tap targets
   - responsive at 375/768/1024/1440
   - no horizontal scroll, no trackers, no cookies

## Avoid (checked against the frontend-design calibration list)

- Cream + terracotta + serif display
- Near-black + acid accent
- Broadsheet hairline columns
- The SaaS-card kit with identical shadows
- Glassmorphism (UI-UX Pro Max suggested it; rejected as generic for this brief)
- Trust-blue + orange

---

# v2 (24 Oct 2026): the concept is "Legible"

**Idea:** people look at a sofa; AI shopping assistants *read* it. A product whose facts aren't written down is invisible to them. The visual language is the **furniture technical drawing**, because dimension lines, material callouts and a swing tag are exactly what a machine needs, and they come from the furniture world itself.

- **Headline:** "AI can't see your sofa. It reads it."
- **Hero:** a drawing sheet. On the left is the product page as text, which the AI reads, plus the AI's answer. On the right is a front-view line drawing of the sofa.
  - **Before:** dashed outline, "?" on every callout and dimension, swing tag blank.
  - **Then:** a reading beam sweeps the page and marker highlights land on 4 real sentences. Connector lines draw from each highlight to its callout. Values replace the "?" marks, the outline goes solid, and the AI answer card appears with citations.
  - **Timing and access:** under 5 s. Pause/Replay live in the sheet's title strip. Reduced motion shows the final state. A text alternative is provided.
- **New section, "What a shopper sees / What an AI reads":** a draggable comparison (`<input type=range>`, keyboard accessible) of the same product card. On one side, a styled listing with lifestyle copy. On the other, the plain text an AI extracts, where the facts trapped in images show as gaps.
- **Launch film:** made with HyperFrames from real engine artifacts (facts JSON, approval sheet, Merchant Center feed). It opens in a `<dialog>` with captions, and the section is hidden until the MP4 exists.
- **Texture:** a faint drawing-sheet grid (2–4% opacity) on the hero sheet only. Evergreen line-work at 1.5 px, with hairlines at 1 px.
