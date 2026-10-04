'use strict';
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
