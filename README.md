# DLIVR-Website

## Aktueller Stand · 14.09.2026

Die lokale Website wurde mit Franks Freigabe an den Stil von Mi-Tool angeglichen:
Helvetica-Systemschrift, dunkler Einstieg, helle Inhaltsflächen, feine Linien und
Graphit und Kupfer als freigegebene Farbrichtung (14.09.2026).
Logoakzent: `#b56846`, Buttons und Verweise: `#a65332`,
Akzent auf dunklem Grund: `#e2a185`. Das DLIVR-Logo greift die zwei
Quadrate am i auf und liegt für helle und dunkle Flächen als SVG mit
Schriftpfaden vor. Es benötigt keine installierte Schrift. Startseite, Leistungen und Kontakt verwenden dieselbe
Navigation und Gestaltung. Mi-Tool ist auf Start- und Leistungsseite als
Praxisbeispiel verlinkt; Inhalte stammen aus dem aktuellen Mi-Tool-Marketingprojekt.
Das dortige Logo wurde als lokale SVG-Datei übernommen.

**Live.** `dlivr.eu` liefert den Stand dieses Repositories aus; geprüft am 22.09.2026
per Hash-Vergleich von `index.html`, `css/style.css`, `leistungen.html` und
`kontakt.html` gegen Commit 870c72c vom 20.09.2026. Hostinger ist mit dem
GitHub-Repository verbunden und übernimmt jeden Push auf `main` automatisch;
ein Push ist damit eine Veröffentlichung.

## Dateien und Vorschau

- `index.html`: Einstieg, drei Schwerpunkte, Mi-Tool und Kurzprofil.
- `leistungen.html`: sechs Leistungsbereiche und Mi-Tool.
- `kontakt.html`: Kontakt, Anbieterangaben und bestehender Datenschutztext.
- `css/style.css`: gemeinsame Gestaltung und responsive Ansichten.
- `assets/dlivr-logo-hell.svg`, `assets/dlivr-logo-dunkel.svg`: DLIVR-Wortmarke.
- `assets/favicon.svg`: aus den beiden Quadraten abgeleitetes Website-Symbol.
- `assets/mi-tool-logo.svg`: Mi-Tool-Logo aus dem Marketingprojekt.

Statische HTML-Seiten ohne Build oder externe Schriftdateien. Ein kleines lokales
JavaScript steuert die Farbwahl und misst die Höhe der Kopfzeile für Sprungziele.
Eine lokale Vorschau lässt sich aus diesem Ordner starten:

```sh
python3 -m http.server 8873 --bind 127.0.0.1
```

Anschließend `http://127.0.0.1:8873/` im Browser öffnen.

## Hosting und historischer Live-Abzug

Am 01.09.2026 lieferten Repository und `dlivr.eu` unterschiedliche Seiten aus:
Die Domain antwortete über nginx; das Repository hatte eine GitHub-Pages-Konfiguration.
Die damalige Live-Seite verwendete ein dunkles Layout mit Rot `#c0392b`.

`live-abzug/dlivr-eu_2026-09-01.html` bleibt unverändert als historische Sicherung.
Sie ist nicht die Quelle dieser Überarbeitung. Am 13.09.2026 war der Live-Stand nicht
abrufbar; seit spätestens 22.09.2026 entspricht er diesem Repository.

## Entschieden am 23.09.2026

- E-Mail-Adresse der Website ist `ft@dlivr.eu` (Kontakt, Impressum, Datenschutz).
  Die frühere Repository-Adresse `frank.toepfer@dlivr-design.com` wird nicht mehr verwendet.
- Der Datenschutztext bleibt in der vorliegenden Fassung. Er wurde bei der
  Layoutarbeit nicht inhaltlich überarbeitet.

Ausgeliefert gehören nur die HTML-Dateien sowie `css/` und `assets/`; die historische
Sicherung und die Werkzeuge unter `werkzeug/` sind nicht Teil der Website.

## Designprüfung

`werkzeug/design-pruefen.py` prüft den hellen Tokenadapter am Anfang von `css/style.css`
gegen die Tokens des Design-Systems. Es liest sie direkt aus
`DLIVR_DATAHOUSE/GEMEINSAM/design-system/` (Repository `ORPAL-FT/design-system`,
freigegebene Version laut `freigabe.json`); eine lokale Kopie der Tokens gibt es seit
dem 22.09.2026 nicht mehr. `werkzeug/design/dlivr-hell.css` ist der Adapter der Website,
kein Bestandteil des Design-Systems. Logo-Entwürfe, Rechnungslogo und Briefkopf liegen
seit dem 22.09.2026 unter `GEMEINSAM/markenmaterial/`, nicht in diesem Repository.

Der Telefonlink wurde an die sichtbare Nummer `+49 (0)6583 – 990 41` angeglichen
(`tel:+49658399041`); zuvor enthielt er eine zusätzliche Null.

## Prüfung der Überarbeitung

Alle drei Seiten bei 320, 768 und 1440 Pixeln im Browser geprüft; keine
horizontalen Überläufe. Startseite zusätzlich bei 390 Pixeln visuell geprüft.
Lokale Verweise, Assets, Abschnittsziele und eindeutige IDs geprüft; Navigation
im Browser betätigt. `git diff --check` ohne Befund.

## Mi-Tool-Layoutkorrekturen übernommen · 14.09.2026

Abschnittsabstände sind jetzt einheitlich 32–48 px, Abstände unter Überschriften
20–32 px. Abschnittstitel folgen der Mi-Tool-Größenstaffel; Karten verwenden
eine gemeinsame Titelgröße, Innenabstände und gut sichtbare Nummern.
Kontaktspalten sind gleich breit. Zusätzliche Trennlinien zwischen Inhaltsbereichen
entfallen; die Linien innerhalb von Karten und der Kupferabschluss des Aufmachers
bleiben. Der Footer ist kompakter. Sprungziele berücksichtigen die Kopfleiste
nur einmal, mit zusätzlichem Abstand von 12 px zum Zielinhalt.

Übertragen wurden die passenden Layoutkorrekturen. Mi-Tool-spezifische Funktionen
wie IT-Blatt, Preise, Formulare und Dropdownnavigation gehören nicht zu diesem
Abgleich. Die rechtlichen Texte wurden dabei nicht geändert.

## Kopfzeile und Einstieg · diktierte Änderungen vom 14.09.2026

- Kopfzeile mit Mi-Tool-Abständen und Navigationsschriftgröße (.88 rem),
  eigenen SVG-Icons und mobilem Menü.
- Hell-/Dunkelschalter auf allen Seiten; ohne gespeicherte Auswahl gilt die
  Systemfarbe. Eine explizite Wahl wird lokal im Browser gespeichert.
- DLIVR- und Mi-Tool-Logos besitzen passende Varianten für beide Hintergründe.
- Einstieg über die ganze Breite, mit Mi-Tool-Schriftgrößen. Der Ablauf
  Verstehen / Ordnen / Umsetzen steht als einzige nummerierte Reihe darunter.
- Leistungsbereiche tragen Icons; auch die zusätzlichen Nummern im
  Mi-Tool-Beispiel entfallen.
- Geprüft: 320/768/1440 px, Bilder und Überläufe, Umschalten in beide
  Richtungen, gespeicherte Farbwahl beim Seitenwechsel und mobiles Menü.

## Verbindliche Layoutvorgabe · 14.09.2026

Frank möchte auf der DLIVR-Website eine dauerhaft sichtbare Kopf- und Fußzeile.
Nur der Mittelteil scrollt. Diese Vorgabe bei zukünftigen Layoutänderungen
beibehalten. Auf Mobilgeräten bleibt die Fußzeile kompakt; Logo, Impressum und
Datenschutz sind sichtbar, ergänzende Namens- und Copyrightzeilen entfallen dort.

Alle drei Seiten verwenden ein Raster über die dynamische Bildschirmhöhe.
Der Inhaltsbereich ist per Tastatur erreichbar; Sprungmarken berücksichtigen
den eigenen Scrollbereich. Beim Drucken wird der gesamte Inhalt ausgegeben.
Die frühere Messung der Kopfleistenhöhe ist dadurch nicht mehr erforderlich.

## Eine durchgehende Seite · 14.09.2026

Freigegebene Struktur: Einstieg → sechs Leistungen → Mi-Tool → Über mich →
Kontakt → Impressum und Datenschutz. Alle Inhalte werden in `index.html`
gepflegt. Die frühere Vorschau mit drei Leistungskarten entfällt.
Navigation und Kontaktlinks verwenden Sprungmarken; der aktive Menüpunkt
folgt dem Scrollbereich. Das mobile Menü schließt nach der Auswahl.
`leistungen.html` und `kontakt.html` sind nur noch Weiterleitungen, die bekannte
Sprungziele erhalten. Ohne JavaScript bieten sie direkte Links zur neuen Seite.
Feste Kopf- und Fußzeile, Kupferpalette und Farbmodus bleiben die Layoutvorgabe.

Geprüft: HTML-Struktur, eindeutige IDs und Sprungziele; Darstellung bei
320/768/1440 px ohne horizontalen Überlauf; mobiles Menü, Farbwechsel und
Weiterleitungen mit erhaltenem Sprungziel (Digitalisierung und Impressum).

## Separate Rechtstexte und E-Mail-Kontakt · 14.09.2026

Impressum und Datenschutz liegen wie bei Mi-Tool auf eigenen Seiten. Die
Hauptseite endet mit Kontakt; dort gibt es nur noch E-Mail an ft@dlivr.eu.
Telefon und Anschrift bleiben im Impressum. Das zusätzliche Footerlogo vor
Frank Töpfer entfällt. Frühere Rechts-Sprungziele werden weitergeleitet.

Basis sind die Mi-Tool-Rechtstexte vom 14.09.2026, angepasst auf die DLIVR-
Website: keine Formular-, Spamfilter- oder Fragefeld-Beschreibungen, Farbauswahl
unter dlivr-theme, keine Behauptung erfundener Fahrzeug-/Kundendaten.
Die ungeprüften Mi-Tool-Aussagen zu 30 Tagen Logaufbewahrung und einem bereits
bestehenden konkreten AV-Vertrag werden nicht übernommen. Vertragsgesellschaft,
AVV-Einbeziehung und tatsächliche Log-/CDN-Löschfristen sind weiterhin anhand
des Hostinger-Kontos zu präzisieren. Die veröffentlichte Fassung nennt
Speicherzwecke und verweist auf die Hostinger-Datenverarbeitungsbedingungen.
Quellen: https://www.hostinger.com/legal/dpa und
https://www.datenschutz.rlp.de/service/kontakt ; § 5 DDG.

## Bewegung und Zugänglichkeit · 14.09.2026

Der Ansatz Verstehen → Ordnen → Umsetzen erhält eine einmalige, zweisekündige
Kupferanimation. Bei reduzierter Bewegung bleibt die Darstellung statisch.
Texte sind jederzeit lesbar. Kontraste, kleine Beschriftungen, Tastaturfokus
und Sprungnavigation wurden nachgebessert. Der zusätzliche Kontaktlink vor
„E-Mail schreiben“ entfällt.

Ergänzung zur Layoutvorgabe: Bei sehr niedriger Fensterhöhe (bis 30 rem, z. B.
durch starken Zoom) scrollen Kopf- und Fußzeile mit, um Lesefläche zu erhalten.
Die normale Darstellung behält den festen Rahmen. Befunde, Prüfungen und
Grenzen stehen in `pruefungen/barrierefreiheit-2026-09-14.md`.

## PDF-Beratung und gegenseitige Footer-Verweise · 14.09.2026

Nach den sechs Leistungen steht ein kurzer eigener Abschnitt `#pdf-formulare`.
Er beschreibt strukturierte Formulare, Datenübernahme, nachvollziehbare Prüfungen
und bei Bedarf Unterschrift am Pad als Beratungsangebot. Technische Voraussetzungen
werden individuell abgestimmt. Grundlage: Franks Unterlage
PDF-Schnelleingabe_Funktionen_und_Nutzen.docx; keine unbelegten Zeitersparnisse,
Kundennamen oder pauschalen Schnittstellenversprechen übernommen.

Alle drei Fußzeilen verweisen auf Mi-Tool („Serviceunterlagen finden“) sowie
Franks bestehendes LinkedIn-Profil. Auf kleinen Bildschirmen zwei kompakte Zeilen;
die bei starker Vergrößerung mitlaufenden Leisten bleiben erhalten. Der Auftrag
für den passenden Mi-Tool-Gegenlink auf https://dlivr.eu/#pdf-formulare wurde
an die bestehende Mi-Tool-Aufgabe übergeben.

Geprüft: Desktop und 320 px, Tastatur-Sprung zum Kontakt sowie 200 % Textgröße
bei 320 px ohne horizontalen Überlauf. Der gezielte axe-Lauf meldet keine
automatischen Verstöße; der dekorative Footer-Pfeil bleibt manuell zu prüfen.
Die Barrierefreiheitshinweise wurden ebenfalls an Mi-Tool übergeben.

## Kontaktbereich · 14.09.2026

Gemeinsame Überschrift und Einleitung über zwei gleich gestalteten Karten,
angelehnt an Mi-Tool. Links Name, sichtbare E-Mail und Mailbutton, rechts
Orientierungsfragen. Desktop bündig und gleich hoch, mobil untereinander.
Desktop 1440 px und mobile Ansicht um 320 px visuell geprüft; kein horizontaler
Überlauf in der mobilen Ansicht. Kupferfarben und feste Fußzeile bleiben erhalten.

Die Animation bei „Verstehen / Ordnen / Umsetzen“ dauert vier Sekunden und
wird bei jedem internen Sprung auf Start neu vorbereitet. Sie beginnt erst,
wenn die Schritte sichtbar sind. Reduzierte Bewegung wird weiterhin respektiert.
Wiederholter Start per Tastatur im Browser geprüft: abgeschlossene Linie wird
zurückgesetzt und erneut aufgebaut.

Fokuskorrektur: Sprungziele behalten den Lesefokus. Bei Mausklicks erscheint
kein Rahmen um die Überschrift; Tastatur-Sprünge zeigen einen kontrastreichen
Fokusrahmen. Beide Eingabearten im Browser geprüft.

Der Einstiegsbereich folgt jetzt dem Hell-Dunkel-Schalter: im Hellmodus
warmer heller Hintergrund, dunkle Schrift und kräftiges Kupfer; im Dunkelmodus
dunkler Hintergrund mit hellen Texten. Buttons, Fokus und Schrittliniendarstellung
verwenden die passende Palette. Beide Modi und 320 px Breite geprüft.
