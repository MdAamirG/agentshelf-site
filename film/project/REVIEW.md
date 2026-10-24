# Review: AgentShelf film, 38.4 s (24 Oct 2026)

**Check:** `ok: true`.

**Warnings accepted, with reasons:**
- **`line_unread` on terminal and feed lines:** the process is meant to run fast. The one line that matters, the dropped claim, is restated on screen as the "Not on the page. Dropped." stamp, held 2 s.
- **`content_overlap` on the page card:** highlight bands on wrapped lines touch adjacent lines by design.

## Fixed after the first look at frames
- The question text was clipped by the card reveal. The AI answer is now its own card that unrolls below the question.
- The "Dropped" stamp covered "The model also claimed". It now sits under the struck-through quote.
- The warranty label sat on the sofa's cushion in the payoff. The labels now sit above the sofa.
- The mark's blocks were visible during the claim. They now start hidden.
- Lint: layout tweens (margin, left/top) were replaced with transforms and clip-path.
- Holds lengthened for the dropped stamp, the approval sheet and the payoff answer. A receipt beat was added to the payoff.

## Defaults this film avoided (from spec.md BANNED)
- Dark void ground, glow and gradients: none.
- Titles land and hold still.
- No three-card rows.
- The logo appears only on the end card, centred and performed (drawn in).

## Adding sound later
Put a music file at `assets/audio/bed.mp3` and add a timed audio element to the root:

```html
<audio id="bed" src="assets/audio/bed.mp3" data-start="0" data-duration="38.4" data-volume="0.8" data-fade-out="1.5">
```

Place effects as in `SPEC.md`:
- a soft marker-squeak on each highlight
- a quiet pop on each verified fact
- one riser into the payoff at 25.8 s

Then run `npx hyperframes@0.8.189 render --quality delivery`.

## Voiceover (added 24 Oct 2026)

- **Voice:** Kokoro `af_heart` at 0.95× speed, generated locally (`npx hyperframes tts`, venv at `film/.tts-venv`). Script in `assets/audio/narration.tsv`; one line per scene.
- **Loudness:** each line normalized with FFmpeg loudnorm to −16 LUFS, true peak −1.5 dB. All within 0.5–1 LU of each other.
- **Timing in the render (silencedetect):**

| Line | Plays |
|---|---|
| Hook | 0.25–6.21 s |
| Reveal | 6.89–9.03 s |
| Proof | 10.04–23.94 s |
| Payoff | 26.63–30.66 s |
| End | 33.05–37.51 s |

- **Sync:** "…gets dropped" lands just after the "Dropped" stamp, so the picture arrives first and the voice confirms it.
- **Captions:** `media/film.en.vtt`, 11 cues timed from the measured speech spans. The spoken lines never repeat the on-screen titles word for word.
- **Upgrade path:** a HeyGen voice, or a music bed under the voice (duck it about 10 dB while speaking).
