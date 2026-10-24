"""Generate the film's scene files from shared pieces (fonts, palette, sofa geometry).

Run: python3 build_scenes.py   (then: npx hyperframes@0.8.189 check)
Edit copy and timing in the SCENES below; the sofa and fonts are shared.
"""

from pathlib import Path

ROOT = Path(__file__).parent
FONTS = (ROOT / "assets/fonts/fonts.css").read_text()

BASE_CSS = FONTS + """
#root { position: absolute; inset: 0; overflow: hidden; font-family: 'Schibsted Grotesk', sans-serif; color: #17202b; }
.abs { position: absolute; }
.ground-linen { position: absolute; inset: 0; background: #eef1eb; }
.floor { position: absolute; left: 0; right: 0; top: 770px; bottom: 0; background: #e2e7de; }
.ground-grid { position: absolute; inset: 0; background-color: #fcfdfb;
  background-image: linear-gradient(rgba(14,90,78,.06) 2px, transparent 2px), linear-gradient(90deg, rgba(14,90,78,.06) 2px, transparent 2px);
  background-size: 32px 32px; }
.mark-band { background-image: linear-gradient(transparent 38%, rgba(246,214,74,.62) 38%, rgba(246,214,74,.62) 94%, transparent 94%);
  background-repeat: no-repeat; background-size: 0% 100%; padding: 0 4px; border-radius: 3px; }
.title { font-weight: 800; letter-spacing: -0.03em; line-height: 1.0; }
.w { display: inline-block; }
.quote { font-family: 'Newsreader', serif; font-style: italic; }
.mono { font-family: 'JetBrains Mono', monospace; }
.card { background: #fff; border-radius: 24px; box-shadow: 0 30px 60px -30px rgba(23,32,43,.35); }
.pill { position: absolute; background: #fff; border: 3px solid #0e5a4e; border-radius: 16px; padding: 10px 22px; font-size: 34px; font-weight: 500; white-space: nowrap; }
.pill .k { color: #566170; font-weight: 500; }
.pill.miss { border-color: #a9b2ab; border-style: dashed; color: #9a3b2e; }
"""

# Sofa geometry (viewBox 0 0 540 260)
BACK = (66, 22, 404, 112, 18)
BACK_CUSH = [(76, 34, 126, 92, 14), (210, 34, 126, 92, 14), (344, 34, 116, 92, 14)]
ARMS = [(20, 84, 58, 132, 22), (458, 84, 58, 132, 22)]
BASE = (44, 130, 448, 86, 14)
SEAT_CUSH = [(78, 134, 124, 42, 10), (210, 134, 124, 42, 10), (342, 134, 116, 42, 10)]
LEGS = [(68, 216, 14, 22, 3), (454, 216, 14, 22, 3)]


def r(x, y, w, h, rx, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {extra}/>'


def sofa_solid(id_):
    parts = [r(*BACK, 'fill="#3f6b62"')]
    parts += [r(*c, 'fill="#54857a"') for c in BACK_CUSH]
    parts += [r(*a, 'fill="#3f6b62"') for a in ARMS]
    parts += [r(*BASE, 'fill="#3f6b62"')]
    parts += [r(*c, 'fill="#54857a"') for c in SEAT_CUSH]
    parts += [r(*l, 'fill="#6b4a32"') for l in LEGS]
    return f'<svg id="{id_}" viewBox="0 0 540 260" class="abs" style="overflow:visible">{"".join(parts)}</svg>'


def sofa_lines(id_, cls, stroke, dash="", cushion_fill="none"):
    st = f'fill="none" stroke="{stroke}" stroke-width="3" vector-effect="non-scaling-stroke" {dash}'
    cst = f'fill="{cushion_fill}" stroke="{stroke}" stroke-width="3" vector-effect="non-scaling-stroke" {dash}'
    frame = r(*BACK, st) + "".join(r(*a, st) for a in ARMS) + r(*BASE, st) + "".join(r(*l, st) for l in LEGS)
    cush = "".join(r(*c, cst) for c in BACK_CUSH + SEAT_CUSH)
    return (f'<svg id="{id_}" viewBox="0 0 540 260" class="abs {cls}" style="overflow:visible">'
            f'<g id="{id_}-frame">{frame}</g><g id="{id_}-cush">{cush}</g></svg>')


GHOST = 'stroke-dasharray="14 12"'


def words(text, cls="w"):
    return " ".join(f'<span class="{cls}">{w}</span>' for w in text.split(" "))


def scene(cid, body, script, extra_css=""):
    return f"""<template>
  <style>
{BASE_CSS}
{extra_css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


SCENES = {}

# ---------------- 1. HOOK (6.6 s) ----------------
SCENES["hook"] = scene("hook", f"""
    <div class="ground-linen"></div><div class="floor"></div>
    <div id="hk-shadow" class="abs" style="left:190px;top:772px;width:960px;height:44px;border-radius:50%;background:rgba(23,32,43,.18);filter:blur(18px)"></div>
    {sofa_lines("hk-ghost", "", "#a9b2ab", GHOST)}
    {sofa_solid("hk-solid")}
    <div id="hk-scan" class="abs" style="left:0;top:250px;width:6px;height:600px;background:#0e5a4e;border-radius:3px;box-shadow:0 0 0 0 transparent"></div>
    <div id="hk-scanband" class="abs" style="left:0;top:250px;width:220px;height:600px;background:linear-gradient(90deg,transparent,rgba(14,90,78,.14))"></div>
    <div id="hk-q1" class="pill miss" style="left:560px;top:372px">Fabric ?</div>
    <div id="hk-q2" class="pill miss" style="left:980px;top:420px">Frame ?</div>
    <div id="hk-q3" class="pill miss" style="left:560px;top:836px">Width ?</div>
    <div id="hk-card" class="card abs" style="left:1260px;top:250px;width:520px;padding:36px 36px 30px;overflow:hidden">
      <p style="font-size:28px;color:#566170;font-weight:500">A shopper asks an AI</p>
      <p style="margin-top:12px;font-size:40px;font-weight:500;line-height:1.25">“Stain-resistant 3-seater under ₹60,000, good with a dog?”</p>
    </div>
    <div id="hk-ans" class="abs" style="left:1260px;top:560px;width:520px;background:#17202b;color:#fff;border-radius:24px;padding:28px 32px;box-shadow:0 30px 60px -30px rgba(23,32,43,.35)">
        <p style="font-size:28px;color:#b9c3cf;font-weight:500">AI answer</p>
        <p class="hk-row" style="margin-top:12px;font-size:32px;line-height:1.3">Brand B 3-seater</p>
        <p class="hk-row" style="margin-top:8px;font-size:32px;line-height:1.3">Brand C 3-seater</p>
        <p class="hk-row" style="margin-top:8px;font-size:32px;line-height:1.3">Brand D 3-seater</p>
    </div>
    <h1 id="hk-title" class="abs title" style="left:150px;top:110px;font-size:104px;width:1060px">{words("Arden isn’t in the answer.")}</h1>
""", """
    // sofa placement
    gsap.set(["#hk-solid", "#hk-ghost"], { left: 150, top: 300, width: 1040, height: 501 });
    // the ghost outline only exists once the AI looks
    tl.fromTo("#hk-ghost", { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "power2.out" }, 1.55);
    gsap.set("#hk-ans", { opacity: 0 });
    gsap.set(".hk-row", { opacity: 0, filter: "blur(6px)" });
    gsap.set("#hk-title .w", { opacity: 0, filter: "blur(6px)" });
    gsap.set(["#hk-q1", "#hk-q2", "#hk-q3"], { opacity: 0, scale: 0.9 });
    // question card arrives
    tl.fromTo("#hk-card", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 0.1);
    // the AI scan: solid sofa disappears exactly behind the line
    tl.fromTo(["#hk-scan", "#hk-scanband"], { x: 120, opacity: 0 }, { x: 1200, opacity: 1, duration: 1.0, ease: "power2.inOut" }, 1.6);
    tl.fromTo("#hk-scanband", { xPercent: -100 }, { xPercent: -100, duration: 1.0 }, 1.6);
    tl.fromTo("#hk-solid", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: 1.0, ease: "power2.inOut" }, 1.6);
    tl.to(["#hk-scan", "#hk-scanband"], { opacity: 0, duration: 0.2, ease: "power3.in" }, 2.6);
    tl.to("#hk-shadow", { opacity: 0.25, duration: 0.6, ease: "power2.inOut" }, 1.8);
    tl.fromTo(["#hk-q1", "#hk-q2", "#hk-q3"], { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", stagger: 0.1 }, 2.75);
    // card grows into the AI answer
    // the card grows downward into the AI answer (clip reveal, no layout tween)
    tl.fromTo("#hk-ans", { opacity: 1, clipPath: "inset(0% 0% 100% 0% round 24px)" }, { opacity: 1, clipPath: "inset(0% 0% 0% 0% round 24px)", duration: 0.6, ease: "expo.out" }, 3.3);
    tl.fromTo(".hk-row", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.09 }, 3.6);
    // the title lands, then holds still
    tl.fromTo("#hk-title .w", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.08 }, 4.5);
""")

# ---------------- 2. REVEAL (3.0 s) ----------------
SCENES["reveal"] = scene("reveal", f"""
    <div class="ground-linen"></div><div id="rv-floor" class="floor"></div>
    <div id="rv-grid" class="ground-grid"></div>
    {sofa_lines("rv-ghost", "", "#a9b2ab", GHOST)}
    <h1 id="rv-title" class="abs title" style="left:150px;top:300px;font-size:132px;width:820px">
      <span class="w">Make</span> <span class="w">it</span><br><span class="w"><span id="rv-legible" class="mark-band">legible.</span></span>
    </h1>
    <div id="rv-lock" class="abs" style="left:150px;top:690px;display:flex;align-items:center;gap:22px">
      <svg viewBox="0 0 32 32" style="width:72px;height:72px;fill:#0e5a4e"><rect x="3" y="20" width="26" height="4" rx="2"/><rect x="6" y="9" width="8" height="10" rx="2"/><rect x="16" y="5" width="10" height="14" rx="2"/></svg>
      <span style="font-size:60px;font-weight:700;letter-spacing:-0.02em">AgentShelf</span>
    </div>
""", """
    gsap.set("#rv-ghost", { left: 150, top: 300, width: 1040, height: 501 });
    gsap.set("#rv-title .w", { opacity: 0, color: "#c9cfc8" });
    // colour flood: the showroom becomes a drawing sheet, the ghost sofa stays and moves right
    tl.fromTo("#rv-grid", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut" }, 0.05);
    tl.fromTo("#rv-floor", { opacity: 1 }, { opacity: 0, duration: 0.5, ease: "power2.inOut" }, 0.05);
    tl.fromTo("#rv-ghost", { x: 0, y: 0, scale: 1, transformOrigin: "0% 0%" }, { x: 890, y: 30, scale: 0.731, duration: 0.7, ease: "power2.inOut" }, 0.1);
    // title: per word from light grey to ink
    tl.fromTo("#rv-title .w", { opacity: 0, color: "#c9cfc8" }, { opacity: 1, color: "#17202b", duration: 0.18, stagger: 0.09 }, 0.55);
    tl.fromTo("#rv-legible", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 1.15);
    tl.fromTo("#rv-lock", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 1.75);
""")

# ---------------- 3. PROOF (12.8 s) ----------------
JSON_LINES = [
    ('$ agentshelf audit example.com/products/arden-3-seater --category sofa', "cmd"),
    ("{", ""),
    ('  "name": "frame_or_core_material",', ""),
    ('  "status": "present",', ""),
    ('  "value": "solid sheesham wood",', ""),
    ('  "source_quote": "Frame: solid sheesham wood"', "q"),
    ("},", ""),
    ("{", ""),
    ('  "name": "fabric_or_comfort_layer",', ""),
    ('  "status": "present",', ""),
    ('  "value": "performance velvet",', ""),
    ('  "source_quote": "upholstered in stain-resistant performance velvet"', "q"),
    ("}", ""),
    ('{"dropped_unverified": "pet_or_kid_friendly_stated", "url": "…/arden-3-seater"}', "err"),
]
term_html = "".join(
    f'<div class="tl {cls}" style="white-space:pre;font-size:28px;line-height:38px;color:{"#9fe0cf" if cls=="cmd" else "#ff9b8a" if cls=="err" else "#f6d64a" if cls=="q" else "#d6dde5"}">{line}</div>'
    for line, cls in JSON_LINES
)
SHEET_ROWS = [
    ("Width", "213 cm", "W 213 cm × D 92 cm × H 84 cm"),
    ("Frame material", "solid sheesham wood", "Frame: solid sheesham wood"),
    ("Upholstery", "performance velvet", "upholstered in stain-resistant performance velvet"),
    ("Stain resistance", "stain-resistant, wipes clean", "stain-resistant performance velvet that wipes clean"),
    ("Warranty", "5 years on the frame", "Warranty: 5 years on the frame"),
]
sheet_html = "".join(
    f'<div class="srow" style="display:grid;grid-template-columns:270px 380px 720px 110px;gap:20px;align-items:center;padding:16px 0;border-top:2px solid #eef1eb;font-size:30px">'
    f'<span style="color:#566170">{a}</span><span style="font-weight:500">{b}</span><span class="quote" style="font-size:30px">“{c}”</span>'
    f'<span class="ok" style="font-weight:700;color:#0e5a4e;text-align:center">Y</span></div>'
    for a, b, c in SHEET_ROWS
)
FEED = [
    "<g:id>ARD-3S</g:id>",
    "<g:product_width>213 cm</g:product_width>",
    "<g:product_detail>",
    "  <g:attribute_name>Frame material</g:attribute_name>",
    "  <g:attribute_value>solid sheesham wood</g:attribute_value>",
    "</g:product_detail>",
    "<g:material>performance velvet</g:material>",
    "<g:product_detail>",
    "  <g:attribute_name>Warranty</g:attribute_name>",
    "  <g:attribute_value>5 years on the frame</g:attribute_value>",
    "</g:product_detail>",
]
feed_html = "".join(
    f'<div class="fl" style="white-space:pre;font-size:28px;line-height:40px;color:#d6dde5">{l.replace("<", "&lt;").replace(">", "&gt;")}</div>'
    for l in FEED
)
SCENES["proof"] = scene("proof", f"""
    <div class="ground-grid"></div>
    <!-- P1 terminal -->
    <div id="pf-term" class="abs" style="left:210px;top:120px;width:1500px;height:800px;background:#17202b;border-radius:24px;padding:48px 56px;overflow:hidden">
      <div id="pf-cmdwrap">{term_html}</div>
    </div>
    <!-- P2 page + drawing -->
    <div id="pf-page" class="card abs" style="left:120px;top:150px;width:760px;padding:44px 48px">
      <p style="font-size:44px;font-weight:700;letter-spacing:-0.01em">Arden 3-seater sofa</p>
      <p style="margin-top:22px;font-size:34px;line-height:1.45">Our bestselling 3-seater, upholstered in <span id="m-fab" class="mark-band">stain-resistant performance velvet</span> that wipes clean.</p>
      <p style="margin-top:18px;font-size:34px;line-height:1.45">Dimensions: <span id="m-wid" class="mark-band">W 213 cm × D 92 cm × H 84 cm</span></p>
      <p style="margin-top:18px;font-size:34px;line-height:1.45">Frame: <span id="m-frm" class="mark-band">solid sheesham wood</span>. Warranty: <span id="m-war" class="mark-band">5 years on the frame</span>.</p>
    </div>
    <div id="pf-claim" class="abs card" style="left:120px;top:780px;width:760px;padding:26px 36px;background:#fff">
      <p style="font-size:28px;color:#566170;font-weight:500">The model also claimed</p>
      <p class="quote" style="margin-top:6px;font-size:38px;color:#566170;text-decoration:line-through;text-decoration-color:#9a3b2e;text-decoration-thickness:3px">“Perfect for homes with pets”</p>
      <div id="pf-stamp" style="display:inline-block;margin-top:14px;border:4px solid #9a3b2e;color:#9a3b2e;border-radius:10px;padding:8px 16px;font-size:30px;font-weight:700;transform:rotate(-4deg);background:#fff">Not on the page. Dropped.</div>
    </div>
    <div id="pf-draw" class="abs" style="left:960px;top:0;width:960px;height:1080px">
      {sofa_lines("pf-ghost", "", "#a9b2ab", GHOST)}
      {sofa_lines("pf-ink", "", "#0e5a4e", "", "#e2efe9")}
      <svg id="pf-dim" class="abs" viewBox="0 0 800 60" style="left:40px;top:770px;width:800px;height:60px;overflow:visible">
        <path d="M30 30 H770 M30 12 V48 M770 12 V48" pathLength="1" fill="none" stroke="#0e5a4e" stroke-width="4" stroke-dasharray="1" stroke-dashoffset="1"/>
      </svg>
      <div id="pl-wid" class="pill" style="left:330px;top:832px">213 cm</div>
      <div id="pl-frm" class="pill" style="left:420px;top:262px"><span class="k">Frame</span> solid sheesham</div>
      <div id="pl-fab" class="pill" style="left:40px;top:180px"><span class="k">Upholstery</span> performance velvet</div>
      <svg id="pf-tag" class="abs" viewBox="0 0 220 170" style="left:690px;top:480px;width:220px;height:170px;overflow:visible">
        <path d="M30 0 C 50 30, 60 50, 70 60" fill="none" stroke="#566170" stroke-width="3"/>
        <path d="M58 60 h140 a10 10 0 0 1 10 10 v80 a10 10 0 0 1 -10 10 h-140 l-14 -50 z" fill="#fff" stroke="#0e5a4e" stroke-width="3"/>
        <circle cx="66" cy="110" r="6" fill="none" stroke="#0e5a4e" stroke-width="3"/>
        <text x="132" y="104" text-anchor="middle" font-family="Schibsted Grotesk" font-weight="700" font-size="30" fill="#17202b">5-yr</text>
        <text x="132" y="138" text-anchor="middle" font-family="Schibsted Grotesk" font-weight="500" font-size="28" fill="#566170">warranty</text>
      </svg>
    </div>
    <!-- P3 approval sheet -->
    <div id="pf-sheet" class="card abs" style="left:120px;top:160px;width:1680px;padding:40px 48px 30px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <p style="font-size:40px;font-weight:700">Approval sheet: Arden 3-seater sofa</p>
        <span id="pf-chip" style="background:#e2efe9;color:#0a453c;border-radius:14px;padding:10px 20px;font-size:30px;font-weight:500">Approved by your team</span>
      </div>
      <div style="display:grid;grid-template-columns:270px 380px 720px 110px;gap:20px;margin-top:26px;font-size:28px;color:#566170;font-weight:500"><span>Fact</span><span>Value</span><span>Source quote</span><span style="text-align:center">Approve</span></div>
      {sheet_html}
    </div>
    <!-- P4 feed -->
    <p id="pf-feedlabel" class="abs" style="left:880px;top:140px;font-size:38px;font-weight:700">Google Merchant Center feed</p>
    <div id="pf-feed" class="abs" style="left:880px;top:210px;width:920px;height:640px;background:#17202b;border-radius:24px;padding:40px 48px;overflow:hidden">{feed_html}</div>
""", """
    // ---- P1 terminal (0 - 2.8) ----
    gsap.set(["#pf-page", "#pf-claim", "#pf-draw", "#pf-sheet", "#pf-feed", "#pf-feedlabel"], { opacity: 0 });
    tl.fromTo("#pf-term", { opacity: 0, scale: 0.3, transformOrigin: "10% 80%" }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }, 0.00);
    tl.fromTo("#pf-cmdwrap .cmd", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "steps(40)" }, 0.40);
    tl.fromTo("#pf-cmdwrap .tl:not(.cmd)", { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: 0.08 }, 1.35);
    tl.to("#pf-term", { opacity: 0, scale: 0.55, x: -420, y: -40, duration: 0.35, ease: "power3.in" }, 3.55);
    // ---- P2 page + drawing (2.8 - 8.6) ----
    gsap.set(["#pf-ghost", "#pf-ink"], { left: 80, top: 330, width: 800, height: 385 });
    gsap.set("#pf-ink", { opacity: 1 });
    gsap.set(["#pf-ink-frame", "#pf-ink-cush", "#pl-wid", "#pl-frm", "#pl-fab", "#pf-tag", "#pf-stamp"], { opacity: 0 });
    tl.fromTo("#pf-page", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }, 3.75);
    tl.fromTo("#pf-draw", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.inOut" }, 3.80);
    // width
    tl.fromTo("#m-wid", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 4.20);
    tl.fromTo("#pf-dim path", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, 4.55);
    tl.fromTo("#pl-wid", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 4.90);
    // frame
    tl.fromTo("#m-frm", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.4, ease: "power2.inOut" }, 5.25);
    tl.fromTo("#pf-ink-frame", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.inOut" }, 5.55);
    tl.fromTo("#pf-ghost-frame", { opacity: 1 }, { opacity: 0, duration: 0.4, ease: "power2.inOut" }, 5.55);
    tl.fromTo("#pl-frm", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 5.80);
    // fabric
    tl.fromTo("#m-fab", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.5, ease: "power2.inOut" }, 6.20);
    tl.fromTo("#pf-ink-cush", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.inOut" }, 6.60);
    tl.fromTo("#pf-ghost-cush", { opacity: 1 }, { opacity: 0, duration: 0.4, ease: "power2.inOut" }, 6.60);
    tl.fromTo("#pl-fab", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 6.85);
    // warranty
    tl.fromTo("#m-war", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.4, ease: "power2.inOut" }, 7.20);
    tl.fromTo("#pf-tag", { opacity: 0, rotation: -24, transformOrigin: "30px 0px" }, { opacity: 1, rotation: 0, duration: 0.7, ease: "expo.out" }, 7.50);
    // the model's unsupported claim is dropped
    tl.fromTo("#pf-claim", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 7.65);
    tl.fromTo("#pf-stamp", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 7.95);
    tl.to(["#pf-page", "#pf-claim", "#pf-draw"], { opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 10.40);
    // ---- P3 approval sheet (8.6 - 10.8) ----
    gsap.set(".ok", { opacity: 0 }); gsap.set("#pf-chip", { opacity: 0 });
    tl.fromTo("#pf-sheet", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, 10.10);
    tl.fromTo(".ok", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out", stagger: 0.14 }, 10.70);
    tl.fromTo("#pf-chip", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 11.50);
    // ---- P4 feed (10.8 - 12.8): the sheet carries across, the feed arrives ----
    tl.to("#pf-sheet", { scale: 0.42, x: -560, y: 180, opacity: 0, duration: 0.6, ease: "power2.inOut", transformOrigin: "0% 0%" }, 12.70);
    tl.fromTo(["#pf-feedlabel", "#pf-feed"], { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.6, ease: "expo.out", stagger: 0.08 }, 12.90);
    tl.fromTo(".fl", { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: 0.06 }, 13.25);
""")

# ---------------- 4. PAYOFF (6.0 s) ----------------
SCENES["payoff"] = scene("payoff", f"""
    <div class="ground-linen"></div><div class="floor"></div>
    <div id="po-cam" class="abs" style="inset:0">
      <div class="abs" style="left:200px;top:774px;width:880px;height:40px;border-radius:50%;background:rgba(23,32,43,.18);filter:blur(18px)"></div>
      {sofa_solid("po-solid")}
      <svg class="abs" viewBox="0 0 800 60" style="left:150px;top:840px;width:960px;height:60px;overflow:visible">
        <path d="M20 30 H780 M20 12 V48 M780 12 V48" fill="none" stroke="#0e5a4e" stroke-width="4"/>
      </svg>
      <div class="pill po-l" style="left:520px;top:880px">213 cm</div>
      <div class="pill po-l" style="left:130px;top:190px"><span class="k">Upholstery</span> performance velvet</div>
      <div class="pill po-l" style="left:560px;top:250px"><span class="k">Frame</span> solid sheesham</div>
      <div class="pill po-l" style="left:900px;top:190px"><span class="k">Warranty</span> 5 years</div>
    </div>
    <div id="po-card" data-hold class="card abs" style="left:1240px;top:220px;width:560px;padding:36px">
      <p style="font-size:28px;color:#566170;font-weight:500">A shopper asks an AI</p>
      <p style="margin-top:10px;font-size:34px;font-weight:500;line-height:1.25">“Stain-resistant 3-seater under ₹60,000, good with a dog?”</p>
      <div style="margin-top:24px;background:#17202b;color:#fff;border-radius:16px;padding:26px">
        <p class="po-a" style="font-size:28px;color:#b9c3cf;font-weight:500">AI answer</p>
        <p class="po-a" style="margin-top:12px;font-size:34px;line-height:1.35"><b>Arden 3-seater sofa</b> fits: 213 cm wide, stain-resistant performance velvet that wipes clean, solid sheesham frame, 5-year warranty.</p>
        <p class="po-a" style="margin-top:16px;font-size:28px;color:#f6d64a">[1] product page  [2] Merchant Center feed</p>
      </div>
      <p id="po-rec" style="margin-top:22px;font-size:30px;color:#566170">[1] <span class="quote" style="font-size:32px;color:#17202b">“Frame: <span id="po-recm" class="mark-band">solid sheesham wood</span>”</span></p>
    </div>
""", """
    gsap.set("#po-solid", { left: 150, top: 330, width: 960, height: 462 });
    // whip in: arrives blurred horizontally, then the camera pulls back
    tl.fromTo("#po-cam", { x: 260, filter: "blur(20px)", opacity: 0.4 }, { x: 0, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);
    tl.fromTo("#po-cam", { scale: 1.1, transformOrigin: "35% 55%" }, { scale: 1, duration: 1.4, ease: "power2.inOut" }, 0.1);
    tl.fromTo(".po-l", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out", stagger: 0.12 }, 0.7);
    tl.fromTo("#po-card", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }, 1.3);
    tl.fromTo(".po-a", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.15, stagger: 0.12 }, 1.65);
    tl.fromTo("#po-rec", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 3.6);
    tl.fromTo("#po-recm", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 3.9);
""")

# ---------------- 5. END (5.6 s) ----------------
SCENES["end"] = scene("end", f"""
    <div class="ground-linen"></div>
    <h1 id="en-claim" class="abs title" style="left:150px;top:330px;font-size:132px;width:1500px">
      <span class="w">Every</span> <span class="w">fact,</span><br><span class="w">with</span> <span class="w">a</span> <span class="w"><span id="en-rec" class="mark-band">receipt.</span></span>
    </h1>
    <div id="en-card" class="abs" style="inset:0">
      <svg id="en-mark" class="abs" viewBox="0 0 32 32" style="left:810px;top:250px;width:300px;height:300px;fill:#0e5a4e;overflow:visible">
        <rect id="en-bar" x="3" y="20" width="26" height="4" rx="2"/>
        <rect id="en-b1" x="6" y="9" width="8" height="10" rx="2"/>
        <rect id="en-b2" x="16" y="5" width="10" height="14" rx="2"/>
      </svg>
      <p id="en-word" class="abs" style="left:0;right:0;top:560px;text-align:center;font-size:120px;font-weight:800;letter-spacing:-0.03em">AgentShelf</p>
      <div id="en-cta" class="abs" style="left:660px;top:740px;width:600px;height:96px;border-radius:18px;background:#0e5a4e;color:#fff;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:500">Get a free AI shelf snapshot</div>
    </div>
""", """
    gsap.set("#en-claim .w", { opacity: 0, filter: "blur(6px)" });
    gsap.set(["#en-bar", "#en-b1", "#en-b2", "#en-word", "#en-cta"], { opacity: 0 });
    tl.fromTo("#en-claim .w", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.08 }, 0.2);
    tl.fromTo("#en-rec", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 0.75);
    tl.to("#en-claim", { opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power3.in" }, 2.2);
    // the mark is performed: the shelf draws, two blocks land on it, the name wipes in
    tl.fromTo("#en-bar", { opacity: 1, scaleX: 0, transformOrigin: "0% 50%" }, { opacity: 1, scaleX: 1, duration: 0.4, ease: "expo.out" }, 2.5);
    tl.fromTo("#en-b1", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.3)" }, 2.75);
    tl.fromTo("#en-b2", { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.3)" }, 2.87);
    tl.fromTo("#en-word", { opacity: 1, clipPath: "inset(0 100% 0 0)" }, { opacity: 1, clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power2.inOut" }, 3.1);
    tl.fromTo("#en-cta", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 3.55);
""")

TIMING = [("hook", 0, 6.6), ("reveal", 6.6, 3.0), ("proof", 9.6, 16.2), ("payoff", 25.8, 7.0), ("end", 32.8, 5.6)]

# Voiceover: one Kokoro line per scene (assets/audio/narration.tsv). Volumes from normalize-audio (-16 LUFS).
VOICE = [  # id, start (s), duration (s), volume
    ("vo-hook", 0.25, 6.04, 1.0),
    ("vo-reveal", 6.85, 2.33, 1.0),
    ("vo-proof", 10.0, 14.02, 1.0),
    ("vo-payoff", 26.6, 4.14, 1.0),
    ("vo-end", 33.0, 4.59, 1.0),
]


def write():
    (ROOT / "compositions").mkdir(exist_ok=True)
    for name, html in SCENES.items():
        (ROOT / "compositions" / f"{name}.html").write_text(html, encoding="utf-8")

    audio = "\n".join(
        f'      <audio id="{i}" class="clip" src="assets/audio/{i}.wav" data-start="{st}" data-duration="{d}" data-volume="{v}" data-track-index="2"></audio>'
        for i, st, d, v in VOICE
    )

    hosts = "\n".join(
        f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" '
        f'data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
        for n, s, d in TIMING
    )
    total = TIMING[-1][1] + TIMING[-1][2]
    (ROOT / "index.html").write_text(f"""<!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=1920, height=1080" />
        <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
        <style>
          * {{ margin: 0; padding: 0; box-sizing: border-box; }}
          html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #eef1eb; }}
          #root {{ position: relative; width: 100%; height: 100%; }}
        </style>
      </head>
      <body>
        <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
    {hosts}
    {audio}
        </div>
        <script>
          window.__timelines = window.__timelines || {{}};
          window.__timelines["main"] = gsap.timeline({{ paused: true }});
        </script>
      </body>
    </html>
    """, encoding="utf-8")
    print("wrote", len(SCENES), "scenes; total", total, "s")


if __name__ == "__main__":
    write()
