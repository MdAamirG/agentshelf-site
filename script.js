(() => {
  const cfg = window.AGENTSHELF || {};
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Contact links from config.js ---------- */
  const subject = encodeURIComponent("AI shelf snapshot request");
  const body = encodeURIComponent("Store website:\nProducts you care about most:\nYour role:\n");
  if (cfg.email) {
    document.querySelectorAll(".js-mail").forEach((a) => { a.href = `mailto:${cfg.email}?subject=${subject}&body=${body}`; });
    document.querySelectorAll(".js-mail-plain").forEach((a) => { a.href = `mailto:${cfg.email}`; });
    document.querySelectorAll(".js-mail-missing").forEach((p) => { p.hidden = true; });
  }
  const cal = document.querySelector(".js-cal");
  if (cal && cfg.calendar) { cal.href = cfg.calendar; cal.hidden = false; }
  const li = document.querySelector(".js-linkedin");
  if (li && cfg.linkedin) { li.href = cfg.linkedin; li.hidden = false; }

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
    sheet.classList.remove("is-before", "is-paused");
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

  /* ---------- Compare slider ---------- */
  const compare = document.querySelector(".compare");
  const range = document.getElementById("compare-range");
  if (compare && range) {
    const update = () => {
      compare.style.setProperty("--pos", `${range.value}%`);
      range.setAttribute("aria-valuetext", `${range.value}% shopper view, ${100 - range.value}% AI view`);
    };
    range.addEventListener("input", update);
    // Pointer drag anywhere on the comparison (mouse, pen, touch). The range input stays for keyboard users.
    const setFromX = (x) => {
      const r = compare.getBoundingClientRect();
      range.value = Math.round(Math.min(100, Math.max(0, ((x - r.left) / r.width) * 100)));
      update();
    };
    let dragging = false;
    compare.addEventListener("pointerdown", (e) => {
      dragging = true;
      compare.setPointerCapture(e.pointerId);
      setFromX(e.clientX);
      range.focus({ preventScroll: true });
      e.preventDefault();
    });
    compare.addEventListener("pointermove", (e) => { if (dragging) setFromX(e.clientX); });
    const stop = () => { dragging = false; };
    compare.addEventListener("pointerup", stop);
    compare.addEventListener("pointercancel", stop);
    update();
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
