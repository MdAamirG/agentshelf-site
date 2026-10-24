/* AgentShelf motion layer.
   Runs only when GSAP + ScrollTrigger have loaded. Every start state is set here, never in CSS,
   so if the CDN is blocked or JS is off the page is exactly the static v2.1 page. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- Tap to trace: a fact's highlight flies back to the words it came from ---------- */
  const ping = (el) => { el.classList.remove("is-ping"); void el.offsetWidth; el.classList.add("is-ping"); };
  const traceBtn = $(".trace");
  const traceTarget = traceBtn && document.getElementById(traceBtn.dataset.traceTo);

  const gsap = window.gsap, ScrollTrigger = window.ScrollTrigger;
  if (!gsap || !ScrollTrigger) {
    // No motion library: the trace button still points at the quote, just without the flight.
    traceBtn && traceTarget && traceBtn.addEventListener("click", () => ping(traceTarget));
    return;
  }
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({ ignoreMobileResize: true });
  document.documentElement.classList.add("motion");

  /* ---------- One motion system for the whole page ---------- */
  const EASE = "power3.out";
  const T = { micro: 0.25, reveal: 0.6, beat: 1.2 };
  const STAGGER = 0.08;
  const NS = "http://www.w3.org/2000/svg";
  const reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

  function fly(from, to, { buzz = false } = {}) {
    if (!from || !to) return;
    const a = from.getBoundingClientRect(), b = to.getBoundingClientRect();
    const visible = b.bottom > 0 && b.top < innerHeight;
    if (reducedQuery.matches || !visible) { ping(to); return; }
    const mark = document.createElement("div");
    mark.className = "fly";
    document.body.appendChild(mark);
    gsap.set(mark, { x: a.left, y: a.top, width: a.width, height: a.height, opacity: 0.9 });
    gsap.to(mark, {
      x: b.left, y: b.top, width: b.width, height: b.height, duration: 0.7, ease: "power3.inOut",
      onComplete: () => { ping(to); gsap.to(mark, { opacity: 0, duration: T.micro, onComplete: () => mark.remove() }); },
    });
    if (buzz && navigator.vibrate) navigator.vibrate(8);
  }
  let traced = false;
  traceBtn && traceTarget && traceBtn.addEventListener("click", () => { traced = true; fly(traceBtn.querySelector("strong"), traceTarget, { buzz: true }); });

  // Hero: tap a callout (or a fact row on phones) and its highlight flies back to the product page text.
  const sheet = $("#sheet");
  if (sheet) {
    $$(".sofa .callout, .sofa .tag, .facts-mobile li", sheet).forEach((el) => {
      el.addEventListener("click", () => {
        const target = $(`mark[data-link="${el.dataset.anchor}"]`, sheet);
        fly(el.querySelector("rect, .tag-shape") || el, target, { buzz: true });
      });
    });
  }

  /* ---------- Depth: ink copies of the sofa outline, pushed back in Z ---------- */
  const layerCache = new Map();
  function layersFor(svg) {
    if (!svg) return [];
    if (layerCache.has(svg)) return layerCache.get(svg);
    const body = svg.querySelector(".body");
    const layers = [1, 2].map(() => {
      const layer = document.createElementNS(NS, "svg");
      layer.setAttribute("viewBox", svg.getAttribute("viewBox"));
      layer.setAttribute("class", "sofa-layer");
      layer.setAttribute("aria-hidden", "true");
      layer.appendChild(body.cloneNode(true));
      svg.parentElement.insertBefore(layer, svg);
      return layer;
    });
    const place = () => layers.forEach((l) => { l.style.top = `${svg.offsetTop}px`; });
    place();
    ScrollTrigger.addEventListener("refreshInit", place);
    layerCache.set(svg, layers);
    return layers;
  }

  /* ---------- Scenes ---------- */
  const feed = $(".feed");

  function heroScene(desk) {
    if (!sheet || !feed) return;
    const svg = desk ? $(".sofa-full", sheet) : $(".sofa-mini", sheet);
    const layers = layersFor(svg);
    const drawing = $(".drawing", sheet), left = $(".sheet-left", sheet), links = $(".links", sheet);
    const rows = $$(".feed-row", feed);
    feed.hidden = false;
    gsap.set(feed, { autoAlpha: 0, y: 18 });
    gsap.set(rows, { autoAlpha: 0, x: -10 });
    const tl = gsap.timeline({ defaults: { ease: "none" } });

    if (desk) {
      // Four acts, each driven by the scroll and narrated by the stage strip:
      // 1 Read the page    the card lifts toward you, a scan line passes, each fact is ringed as it is read.
      // 2 Quote the source the card settles; a line draws from each fact to its callout, which pops as it lands.
      // 3 Write the feed   the sheet comes apart in 3D, the sofa turns, the feed card is written row by row.
      // 4 AI answers       the feed wipes away, the answer comes forward, its two sources light up, all settles.
      const answer = $(".answer", sheet);
      const body = $(".page-body", sheet);
      const scan = $(".scan", sheet);
      const marks = $$("mark[data-link]", sheet);
      const callouts = $$(".sofa-full .callout, .sofa-full .tag", sheet);
      const cites = $$(".answer-cite a", sheet);
      const strip = $(".stage-strip", sheet);
      const steps = strip ? $$("li", strip) : [];
      const fit = () => { feed.style.height = `${answer.offsetHeight}px`; };
      fit();
      ScrollTrigger.addEventListener("refreshInit", fit);
      if (strip) { strip.hidden = false; strip.closest(".title-strip").classList.add("has-stages"); }
      links.classList.add("is-scrub"); // connector lines are drawn from CSS variables --d0..--d3 (1 = hidden, 0 = drawn)
      const ring = "0 0 0 2px rgba(14, 90, 78, 0.9)", noRing = "0 0 0 2px rgba(14, 90, 78, 0)";
      gsap.set(marks, { boxShadow: noRing });
      const lines = (v) => ({ "--d0": v, "--d1": v, "--d2": v, "--d3": v });

      // 1 Read the page
      tl.to(links, { opacity: 0, duration: 0.03 }, 0)
        .fromTo(links, lines(0), { ...lines(1), duration: 0.01, immediateRender: false }, 0.04)
        .to(left, { rotationY: 12, z: 50, duration: 0.07, ease: "power1.out" }, 0)
        .fromTo(scan, { y: 0, autoAlpha: 0 }, { y: () => body.offsetHeight - 2, autoAlpha: 1, duration: 0.16, immediateRender: false }, 0.04)
        .to(scan, { autoAlpha: 0, duration: 0.02 }, 0.2);
      marks.forEach((m) => {
        const f = Math.min(0.95, m.offsetTop / body.offsetHeight);
        tl.to(m, { boxShadow: ring, duration: 0.015 }, 0.04 + 0.16 * f);
      });

      // 2 Quote the source
      tl.to(left, { rotationY: 0, z: 0, duration: 0.04 }, 0.22)
        .to(links, { opacity: 1, duration: 0.02 }, 0.26);
      [0, 1, 2, 3].forEach((i) => {
        tl.fromTo(links, { [`--d${i}`]: 1 }, { [`--d${i}`]: 0, duration: 0.05, immediateRender: false }, 0.27 + i * 0.04);
        if (callouts[i]) tl.fromTo(callouts[i], { scale: 1 }, { scale: 1.1, duration: 0.015, yoyo: true, repeat: 1, transformOrigin: "50% 50%", immediateRender: false }, 0.315 + i * 0.04);
      });
      tl.to(marks, { boxShadow: noRing, duration: 0.03 }, 0.42);

      // 3 Write the feed
      tl.to(links, { opacity: 0, duration: 0.03 }, 0.45)
        .to(left, { z: 70, rotationY: 10, duration: 0.11 }, 0.46)
        .to(drawing, { rotationY: -38, rotationX: 12, z: -40, scale: 0.96, duration: 0.11 }, 0.46)
        .to(layers[0], { opacity: 0.65, z: -30, duration: 0.11 }, 0.46)
        .to(layers[1], { opacity: 0.35, z: -60, duration: 0.11 }, 0.46)
        .fromTo(feed, { autoAlpha: 1, y: 0, clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.05, immediateRender: false }, 0.55)
        .to(rows, { autoAlpha: 1, x: 0, stagger: 0.03, duration: 0.035 }, 0.58);

      // 4 AI answers, with a source
      tl.to(feed, { clipPath: "inset(0% 0% 0% 100%)", duration: 0.05 }, 0.73)
        .to(answer, { z: 60, scale: 1.04, duration: 0.05 }, 0.76)
        .call(() => cites[0] && ping(cites[0]), null, 0.81)
        .call(() => cites[1] && ping(cites[1]), null, 0.85)
        .to(answer, { z: 0, scale: 1, duration: 0.07 }, 0.9)
        .to(left, { z: 0, rotationY: 0, duration: 0.09 }, 0.88)
        .to(drawing, { rotationY: 0, rotationX: 0, z: 0, scale: 1, duration: 0.09 }, 0.88)
        .to(layers, { opacity: 0, z: 0, duration: 0.09 }, 0.88)
        .to(links, { opacity: 1, duration: 0.02 }, 0.97);

      const stageAt = [0, 0.22, 0.45, 0.72];
      const setStage = (p) => steps.forEach((li, i) => {
        const next = stageAt[i + 1] ?? 2;
        li.classList.toggle("is-on", p >= stageAt[i] && p < next);
        li.classList.toggle("is-done", p >= next);
      });
      setStage(0);
      ScrollTrigger.create({
        trigger: sheet, start: "center 54%", end: () => `+=${Math.round(innerHeight * 2.2)}`,
        pin: true, scrub: 0.6, anticipatePin: 1, invalidateOnRefresh: true, animation: tl,
        onUpdate: (self) => setStage(self.progress),
      });
    } else {
      // Phones: no pinning. The drawing turns as it passes under the thumb, and the feed stays once written.
      const sofa = [svg, ...layers];
      tl.to(sofa, { rotationY: -24, rotationX: 8, duration: 0.5 }, 0)
        .to(layers[0], { opacity: 0.5, z: -14, duration: 0.5 }, 0)
        .to(layers[1], { opacity: 0.25, z: -28, duration: 0.5 }, 0)
        .to(sofa, { rotationY: 0, rotationX: 0, duration: 0.5 }, 0.5)
        .to(layers, { opacity: 0, z: 0, duration: 0.5 }, 0.5);
      ScrollTrigger.create({ trigger: svg, start: "top 80%", end: "bottom 20%", scrub: 0.4, animation: tl });
      ScrollTrigger.create({
        trigger: feed, start: "top 88%", once: true,
        onEnter: () => gsap.timeline()
          .to(feed, { autoAlpha: 1, y: 0, duration: T.reveal, ease: EASE })
          .to(rows, { autoAlpha: 1, x: 0, stagger: STAGGER, duration: T.micro * 1.6, ease: EASE }, "-=0.3"),
      });
    }
  }

  function gapScene() {
    const facts = $$(".ai-facts > div");
    const thread = $(".ai-facts .thread");
    if (!facts.length) return;
    gsap.set(facts, { autoAlpha: 0, x: 12 });
    ScrollTrigger.create({
      trigger: ".compare", start: "top 70%", once: true,
      onEnter: () => {
        const tl = gsap.timeline();
        tl.to(facts, { autoAlpha: 1, x: 0, stagger: STAGGER * 1.5, duration: T.reveal, ease: EASE });
        if (thread) {
          tl.fromTo(thread, { backgroundColor: "rgba(246, 214, 74, 0)" }, { backgroundColor: "rgba(246, 214, 74, 0.55)", duration: T.micro, yoyo: true, repeat: 3, ease: "power1.inOut" }, "-=0.1")
            .to(thread, { backgroundColor: "rgba(246, 214, 74, 0.3)", duration: T.micro });
        }
      },
    });
  }

  function receiptScene() {
    const receipt = $(".receipt");
    if (!receipt) return;
    const parts = [$(".receipt-top", receipt), ...$$("dl > div", receipt), $(".receipt-note", receipt)].filter(Boolean);
    gsap.set(receipt, { transformPerspective: 900, rotationX: 24, y: -28, autoAlpha: 0 });
    gsap.set(parts, { autoAlpha: 0, y: -10 });
    const tl = gsap.timeline({ paused: true })
      .to(receipt, { rotationX: 0, y: 0, autoAlpha: 1, duration: T.beat * 0.7, ease: EASE })
      // Printed line by line, like a till receipt.
      .to(parts, { autoAlpha: 1, y: 0, stagger: 0.14, duration: T.micro * 1.4, ease: "power2.out" }, "-=0.45")
      .add(() => { if (!traced) fly(traceBtn && traceBtn.querySelector("strong"), traceTarget); }, "+=0.35");
    ScrollTrigger.create({ trigger: receipt, start: "top 75%", once: true, onEnter: () => tl.play() });
  }

  function approvalScene() {
    const rows = $$(".approval tbody tr");
    const count = $(".js-approved");
    if (!rows.length) return;
    const paths = rows.map((r) => r.querySelector(".tick path"));
    paths.forEach((p) => { const len = Math.ceil(p.getTotalLength()); gsap.set(p, { strokeDasharray: len, strokeDashoffset: len }); });
    rows.forEach((r) => r.classList.add("is-pending"));
    if (count) count.textContent = "0";
    const tl = gsap.timeline({ paused: true });
    rows.forEach((r, i) => {
      tl.to(paths[i], {
        strokeDashoffset: 0, duration: T.micro * 1.4, ease: "power2.out",
        onStart: () => r.classList.remove("is-pending"),
        onComplete: () => { if (count) count.textContent = String(i + 1); },
      }, i * 0.34);
    });
    ScrollTrigger.create({ trigger: ".approval", start: "top 70%", once: true, onEnter: () => tl.play() });
  }

  function reveals() {
    const els = $$([
      ".section-head > *", ".how h2", ".steps li", ".safe-list li", ".tier", ".agencies",
      ".faq-grid h2", ".faq-list details", ".film-copy > *", ".start-copy > *", ".founder", ".view-toggle",
    ].join(","));
    gsap.set(els, { autoAlpha: 0, y: 12 });
    ScrollTrigger.batch(els, {
      start: "top 88%", once: true,
      onEnter: (batch) => gsap.to(batch, { autoAlpha: 1, y: 0, duration: T.reveal, ease: EASE, stagger: STAGGER, overwrite: true }),
    });
    // Safety net: nothing that is on screen may stay hidden.
    window.addEventListener("load", () => setTimeout(() => els.forEach((el) => {
      if (getComputedStyle(el).visibility === "hidden" && el.getBoundingClientRect().top < innerHeight) gsap.to(el, { autoAlpha: 1, y: 0, duration: T.micro });
    }), 2500));
  }

  function sweep() {
    const el = $(".sweep");
    if (!el) return;
    gsap.set(el, { backgroundSize: "0% 100%" });
    ScrollTrigger.create({ trigger: el, start: "top 80%", once: true, onEnter: () => gsap.to(el, { backgroundSize: "100% 100%", duration: T.reveal, ease: EASE, delay: 0.3 }) });
  }


  // X-ray lens: on desktop, the shopper's page under a circle that shows what the AI reads beneath the cursor.
  function lensScene() {
    const compare = $(".compare");
    if (!compare || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return () => {};
    let lens = $(".pane-lens", compare), ring = $(".lens-ring", compare);
    if (!lens) {
      lens = $(".pane-ai", compare).cloneNode(true);
      lens.classList.add("pane-lens");
      const label = $(".pane-label", lens);
      if (label) label.remove();
      // The AI facts may be mid-entrance (hidden inline) when cloned; the lens always shows the finished view.
      $$("[style]", lens).forEach((el) => el.removeAttribute("style"));
      ring = document.createElement("span");
      ring.className = "lens-ring";
      ring.setAttribute("aria-hidden", "true");
      compare.append(lens, ring);
    }
    const pos = { x: 0, y: 0 }, radius = { r: 0 };
    const apply = () => { compare.style.setProperty("--lx", `${pos.x}px`); compare.style.setProperty("--ly", `${pos.y}px`); gsap.set(ring, { x: pos.x, y: pos.y }); };
    const setR = () => compare.style.setProperty("--lr", `${radius.r}px`);
    const toX = gsap.quickTo(pos, "x", { duration: 0.22, ease: "power3", onUpdate: apply });
    const toY = gsap.quickTo(pos, "y", { duration: 0.22, ease: "power3", onUpdate: apply });
    const local = (e) => { const r = compare.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
    const onEnter = (e) => {
      if (e.pointerType !== "mouse") return;
      [pos.x, pos.y] = local(e); apply();
      compare.classList.add("lens-on");
      compare.style.setProperty("--pos", "100%");
      gsap.to(radius, { r: 140, duration: 0.45, ease: EASE, onUpdate: setR, overwrite: true });
    };
    const onMove = (e) => { if (compare.classList.contains("lens-on")) { const [x, y] = local(e); toX(x); toY(y); } };
    const onLeave = () => gsap.to(radius, {
      r: 0, duration: 0.3, ease: "power2.in", onUpdate: setR, overwrite: true,
      onComplete: () => {
        compare.classList.remove("lens-on");
        compare.style.setProperty("--pos", `${compare.dataset.pos || 100}%`);
      },
    });
    compare.addEventListener("pointerenter", onEnter);
    compare.addEventListener("pointermove", onMove);
    compare.addEventListener("pointerleave", onLeave);
    return () => {
      compare.removeEventListener("pointerenter", onEnter);
      compare.removeEventListener("pointermove", onMove);
      compare.removeEventListener("pointerleave", onLeave);
    };
  }

  // The film opens like a window as it arrives.
  function filmScene() {
    const open = $(".film-open");
    if (!open || $("#film").hidden) return;
    const poster = $(".film-poster", open);
    const st = { trigger: open, start: "top 92%", end: "center 55%", scrub: 0.5 };
    gsap.fromTo(open, { clipPath: "inset(12% 16% round 18px)" }, { clipPath: "inset(-4% -4% round 18px)", ease: "none", scrollTrigger: st });
    if (poster) gsap.fromTo(poster, { scale: 1.18 }, { scale: 1, ease: "none", scrollTrigger: { ...st } });
  }

  // The highlighter runs under one phrase in every heading: the same marker that quotes the facts.
  function headingSweeps() {
    const hero = $(".hero .hl");
    if (hero) gsap.fromTo(hero, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.9, ease: "power2.inOut", delay: 0.5 });
    $$(".hl").filter((el) => !el.closest(".hero")).forEach((el) => {
      gsap.set(el, { backgroundSize: "0% 100%" });
      ScrollTrigger.create({ trigger: el, start: "top 82%", once: true, onEnter: () => gsap.to(el, { backgroundSize: "100% 100%", duration: 0.8, ease: "power2.inOut", delay: 0.35 }) });
    });
  }

  /* ---------- Wire it up per viewport and motion preference ---------- */
  const mm = gsap.matchMedia();
  mm.add({
    motion: "(prefers-reduced-motion: no-preference)",
    desk: "(min-width: 1024px)",
  }, (ctx) => {
    const { motion, desk } = ctx.conditions;
    if (!motion) {
      // Reduced motion: finished states only. The feed is shown where it sits in the flow (phones).
      if (feed) feed.hidden = desk;
      return;
    }
    heroScene(desk);
    gapScene();
    receiptScene();
    approvalScene();
    reveals();
    sweep();
    headingSweeps();
    filmScene();
    const offLens = desk ? lensScene() : () => {};
    return () => { if (feed) feed.hidden = true; offLens(); };
  });

  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => ScrollTrigger.refresh());
})();
