# Gezielter Barrierefreiheitsdurchgang · 14.09.2026

Umfang: Startseite, Impressum, Datenschutz. Orientierung an WCAG 2.2 AA;
kein vollständiger Konformitätsnachweis. Geprüft im integrierten Chromium-Browser,
per HTML-/CSS-/JavaScript-Inspektion und anhand des Accessibility-Baums.

## Korrigierte Befunde

- Kupfertext auf dem hellen Produkthintergrund: bisher 4,38:1. Textakzent
  auf #99482b abgedunkelt; die kupferne Buttonfüllung bleibt unverändert.
- Fokusumrandung auf dunklem Hero: bisher 2,96:1. Jetzt helles Kupfer
  mit 7,33:1 zum Hintergrund; auch in der Fußzeile.
- Sehr kleine Beschriftungen (9–11 px) auf mindestens 12 px erhöht,
  mobile Rechtslinks auf 13 px. Das ist eine Verbesserung der Lesbarkeit,
  keine Behauptung einer pauschalen WCAG-Mindestschriftgröße.
- Bei Fensterhöhe bis 30 rem scrollt die gesamte Seite, damit feste Leisten
  bei starker Vergrößerung nicht den Lesebereich belegen.
- Sprungnavigation setzt Fokus auf die Zielüberschrift. Bei Tastaturauslösung
  erfolgt der Sprung sofort; bei Mausauslösung sanft, sofern Bewegung erlaubt ist.
- Aktiver Menüpunkt zusätzlich unterstrichen. Mobiles Menü schließt bei Escape,
  Auswahl und wenn der Fokus das Menü verlässt.
- Lange Überschriften dürfen umbrechen. Druckfarben bleiben auch nach Auswahl
  des Dunkelmodus lesbar; der Ansatz mit den drei Schritten bleibt im Druck erhalten.
- Redundanter Link „Lassen Sie uns sprechen“ vor dem direkten Kontakt entfernt.

## Neue Animation

Der kupferne Pfad und seine drei Markierungen erscheinen beim ersten Sichtbarwerden
in maximal zwei Sekunden. Kein Loop; Wörter und Zahlen bleiben durchgehend sichtbar.
Dekoration ausschließlich über CSS-Pseudoelemente, keine Live-Region und keine
zusätzlichen Ansagen. Ohne JavaScript oder IntersectionObserver bleibt die Grafik
statisch. Bei prefers-reduced-motion: reduce ist sie statisch; eine während des
Besuchs eingeschaltete Reduzierung beendet die Bewegung. CSS-/JS-Zweige geprüft;
ein realer Wechsel der Betriebssystemeinstellung wurde nicht vorgenommen.

## Ausgeführte Prüfungen

- Berechnete Textfarben gegen die jeweiligen Hintergründe in beiden Farbmodi:
  Startseite 95 Textelemente, Impressum 35, Datenschutz 43. Kein unterschrittener
  4,5:1-/3:1-Grenzwert in dieser DOM-Messung. Kleinster gemessener Wert:
  Startseite hell 4,81:1, dunkel 5,38:1; Rechtsseiten hell 5,29:1, dunkel 7,35:1.
  Verdeckte Menülinks werden ergänzend durch Tastaturbedienung geprüft;
  die Messung ersetzt keine Pixelanalyse aller möglichen Zustände.
- Reflow bei 320 × 225 CSS-Pixeln auf allen drei Seiten, entsprechend 400 %
  eines 1280 × 900-Fensters: keine horizontale Überbreite, Hauptinhalt frei
  scrollbar, Leisten im Dokumentfluss. Das war eine Viewport-Simulation,
  kein tatsächlicher Browser-Zoom oder Text-only-Zoom.
- Zusätzlich Startseite bei 640 × 450 CSS-Pixeln (200-%-Reflow): keine
  horizontale Überbreite und Leisten im Dokumentfluss. Mobile Footerlinks
  haben 44 px Höhe; Tastatursprung-Abstand am Ziel gemessen: 12,09 px.
- Textabstände auf allen drei Seiten bei 320 px Breite: Zeilenhöhe 1,5,
  Buchstabenabstand 0,12 em, Wortabstand 0,16 em, Absatzabstand 2 em.
  Keine horizontale Überbreite. Test über eine temporäre lokale Prüfvorschau;
  die veröffentlichten Seiten enthalten keine Testschalter.
- Desktop- und Mobilansicht visuell geprüft, Hauptnavigation per Enter,
  mobiles Menü per Enter/Tab/Escape, Kontaktansprung mit Fokus auf h2 und
  nächster Tab auf „E-Mail schreiben“. Der fokussierte Link ist sichtbar.
- Accessibility-Baum: eine h1 pro Seite, geordnete Leistungsüberschriften,
  benannte Navigation und Farbmodus-Schalter, Hauptinhalt und Fußbereich,
  Alternativtexte der Logos; dekorative SVG-Icons von Ansagen ausgeschlossen.
- Syntaxprüfung JavaScript, lokale Links, eindeutige IDs und HTML-Struktur.

## Grenzen

Keine vollständige WCAG-Prüfung aller Erfolgskriterien, kein praktischer
VoiceOver-/NVDA-Durchgang und kein realer 200-%-Text-only-Zoom. Eine Aussage
„vollständig barrierefrei“ wird daher nicht veröffentlicht. Die BFSG-Einordnung
wurde durch diesen technischen Durchgang nicht rechtlich bestätigt.

## Referenzen

- [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)
- [Textabstände](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)
- [Fokus nicht verdeckt](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)
- [Bewegung pausieren oder stoppen](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
