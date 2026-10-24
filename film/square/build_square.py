"""Square (1080x1080) LinkedIn cut of the AgentShelf film, with burned-in captions.

Same story, timing and voiceover as ../project; every scene is recomposed for a square frame
(stacked, not side by side), all reading text >= 28 px, and the band below y=880 kept for captions.

Run: python3 build_square.py   (then: npx hyperframes@0.8.189 check)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "project"))
import build_scenes as b  # noqa: E402  shared fonts, sofa, real engine data, voice timing

W = H = 1080
scene, words, GHOST = b.scene, b.words, b.GHOST
sofa_solid, sofa_lines = b.sofa_solid, b.sofa_lines

EXTRA = """
.pill { font-size: 30px; padding: 8px 18px; border-radius: 14px; }
.wrap-pre { white-space: pre-wrap; word-break: break-word; }
"""

S = {}

# ---------------- 1. HOOK (6.6 s) ----------------
S["hook"] = scene("hook", f"""
    <div class="ground-linen"></div><div class="floor" style="top:660px"></div>
    <div id="hk-shadow" class="abs" style="left:200px;top:650px;width:680px;height:34px;border-radius:50%;background:rgba(23,32,43,.18);filter:blur(16px)"></div>
    {sofa_lines("hk-ghost", "", "#a9b2ab", GHOST)}
    {sofa_solid("hk-solid")}
    <div id="hk-scan" class="abs" style="left:0;top:270px;width:6px;height:420px;background:#0e5a4e;border-radius:3px"></div>
    <div id="hk-scanband" class="abs" style="left:0;top:270px;width:180px;height:420px;background:linear-gradient(90deg,transparent,rgba(14,90,78,.14))"></div>
    <div id="hk-q1" class="pill miss" style="left:250px;top:330px">Fabric ?</div>
    <div id="hk-q2" class="pill miss" style="left:770px;top:470px">Frame ?</div>
    <div id="hk-q3" class="pill miss" style="left:60px;top:590px">Width ?</div>
    <div id="hk-card" class="card abs" style="left:60px;top:50px;width:960px;padding:28px 36px">
      <p style="font-size:30px;color:#566170;font-weight:500">A shopper asks an AI</p>
      <p style="margin-top:8px;font-size:44px;font-weight:500;line-height:1.22">“Stain-resistant 3-seater under ₹60,000, good with a dog?”</p>
    </div>
    <div id="hk-ans" class="abs" style="left:60px;top:700px;width:960px;background:#17202b;color:#fff;border-radius:22px;padding:24px 28px">
      <p style="font-size:30px;color:#b9c3cf;font-weight:500">AI answer</p>
      <div style="display:flex;gap:14px;margin-top:12px">
        <span class="hk-row" style="font-size:32px;background:#2a3542;border-radius:12px;padding:8px 16px">Brand B 3-seater</span>
        <span class="hk-row" style="font-size:32px;background:#2a3542;border-radius:12px;padding:8px 16px">Brand C 3-seater</span>
        <span class="hk-row" style="font-size:32px;background:#2a3542;border-radius:12px;padding:8px 16px">Brand D 3-seater</span>
      </div>
    </div>
    <h1 id="hk-title" class="abs title" style="left:60px;top:70px;font-size:92px;width:960px">{words("Arden isn’t in the answer.")}</h1>
""", """
    gsap.set(["#hk-solid", "#hk-ghost"], { left: 160, top: 300, width: 760, height: 366 });
    tl.fromTo("#hk-ghost", { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "power2.out" }, 1.55);
    gsap.set(".hk-row", { opacity: 0, filter: "blur(6px)" });
    gsap.set("#hk-title .w", { opacity: 0, filter: "blur(6px)" });
    gsap.set(["#hk-q1", "#hk-q2", "#hk-q3"], { opacity: 0, scale: 0.9 });
    tl.fromTo("#hk-card", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 0.1);
    tl.fromTo(["#hk-scan", "#hk-scanband"], { x: 150, opacity: 0 }, { x: 930, opacity: 1, duration: 1.0, ease: "power2.inOut" }, 1.6);
    tl.fromTo("#hk-scanband", { xPercent: -100 }, { xPercent: -100, duration: 1.0 }, 1.6);
    tl.fromTo("#hk-solid", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: 1.0, ease: "power2.inOut" }, 1.6);
    tl.to(["#hk-scan", "#hk-scanband"], { opacity: 0, duration: 0.2, ease: "power3.in" }, 2.6);
    tl.to("#hk-shadow", { opacity: 0.25, duration: 0.6, ease: "power2.inOut" }, 1.8);
    tl.fromTo(["#hk-q1", "#hk-q2", "#hk-q3"], { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", stagger: 0.1 }, 2.75);
    tl.fromTo("#hk-ans", { opacity: 1, clipPath: "inset(0% 0% 100% 0% round 22px)" }, { opacity: 1, clipPath: "inset(0% 0% 0% 0% round 22px)", duration: 0.6, ease: "expo.out" }, 3.3);
    tl.fromTo(".hk-row", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.09 }, 3.6);
    // the question card makes way for the title
    tl.to("#hk-card", { opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 4.3);
    tl.fromTo("#hk-title .w", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.08 }, 4.55);
""", EXTRA)

# ---------------- 2. REVEAL (3.0 s) ----------------
S["reveal"] = scene("reveal", f"""
    <div class="ground-linen"></div><div id="rv-floor" class="floor" style="top:660px"></div>
    <div id="rv-grid" class="ground-grid"></div>
    {sofa_lines("rv-ghost", "", "#a9b2ab", GHOST)}
    <h1 id="rv-title" class="abs title" style="left:60px;top:80px;font-size:120px;width:960px">
      <span class="w">Make</span> <span class="w">it</span><br><span class="w"><span id="rv-legible" class="mark-band">legible.</span></span>
    </h1>
    <div id="rv-lock" class="abs" style="left:60px;top:790px;display:flex;align-items:center;gap:20px">
      <svg viewBox="0 0 32 32" style="width:68px;height:68px;fill:#0e5a4e"><rect x="3" y="20" width="26" height="4" rx="2"/><rect x="6" y="9" width="8" height="10" rx="2"/><rect x="16" y="5" width="10" height="14" rx="2"/></svg>
      <span style="font-size:56px;font-weight:700;letter-spacing:-0.02em">AgentShelf</span>
    </div>
""", """
    gsap.set("#rv-ghost", { left: 160, top: 300, width: 760, height: 366 });
    gsap.set("#rv-title .w", { opacity: 0, color: "#c9cfc8" });
    tl.fromTo("#rv-grid", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut" }, 0.05);
    tl.fromTo("#rv-floor", { opacity: 1 }, { opacity: 0, duration: 0.5, ease: "power2.inOut" }, 0.05);
    tl.fromTo("#rv-ghost", { x: 0, y: 0, scale: 1, transformOrigin: "0% 0%" }, { x: 60, y: 160, scale: 0.842, duration: 0.7, ease: "power2.inOut" }, 0.1);
    tl.fromTo("#rv-title .w", { opacity: 0, color: "#c9cfc8" }, { opacity: 1, color: "#17202b", duration: 0.18, stagger: 0.09 }, 0.55);
    tl.fromTo("#rv-legible", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 1.15);
    tl.fromTo("#rv-lock", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 1.75);
""", EXTRA)

# ---------------- 3. PROOF (16.2 s) ----------------
term = "".join(
    f'<div class="tl wrap-pre {cls}" style="font-size:28px;line-height:38px;color:{"#9fe0cf" if cls=="cmd" else "#ff9b8a" if cls=="err" else "#f6d64a" if cls=="q" else "#d6dde5"}">{line}</div>'
    for line, cls in b.JSON_LINES if '"status"' not in line
)
rows = "".join(
    f'<div class="srow" style="display:grid;grid-template-columns:230px 1fr 90px;gap:18px;align-items:center;padding:14px 0;border-top:2px solid #eef1eb">'
    f'<span style="color:#566170;font-size:30px">{a}</span>'
    f'<span><span style="display:block;font-size:30px;font-weight:500">{v}</span><span class="quote" style="display:block;font-size:28px;color:#566170">“{q}”</span></span>'
    f'<span class="ok" style="font-size:32px;font-weight:700;color:#0e5a4e;text-align:center">Y</span></div>'
    for a, v, q in b.SHEET_ROWS
)
feed = "".join(
    f'<div class="fl wrap-pre" style="font-size:28px;line-height:40px;color:#d6dde5">{l.replace("<", "&lt;").replace(">", "&gt;")}</div>'
    for l in b.FEED
)
S["proof"] = scene("proof", f"""
    <div class="ground-grid"></div>
    <div id="pf-term" class="abs mono" style="left:40px;top:40px;width:1000px;height:820px;background:#17202b;border-radius:22px;padding:36px 40px;overflow:hidden">
      <div id="pf-cmdwrap">{term}</div>
    </div>
    <div id="pf-page" class="card abs" style="left:60px;top:40px;width:960px;padding:30px 38px">
      <p style="font-size:40px;font-weight:700;letter-spacing:-0.01em">Arden 3-seater sofa</p>
      <p style="margin-top:14px;font-size:32px;line-height:1.4">Our bestselling 3-seater, upholstered in <span id="m-fab" class="mark-band">stain-resistant performance velvet</span> that wipes clean.</p>
      <p style="margin-top:12px;font-size:32px;line-height:1.4">Dimensions: <span id="m-wid" class="mark-band">W 213 cm × D 92 cm × H 84 cm</span></p>
      <p style="margin-top:12px;font-size:32px;line-height:1.4">Frame: <span id="m-frm" class="mark-band">solid sheesham wood</span>. Warranty: <span id="m-war" class="mark-band">5 years on the frame</span>.</p>
    </div>
    <div id="pf-claim" class="abs card" style="left:60px;top:60px;width:960px;padding:26px 36px">
      <p style="font-size:30px;color:#566170;font-weight:500">The model also claimed</p>
      <p class="quote" style="margin-top:6px;font-size:40px;color:#566170;text-decoration:line-through;text-decoration-color:#9a3b2e;text-decoration-thickness:3px">“Perfect for homes with pets”</p>
      <div id="pf-stamp" style="display:inline-block;margin-top:14px;border:4px solid #9a3b2e;color:#9a3b2e;border-radius:10px;padding:8px 16px;font-size:32px;font-weight:700;transform:rotate(-3deg);background:#fff">Not on the page. Dropped.</div>
    </div>
    <div id="pf-draw" class="abs" style="left:0;top:0;width:1080px;height:880px">
      {sofa_lines("pf-ghost", "", "#a9b2ab", GHOST)}
      {sofa_lines("pf-ink", "", "#0e5a4e", "", "#e2efe9")}
      <svg id="pf-dim" class="abs" viewBox="0 0 540 40" style="left:270px;top:778px;width:540px;height:40px;overflow:visible">
        <path d="M10 20 H530 M10 6 V34 M530 6 V34" pathLength="1" fill="none" stroke="#0e5a4e" stroke-width="4" stroke-dasharray="1" stroke-dashoffset="1"/>
      </svg>
      <div id="pl-wid" class="pill" style="left:470px;top:812px">213 cm</div>
      <div id="pl-fab" class="pill" style="left:60px;top:452px"><span class="k">Upholstery</span> performance velvet</div>
      <div id="pl-frm" class="pill" style="left:600px;top:452px"><span class="k">Frame</span> solid sheesham</div>
      <svg id="pf-tag" class="abs" viewBox="0 0 220 170" style="left:830px;top:600px;width:200px;height:155px;overflow:visible">
        <path d="M30 0 C 50 30, 60 50, 70 60" fill="none" stroke="#566170" stroke-width="3"/>
        <path d="M58 60 h140 a10 10 0 0 1 10 10 v80 a10 10 0 0 1 -10 10 h-140 l-14 -50 z" fill="#fff" stroke="#0e5a4e" stroke-width="3"/>
        <circle cx="66" cy="110" r="6" fill="none" stroke="#0e5a4e" stroke-width="3"/>
        <text x="132" y="104" text-anchor="middle" font-family="Schibsted Grotesk" font-weight="700" font-size="34" fill="#17202b">5-yr</text>
        <text x="132" y="138" text-anchor="middle" font-family="Schibsted Grotesk" font-weight="500" font-size="32" fill="#566170">warranty</text>
      </svg>
    </div>
    <div id="pf-sheet" class="card abs" style="left:40px;top:40px;width:1000px;padding:30px 36px 20px">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:16px">
        <p style="font-size:38px;font-weight:700">Approval sheet</p>
        <span id="pf-chip" style="background:#e2efe9;color:#0a453c;border-radius:14px;padding:8px 18px;font-size:30px;font-weight:500">Approved by your team</span>
      </div>
      <div style="display:grid;grid-template-columns:230px 1fr 90px;gap:18px;margin-top:18px;font-size:28px;color:#566170;font-weight:500"><span>Fact</span><span>Value and source quote</span><span style="text-align:center">OK</span></div>
      {rows}
    </div>
    <p id="pf-feedlabel" class="abs" style="left:60px;top:50px;font-size:38px;font-weight:700">Google Merchant Center feed</p>
    <div id="pf-feed" class="abs mono" style="left:40px;top:120px;width:1000px;height:740px;background:#17202b;border-radius:22px;padding:36px 40px;overflow:hidden">{feed}</div>
""", """
    gsap.set(["#pf-page", "#pf-claim", "#pf-draw", "#pf-sheet", "#pf-feed", "#pf-feedlabel"], { opacity: 0 });
    // P1 terminal
    tl.fromTo("#pf-term", { opacity: 0, scale: 0.3, transformOrigin: "10% 90%" }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }, 0);
    tl.fromTo("#pf-cmdwrap .cmd", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "steps(40)" }, 0.4);
    tl.fromTo("#pf-cmdwrap .tl:not(.cmd)", { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: 0.09 }, 1.35);
    tl.to("#pf-term", { opacity: 0, scale: 0.6, y: -60, duration: 0.35, ease: "power3.in" }, 3.55);
    // P2 page (top) + drawing (below)
    gsap.set(["#pf-ghost", "#pf-ink"], { left: 280, top: 520, width: 520, height: 250 });
    gsap.set(["#pf-ink-frame", "#pf-ink-cush", "#pl-wid", "#pl-frm", "#pl-fab", "#pf-tag", "#pf-stamp"], { opacity: 0 });
    tl.fromTo("#pf-page", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }, 3.75);
    tl.fromTo("#pf-draw", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.inOut" }, 3.8);
    tl.fromTo("#m-wid", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 4.2);
    tl.fromTo("#pf-dim path", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, 4.55);
    tl.fromTo("#pl-wid", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 4.9);
    tl.fromTo("#m-frm", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.4, ease: "power2.inOut" }, 5.25);
    tl.fromTo("#pf-ink-frame", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.inOut" }, 5.55);
    tl.fromTo("#pf-ghost-frame", { opacity: 1 }, { opacity: 0, duration: 0.4, ease: "power2.inOut" }, 5.55);
    tl.fromTo("#pl-frm", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 5.8);
    tl.fromTo("#m-fab", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.5, ease: "power2.inOut" }, 6.2);
    tl.fromTo("#pf-ink-cush", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.inOut" }, 6.6);
    tl.fromTo("#pf-ghost-cush", { opacity: 1 }, { opacity: 0, duration: 0.4, ease: "power2.inOut" }, 6.6);
    tl.fromTo("#pl-fab", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 6.85);
    tl.fromTo("#m-war", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.4, ease: "power2.inOut" }, 7.2);
    tl.fromTo("#pf-tag", { opacity: 0, rotation: -24, transformOrigin: "30px 0px" }, { opacity: 1, rotation: 0, duration: 0.7, ease: "expo.out" }, 7.5);
    // the page makes way for the unsupported claim
    tl.to("#pf-page", { opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 7.45);
    tl.fromTo("#pf-claim", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 7.65);
    tl.fromTo("#pf-stamp", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 7.95);
    tl.to(["#pf-claim", "#pf-draw"], { opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 10.0);
    // P3 approval sheet
    gsap.set(".ok", { opacity: 0 }); gsap.set("#pf-chip", { opacity: 0 });
    tl.fromTo("#pf-sheet", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, 10.1);
    tl.fromTo(".ok", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out", stagger: 0.14 }, 10.7);
    tl.fromTo("#pf-chip", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 11.5);
    // P4 feed: the sheet carries away, the feed arrives
    tl.to("#pf-sheet", { scale: 0.42, x: -300, y: 420, opacity: 0, duration: 0.6, ease: "power2.inOut", transformOrigin: "0% 0%" }, 12.7);
    tl.fromTo(["#pf-feedlabel", "#pf-feed"], { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out", stagger: 0.08 }, 12.9);
    tl.fromTo(".fl", { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: 0.06 }, 13.25);
""", EXTRA)

# ---------------- 4. PAYOFF (7.0 s) ----------------
S["payoff"] = scene("payoff", f"""
    <div class="ground-linen"></div><div class="floor" style="top:520px"></div>
    <div id="po-cam" class="abs" style="inset:0">
      <div class="abs" style="left:250px;top:500px;width:580px;height:30px;border-radius:50%;background:rgba(23,32,43,.18);filter:blur(14px)"></div>
      {sofa_solid("po-solid")}
      <svg class="abs" viewBox="0 0 620 40" style="left:230px;top:525px;width:620px;height:40px;overflow:visible">
        <path d="M6 20 H614 M6 6 V34 M614 6 V34" fill="none" stroke="#0e5a4e" stroke-width="4"/>
      </svg>
      <div class="pill po-l" style="left:470px;top:560px">213 cm</div>
      <div class="pill po-l" style="left:60px;top:50px"><span class="k">Upholstery</span> performance velvet</div>
      <div class="pill po-l" style="left:60px;top:118px"><span class="k">Frame</span> solid sheesham</div>
      <div class="pill po-l" style="left:500px;top:118px"><span class="k">Warranty</span> 5 years</div>
    </div>
    <div id="po-card" data-hold class="abs" style="left:60px;top:630px;width:960px;background:#17202b;color:#fff;border-radius:22px;padding:22px 30px;box-shadow:0 30px 60px -30px rgba(23,32,43,.35)">
      <p class="po-a" style="font-size:28px;color:#b9c3cf;font-weight:500">AI answer</p>
      <p class="po-a" style="margin-top:6px;font-size:30px;line-height:1.35"><b>Arden 3-seater sofa</b> fits: 213 cm wide, stain-resistant performance velvet that wipes clean, solid sheesham frame, 5-year warranty.</p>
      <p class="po-a" style="margin-top:8px;font-size:28px;color:#f6d64a">[1] product page  [2] Merchant Center feed</p>
    </div>
""", """
    gsap.set("#po-solid", { left: 230, top: 200, width: 620, height: 299 });
    tl.fromTo("#po-cam", { x: 200, filter: "blur(20px)", opacity: 0.4 }, { x: 0, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);
    tl.fromTo("#po-cam", { scale: 1.1, transformOrigin: "50% 45%" }, { scale: 1, duration: 1.4, ease: "power2.inOut" }, 0.1);
    tl.fromTo(".po-l", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out", stagger: 0.12 }, 0.7);
    tl.fromTo("#po-card", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 1.3);
    tl.fromTo(".po-a", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.15, stagger: 0.12 }, 1.55);
""", EXTRA)

# ---------------- 5. END (5.6 s) ----------------
S["end"] = scene("end", """
    <div class="ground-linen"></div>
    <h1 id="en-claim" class="abs title" style="left:60px;top:300px;font-size:120px;width:960px">
      <span class="w">Every</span> <span class="w">fact,</span><br><span class="w">with</span> <span class="w">a</span> <span class="w"><span id="en-rec" class="mark-band">receipt.</span></span>
    </h1>
    <svg id="en-mark" class="abs" viewBox="0 0 32 32" style="left:420px;top:200px;width:240px;height:240px;fill:#0e5a4e;overflow:visible">
      <rect id="en-bar" x="3" y="20" width="26" height="4" rx="2"/>
      <rect id="en-b1" x="6" y="9" width="8" height="10" rx="2"/>
      <rect id="en-b2" x="16" y="5" width="10" height="14" rx="2"/>
    </svg>
    <p id="en-word" class="abs" style="left:0;right:0;top:450px;text-align:center;font-size:116px;font-weight:800;letter-spacing:-0.03em">AgentShelf</p>
    <div id="en-cta" class="abs" style="left:200px;top:640px;width:680px;height:96px;border-radius:18px;background:#0e5a4e;color:#fff;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:500">Get a free AI shelf snapshot</div>
""", """
    gsap.set("#en-claim .w", { opacity: 0, filter: "blur(6px)" });
    gsap.set(["#en-bar", "#en-b1", "#en-b2", "#en-word", "#en-cta"], { opacity: 0 });
    tl.fromTo("#en-claim .w", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.08 }, 0.2);
    tl.fromTo("#en-rec", { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.45, ease: "power2.inOut" }, 0.75);
    tl.to("#en-claim", { opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power3.in" }, 2.2);
    tl.fromTo("#en-bar", { opacity: 1, scaleX: 0, transformOrigin: "0% 50%" }, { opacity: 1, scaleX: 1, duration: 0.4, ease: "expo.out" }, 2.5);
    tl.fromTo("#en-b1", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.3)" }, 2.75);
    tl.fromTo("#en-b2", { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.3)" }, 2.87);
    tl.fromTo("#en-word", { opacity: 1, clipPath: "inset(0 100% 0 0)" }, { opacity: 1, clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power2.inOut" }, 3.1);
    tl.fromTo("#en-cta", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 3.55);
""", EXTRA)

# ---------------- CAPTIONS (burned in) ----------------
# Measured speech spans in the render (ffmpeg silencedetect); words are spread inside each span
# by length, with pauses after commas and full stops. Exact script text, not the ASR spelling.
SPANS = {"vo-hook": (0.25, 6.21), "vo-reveal": (6.89, 9.03), "vo-proof": (10.04, 23.94),
         "vo-payoff": (26.63, 30.66), "vo-end": (33.05, 37.51)}
LINES = dict(l.split("\t", 1) for l in (ROOT / "assets/audio/narration.tsv").read_text().strip().splitlines())


WEAK = {"a", "an", "the", "on", "from", "in", "for", "with", "of", "to", "and", "your", "it", "we", "each", "every"}


def caption_groups():
    groups = []
    for vid, (a, z) in SPANS.items():
        toks = LINES[vid].split()
        weights = [len(t) + 1 + (4 if t.endswith((".", "?", "!")) else 2 if t.endswith(",") else 0) for t in toks]
        total = sum(weights)
        t, times = a, []
        for tok, wgt in zip(toks, weights):
            d = (z - a) * wgt / total
            times.append((tok, t, t + d * 0.8))  # the word itself; the rest of its share is the pause
            t += d
        cur = []
        for tok, s0, s1 in times:
            cur.append((tok, s0, s1))
            ends_clause = tok.endswith((".", ",", "?", "!"))
            if ends_clause and len(cur) >= 2 or len(cur) >= 5:
                # never end a group on a small word ("an", "the", "from"...): carry it into the next group
                carry = []
                while not ends_clause and len(cur) > 2 and cur[-1][0].lower() in WEAK:
                    carry.insert(0, cur.pop())
                groups.append(cur); cur = carry
        if cur:
            if groups and len(cur) == 1 and groups[-1][-1][2] > a:
                groups[-1].extend(cur)
            else:
                groups.append(cur)
    return [(" ".join(w for w, _, _ in g), g[0][1], g[-1][2]) for g in groups]


GROUPS = caption_groups()
cap_html = "\n".join(
    f'    <div id="cg{i}" class="cg"><span>{txt}</span></div>' for i, (txt, _, _) in enumerate(GROUPS)
)
def _cap_lines():
    out = []
    for i, (_, s0, e1) in enumerate(GROUPS):
        nxt = GROUPS[i + 1][1] if i + 1 < len(GROUPS) else 10_000
        kill = min(e1 + 0.15, nxt - 0.02)          # one group on screen at a time
        fade = max(s0 + 0.2, kill - 0.1)
        out.append(f'    tl.set("#cg{i}", {{ opacity: 1, visibility: "visible" }}, {s0:.2f});\n'
                   f'    tl.to("#cg{i}", {{ opacity: 0, duration: {kill - fade:.2f}, ease: "power2.in" }}, {fade:.2f});\n'
                   f'    tl.set("#cg{i}", {{ opacity: 0, visibility: "hidden" }}, {kill:.2f});')
    return "\n".join(out)


cap_script = _cap_lines()
S["captions"] = scene("captions", cap_html, '    gsap.set(".cg", { opacity: 0, visibility: "hidden" });\n' + cap_script, """
.cg { position: absolute; left: 0; right: 0; bottom: 64px; text-align: center; overflow: visible; }
.cg span { display: inline-block; max-width: 940px; background: rgba(23,32,43,.92); color: #fff; font-size: 44px; font-weight: 700;
  line-height: 1.2; letter-spacing: -0.01em; padding: 10px 22px; border-radius: 14px; }
""")

TIMING = b.TIMING
(ROOT / "compositions").mkdir(exist_ok=True)
for name, html in S.items():
    (ROOT / "compositions" / f"{name}.html").write_text(html.replace('data-width="1920" data-height="1080"', f'data-width="{W}" data-height="{H}"'), encoding="utf-8")
total = TIMING[-1][1] + TIMING[-1][2]
hosts = "\n".join(
    f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{s}" data-duration="{d}" '
    f'data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>' for n, s, d in TIMING
)
hosts += (f'\n      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
          f'data-duration="{total}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:10"></div>')
audio = "\n".join(
    f'      <audio id="{i}" class="clip" src="assets/audio/{i}.wav" data-start="{st}" data-duration="{d}" data-volume="{v}" data-track-index="2"></audio>'
    for i, st, d, v in b.VOICE
)
(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #eef1eb; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
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
print(f"square: {len(S)} compositions, {len(GROUPS)} caption groups, {total} s")
for txt, s0, e1 in GROUPS[:6]:
    print(f"  {s0:5.2f}-{e1:5.2f}  {txt}")
