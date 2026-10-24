# Square LinkedIn cut: review (24 Oct 2026)

- **Format:** 1080×1080, 30 fps, 38.4 s, H.264 + AAC, 3.5 MB.
  - Output: `media/agentshelf-film-square.mp4`, with a copy on the Desktop.
- **Built from the same story, timing and voiceover as `../project`.** Every scene is recomposed for square: stacked instead of side by side, all reading text ≥ 28 px, and the band below y=880 kept clear for captions.
- **Burned-in captions:**
  - 23 groups of 2–5 words, one on screen at a time.
  - Groups never end on a small word.
  - The text is the exact script (AgentShelf, ChatGPT).
  - Timing is the measured speech spans from the render, with words spread by length and pauses at punctuation.
  - Whisper word times drifted up to 1.8 s, so they were not used directly.
- **Check:** `ok: true`. The remaining warnings are the fast-scrolling terminal and feed lines, which are deliberate (process shots).
- **Fixed after reviewing the decoded MP4:**
  - Two captions overlapped at 28.0 s. Each group now ends before the next begins.
  - The claim card overlapped the page text. The page now exits before the claim.
- **Rebuild:** `python3 build_square.py && npx hyperframes@0.8.189 render --quality delivery --output renders/agentshelf-film-square.mp4`
