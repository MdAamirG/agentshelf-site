(() => {
  const cfg = window.AGENTSHELF || {};

  // Contact links from config.js. Without an email, CTAs point at the snapshot section.
  const subject = encodeURIComponent("AI shelf snapshot request");
  const body = encodeURIComponent("Store website:\nProducts you care about most:\nYour role:\n");
  document.querySelectorAll(".js-mail, .js-mail-plain").forEach((a) => {
    if (cfg.email) {
      a.href = a.classList.contains("js-mail")
        ? `mailto:${cfg.email}?subject=${subject}&body=${body}`
        : `mailto:${cfg.email}`;
    } else {
      a.href = "#snapshot";
    }
  });
  const cal = document.querySelector(".js-cal");
  if (cal && cfg.calendar) { cal.href = cfg.calendar; cal.hidden = false; }
  const li = document.querySelector(".js-linkedin");
  if (li && cfg.linkedin) { li.href = cfg.linkedin; li.hidden = false; }

  // Hero panel: Today / With AgentShelf toggle, plus one highlight sweep on first load.
  const facts = document.querySelector(".facts");
  const segs = document.querySelectorAll(".seg");
  if (!facts || !segs.length) return;

  const show = (state) => {
    facts.dataset.view = state;
    segs.forEach((s) => s.setAttribute("aria-pressed", String(s.dataset.state === state)));
  };
  segs.forEach((s) => s.addEventListener("click", () => {
    facts.classList.remove("is-revealing");
    facts.classList.add("is-revealed");
    show(s.dataset.state);
  }));

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) { show("after"); return; }
  show("before");
  facts.classList.add("is-revealing");
  setTimeout(() => {
    show("after");
    requestAnimationFrame(() => requestAnimationFrame(() => {
      facts.classList.add("is-revealed");
      facts.classList.remove("is-revealing");
    }));
  }, 1400);
})();
