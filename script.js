(() => {
  const cfg = window.AGENTSHELF || {};
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Contact: form, email or WhatsApp, from config.js ---------- */
  // ?ref=brand-or-campaign on a cold-email link travels into the request, so you know which email worked.
  const params = new URLSearchParams(location.search);
  const ref = (params.get("ref") || params.get("utm_campaign") || "").slice(0, 60);
  const ctas = document.querySelectorAll(".js-cta");
  let wired = false;
  if (cfg.form) {
    const url = new URL(cfg.form, location.href);
    if (ref) url.searchParams.set("ref", ref);
    ctas.forEach((a) => { a.href = url.toString(); a.target = "_blank"; a.rel = "noopener"; });
    wired = true;
  } else if (cfg.email) {
    const body = encodeURIComponent(`Store website:\nProducts you care about most:\nYour role:\n${ref ? `\nRef: ${ref}\n` : ""}`);
    ctas.forEach((a) => {
      const subject = encodeURIComponent(a.dataset.subject || "Free AI check");
      a.href = `mailto:${cfg.email}?subject=${subject}&body=${body}`;
    });
    wired = true;
  }
  if (cfg.email) document.querySelectorAll(".js-mail-plain").forEach((a) => { a.href = `mailto:${cfg.email}`; });
  if (cfg.whatsapp) {
    const text = encodeURIComponent(`Hi Mohamed, I'd like a free AI check for my store.${ref ? ` (ref: ${ref})` : ""}`);
    document.querySelectorAll(".js-wa").forEach((a) => { a.href = `https://wa.me/${String(cfg.whatsapp).replace(/\D/g, "")}?text=${text}`; a.hidden = false; });
    wired = true;
  }
  if (wired) document.querySelectorAll(".js-cta-missing").forEach((p) => { p.hidden = true; });
  const li = document.querySelector(".js-linkedin");
  if (li && cfg.linkedin) { li.href = cfg.linkedin; li.hidden = false; }
  const photo = document.querySelector(".js-photo");
  if (photo && cfg.photo) {
    photo.src = cfg.photo; photo.hidden = false;
    const mono = document.querySelector(".js-monogram");
    if (mono) mono.hidden = true;
  }

  /* ---------- Hero sheet: highlight -> connector -> callout ---------- */
  const sheet = document.getElementById("sheet");
  const links = sheet && sheet.querySelector(".links");
  const marks = sheet ? [...sheet.querySelectorAll("mark[data-link]")] : [];
  const order = ["fabric", "width", "frame", "warranty"];
  marks.forEach((m) => m.style.setProperty("--i", order.indexOf(m.dataset.link)));
  sheet && sheet.querySelectorAll("[data-anchor]").forEach((g) => g.style.setProperty("--i", order.indexOf(g.dataset.anchor)));

  const NS = "http://www.w3.org/2000/svg";
  function drawLinks() {
    if (!links) return;
    links.replaceChildren();
    if (getComputedStyle(links).display === "none") return;
    const box = sheet.getBoundingClientRect();
    const card = sheet.querySelector(".page-card").getBoundingClientRect();
    links.setAttribute("viewBox", `0 0 ${box.width} ${box.height}`);
    marks.forEach((m) => {
      const target = sheet.querySelector(`[data-anchor="${m.dataset.link}"]`);
      if (!target) return;
      const first = m.getClientRects()[0];
      // Aim at the label itself, not the whole group (which includes its leader line).
      const t = (target.querySelector("rect") || target.querySelector(".tag-shape") || target).getBoundingClientRect();
      // Leave from the card's right edge at the highlighted line, like a footnote leader.
      const x1 = card.right - box.left, y1 = first.top + first.height / 2 - box.top;
      const x2 = t.left - box.left - 6, y2 = t.top + t.height / 2 - box.top;
      const mid = (x1 + x2) / 2;
      const path = document.createElementNS(NS, "path");
      path.setAttribute("d", `M${x1} ${y1} C${mid} ${y1}, ${mid} ${y2}, ${x2} ${y2}`);
      path.style.setProperty("--i", order.indexOf(m.dataset.link));
      links.appendChild(path);
      const len = Math.ceil(path.getTotalLength());
      path.style.setProperty("--len", len);
      const dot = document.createElementNS(NS, "circle");
      dot.setAttribute("cx", x2); dot.setAttribute("cy", y2); dot.setAttribute("r", 3);
      dot.style.setProperty("--i", order.indexOf(m.dataset.link));
      links.appendChild(dot);
    });
  }

  const toggle = document.getElementById("play-toggle");
  const replay = document.getElementById("replay");
  const answer = sheet && sheet.querySelector(".answer");

  function finish() {
    // Clearing is-playing leaves the same finished look but releases the highlights, lines and cards
    // from their CSS animations, so the scroll scene in motion.js can drive them.
    sheet.classList.remove("is-before", "is-paused", "is-playing");
    if (toggle) { toggle.disabled = true; toggle.textContent = "Pause"; toggle.setAttribute("aria-pressed", "false"); }
  }
  function play() {
    if (!sheet || reduced) { finish(); return; }
    sheet.classList.remove("is-playing", "is-paused");
    sheet.classList.add("is-before");
    void sheet.offsetWidth; // restart the CSS animations
    sheet.classList.add("is-playing");
    if (toggle) { toggle.disabled = false; toggle.textContent = "Pause"; toggle.setAttribute("aria-pressed", "false"); }
  }
  answer && answer.addEventListener("animationend", (e) => { if (e.animationName === "rise") finish(); });
  toggle && toggle.addEventListener("click", () => {
    const paused = sheet.classList.toggle("is-paused");
    toggle.textContent = paused ? "Play" : "Pause";
    toggle.setAttribute("aria-pressed", String(paused));
  });
  replay && replay.addEventListener("click", () => { drawLinks(); play(); });

  if (sheet) {
    sheet.classList.add("is-before");
    const start = () => {
      drawLinks();
      // Start when the sheet is actually on screen, once.
      if ("IntersectionObserver" in window && !reduced) {
        const io = new IntersectionObserver((entries) => {
          if (entries.some((e) => e.isIntersecting)) { io.disconnect(); play(); }
        }, { threshold: 0.12 });
        io.observe(sheet);
      } else { play(); }
    };
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(start);
    let raf;
    window.addEventListener("resize", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(drawLinks); });
  }

  /* ---------- Shopper vs AI: a two-way toggle (desktop also gets the X-ray lens in motion.js) ---------- */
  const compare = document.querySelector(".compare");
  const viewButtons = [...document.querySelectorAll(".vt")];
  if (compare && viewButtons.length) {
    const show = (pos, animate) => {
      if (animate && !reduced) {
        compare.classList.add("is-animating");
        setTimeout(() => compare.classList.remove("is-animating"), 520);
      }
      compare.dataset.pos = pos;
      compare.style.setProperty("--pos", `${pos}%`);
      viewButtons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.pos === pos)));
    };
    viewButtons.forEach((b) => b.addEventListener("click", () => show(b.dataset.pos, true)));
    show("100", false);
    // Phones have no hover lens: start on the shopper's view, then show what the AI reads, once.
    if (window.matchMedia("(max-width: 720px)").matches && !reduced && "IntersectionObserver" in window) {
      const once = new IntersectionObserver(([e]) => {
        if (!e.isIntersecting) return;
        once.disconnect();
        setTimeout(() => { if (compare.dataset.pos === "100") show("0", true); }, 900);
      }, { threshold: 0.5 });
      once.observe(compare);
    }
  }

  /* ---------- Mobile sticky action: after the hero button, until the closing section ---------- */
  const heroCta = document.querySelector(".hero .cta-row");
  const startSection = document.getElementById("start");
  if (heroCta && startSection && "IntersectionObserver" in window) {
    let pastHero = false, atStart = false;
    const sync = () => document.body.classList.toggle("show-sticky", pastHero && !atStart);
    new IntersectionObserver(([e]) => { pastHero = !e.isIntersecting && e.boundingClientRect.top < 0; sync(); }).observe(heroCta);
    // Hide over the FAQ (so it never covers an answer) and over the closing CTA.
    const covering = new Set();
    const cover = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) covering.add(e.target); else covering.delete(e.target); });
      atStart = covering.size > 0; sync();
    }, { threshold: 0.2 });
    [startSection, document.getElementById("faq")].forEach((el) => el && cover.observe(el));
  }

  /* ---------- Film (only when config.film is set) ---------- */
  const film = document.getElementById("film");
  if (film && cfg.film && cfg.film.src) {
    film.hidden = false;
    const poster = film.querySelector(".film-poster");
    if (cfg.film.poster) poster.src = cfg.film.poster;
    const dialog = document.getElementById("film-dialog");
    const video = dialog.querySelector("video");
    video.src = cfg.film.src;
    if (cfg.film.captions) video.querySelector("track").src = cfg.film.captions;
    document.getElementById("film-open").addEventListener("click", () => { dialog.showModal(); video.play().catch(() => {}); });
    const close = () => { video.pause(); dialog.close(); };
    document.getElementById("film-close").addEventListener("click", close);
    dialog.addEventListener("close", () => video.pause());
    dialog.addEventListener("click", (e) => { if (e.target === dialog) close(); });
  }
})();
