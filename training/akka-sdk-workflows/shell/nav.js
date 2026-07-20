(function() {
  const slides = document.querySelectorAll('.deck-slide');
  const total = slides.length;

  // Deck name from the document title: "Akka SDK Fundamentals — Akka" -> "AKKA SDK FUNDAMENTALS"
  const deckName = (document.title || '')
    .replace(/\s*[—–-]\s*Akka\s*$/i, '')
    .trim()
    .toUpperCase();

  // Per-slide wayfinding rail (skipped on centred title / thanks slides).
  slides.forEach(function(slide, i) {
    if (slide.classList.contains('title-slide')) return;
    const footer = document.createElement('div');
    footer.className = 'deck-footer';
    const brand = document.createElement('span');
    brand.className = 'deck-footer-brand';
    brand.textContent = deckName;
    const num = document.createElement('span');
    num.className = 'deck-footer-num';
    num.textContent = (i + 1) + ' / ' + total;
    footer.appendChild(brand);
    footer.appendChild(num);
    slide.appendChild(footer);
  });

  // Global scroll-progress bar, anchored to the bottom edge of the viewport.
  const progress = document.createElement('div');
  progress.className = 'deck-progress';
  document.body.appendChild(progress);
  function updateProgress() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const y = window.scrollY || window.pageYOffset;
    const pct = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
    progress.style.transform = 'scaleX(' + pct + ')';
  }
  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress);
  updateProgress();

  const views = Array.from(document.querySelectorAll('[data-view]'));
  function top(el) { return el.getBoundingClientRect().top + (window.scrollY || window.pageYOffset); }
  function current() {
    const y = window.scrollY || window.pageYOffset;
    let best = 0;
    for (let i = 0; i < views.length; i++) if (top(views[i]) <= y + 12) best = i;
    return best;
  }
  document.addEventListener('keydown', function(e) {
    if (['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)) {
      e.preventDefault();
      const i = current();
      if (i < views.length - 1) window.scrollTo({ top: top(views[i + 1]), behavior: 'smooth' });
    }
    if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) {
      e.preventDefault();
      const i = current();
      const y = window.scrollY || window.pageYOffset;
      if (y > top(views[i]) + 12) window.scrollTo({ top: top(views[i]), behavior: 'smooth' });
      else if (i > 0) window.scrollTo({ top: top(views[i - 1]), behavior: 'smooth' });
    }
  });
})();
