'use strict';
/* Formularmuster mit Reitern, seit 28.10.2026: unabhängig von Bewegung, läuft immer. */
(() => {
  /* --- Formularmuster: Reiter (seit 28.10.2026). Ohne JS stehen alle Muster untereinander. --- */
  const reiterliste = document.querySelector('.muster-reiter');
  if (reiterliste) {
    const reiter = Array.from(reiterliste.querySelectorAll('[role="tab"]'));
    const zeigen = (aktiv, fokus) => {
      reiter.forEach(r => {
        const an = r === aktiv;
        r.setAttribute('aria-selected', an ? 'true' : 'false');
        r.tabIndex = an ? 0 : -1;
        document.getElementById(r.getAttribute('aria-controls')).hidden = !an;
      });
      if (fokus) aktiv.focus();
    };
    reiterliste.hidden = false;
    document.documentElement.classList.add('muster-bereit');
    zeigen(reiter[0], false);
    reiter.forEach((r, i) => {
      r.addEventListener('click', () => zeigen(r, false));
      r.addEventListener('keydown', e => {
        const ziel = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: reiter.length - 1 }[e.key];
        if (ziel === undefined) return;
        e.preventDefault();
        zeigen(reiter[(ziel + reiter.length) % reiter.length], true);
      });
    });
  }
})();

/* Bewegung auf der Startseite, seit 05.10.2026: Die Strichgrafiken der
 * Leistungen zeichnen sich, das Formularbeispiel füllt sich aus. Keine
 * Bibliothek — Sichtkontakt per IntersectionObserver, der Rest ist CSS.
 *
 * Regeln aus dem Design-System („Abstände und Bewegung“, 20.09.2026):
 *   - Jeder Ablauf läuft einmal beim Sichtkontakt und bleibt dann stehen.
 *   - Das HTML trägt den fertigen Endzustand. Ohne JavaScript, bei
 *     reduzierter Bewegung und im Druck bleibt genau der stehen.
 */
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)');
  const druck = window.matchMedia('print');
  if (ruhig.matches || druck.matches || !('IntersectionObserver' in window)) return;

  const wurzel = document.documentElement;
  const zeitgeber = [];
  const amEnde = () => {
    zeitgeber.forEach(clearTimeout);
    wurzel.classList.remove('linien-bereit', 'formular-bereit');
  };
  window.addEventListener('beforeprint', amEnde);
  druck.addEventListener('change', e => { if (e.matches) amEnde(); });
  ruhig.addEventListener('change', e => { if (e.matches) amEnde(); });

  const einmal = (ziele, wenn, schwelle) => {
    const wache = new IntersectionObserver((eintraege, selbst) => {
      eintraege.forEach(eintrag => {
        if (!eintrag.isIntersecting) return;
        selbst.unobserve(eintrag.target);
        wenn(eintrag.target);
      });
    }, { threshold: schwelle });
    ziele.forEach(ziel => wache.observe(ziel));
  };

  /* --- Strichgrafiken der Leistungen --- */
  const linien = Array.from(document.querySelectorAll('.leistung-linie'));
  if (linien.length) {
    wurzel.classList.add('linien-bereit');
    einmal(linien, svg => svg.classList.add('zeichnet'), 0.6);
  }

  /* --- Formularbeispiel füllt sich Schritt für Schritt --- */
  const formular = document.querySelector('[data-formular]');
  if (formular) {
    const schritte = Array.from(formular.querySelectorAll('[data-schritt]'));
    const hoechster = Math.max(...schritte.map(el => Number(el.dataset.schritt)));
    wurzel.classList.add('formular-bereit');
    einmal([formular], () => {
      for (let n = 1; n <= hoechster; n += 1) {
        zeitgeber.push(setTimeout(() => {
          schritte.filter(el => Number(el.dataset.schritt) === n).forEach(el => el.classList.add('da'));
        }, 400 + (n - 1) * 900));
      }
    }, 0.45);
  }
})();
