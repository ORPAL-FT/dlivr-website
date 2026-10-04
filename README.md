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

## Partnerseite · 25.09.2026

`partner.html` wird **nicht von Hand bearbeitet**. Sie entsteht aus der
gemeinsamen Quelle `GEMEINSAM/inhalte/partner.json` (Repo `ORPAL-FT/inhalte`),
die sich mi-tool.tech und dlivr.eu teilen:

```bash
python3 werkzeug/partner-erzeugen.py            # schreibt partner.html
python3 werkzeug/partner-erzeugen.py --pruefen  # meldet nur, ob sie aktuell ist
```

Gebaut wird nur, was freigegeben ist: `"dlivr"` muss in `seiten` stehen, `aktiv`
auf `true` und die Beschreibung darf nicht leer sein. Die Regeln stehen in
`schema.md` der Quelle. Ist nichts freigegeben, entsteht eine leere Seite mit
Hinweis — dann gehört der Navigationseintrag wieder heraus.

Kopf und Fuß schreibt der Generator nicht ab, sondern nimmt sie aus
`index.html` und schreibt `href="#…"` zu `href="index.html#…"` um. Ändert sich
die Navigation der Startseite, zieht der nächste Lauf sie mit. Die Seite
verwendet nur vorhandene Bausteine (`.section`, `.wrap`, `.cards`, `.card`,
`.label`, `.text-link`) — an `css/style.css` ändert sich nichts.

Ändert sich ein Text, wird er **in der Quelle** geändert, nicht hier; danach
laufen die Generatoren in **beiden** Webseiten-Repos.

Seit dem 25.09.2026 steht der gemeinsame Teil der Generatoren in
`werkzeug/inhalte.py`: Quelle lesen, sieben, schreiben, prüfen, Logos, Rahmen,
Sortierung. `partner-erzeugen.py` und `referenzen-erzeugen.py` enthalten nur
noch das Layout ihrer Seite. Wer eine Baustopp-Regel ändert, ändert sie damit
für beide Seiten zugleich — sie können nicht mehr auseinanderlaufen.
`beitraege-erzeugen.py` bleibt vorerst für sich: es hat eigene Regeln
(`veroeffentlicht_am`, `geplant_zeigen`, verstrichene Termine).

## Referenzseite · 25.09.2026

`referenzen.html` entsteht wie die Partnerseite aus der gemeinsamen Quelle,
hier aus `GEMEINSAM/inhalte/referenzen.json`:

```bash
python3 werkzeug/referenzen-erzeugen.py            # schreibt referenzen.html
python3 werkzeug/referenzen-erzeugen.py --pruefen  # meldet nur, ob sie aktuell ist
```

Der Unterschied zur Partnerseite ist der Schalter. Bei Partnern entscheidet
`aktiv`, bei Referenzen `freigegeben_am` — und dieses Datum trägt die Freigabe
**des Kunden**, die Frank einholt. Ohne das Datum erscheint ein Haus nirgends,
auch nicht mit Namen. Die Karte zeigt Kategorie, Name, Leistung, den Satz aus
`beschreibung` (er nennt auch den Ort) und, falls vorhanden, das Logo. Ein
Zitat steht dort nicht: dafür bräuchte es eine eigene schriftliche Freigabe,
und die Quelle führt kein Feld dafür. Verwendet sind nur vorhandene Bausteine
(`.section`, `.wrap`, `.cards`, `.card`, `.service-card`, `.service-lead`,
`.label`, `.text-link`) — an `css/style.css` ändert sich nichts.

**Stand 25.09.2026: kein Eintrag ist freigegeben.** Die Seite entsteht
trotzdem, bleibt aber leer und steht **nicht** in der Navigation. Trägt
`referenzen.json` das erste `freigegeben_am`, gehört der Navigationseintrag in
`index.html` nachgezogen; der nächste Generatorlauf zieht ihn dann in alle
erzeugten Unterseiten mit.

Zwei Häuser stehen als Entwurf in der Quelle, beide für dlivr.eu vorgesehen.
Solange `freigegeben_am` leer ist, landet keines von beiden im ausgelieferten
HTML — auch nicht der Kundenname.

## Arbeitsablauf: Änderungen an der Website

Jeder Push auf `main` geht sofort live. Deshalb ist `main` seit dem 23.09.2026 durch die
GitHub-Regel „main nur per Pull Request“ geschützt: kein direkter Push, kein Löschen,
kein Überschreiben der Historie, auch nicht für Administratoren.

1. Änderungen auf einem Zweig vorbereiten (`git checkout -b <thema>`), committen, pushen.
2. Pull Request gegen `main` öffnen; die Beschreibung nennt, was sich sichtbar ändert.
3. Frank prüft und mergt. Der Merge ist die Freigabe und zugleich die Veröffentlichung;
   Hostinger übernimmt den neuen Stand automatisch. Der Zweig wird beim Merge gelöscht.

Kleine Korrekturen gehen denselben Weg, nur schneller. Muss die Regel einmal umgangen
werden, lässt sie sich unter Settings › Rules › Rulesets vorübergehend deaktivieren.

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

## Beitragsseite

`beitraege.html` zeigt die LinkedIn-Beiträge und wird **nicht von Hand
bearbeitet**. Quelle ist `GEMEINSAM/inhalte/beitraege.json` (Repo
`ORPAL-FT/inhalte`), dieselbe Ablage wie bei den Partnern; mi-tool.tech baut
aus derselben Datei seine eigene Fassung.

```bash
python3 werkzeug/beitraege-erzeugen.py            # schreibt beitraege.html
python3 werkzeug/beitraege-erzeugen.py --pruefen  # meldet nur, ob sie aktuell ist
```

Ein Beitrag mit `veroeffentlicht_am` erscheint vollständig, mit Text, Grafik
und dem Verweis auf LinkedIn. Ein geplanter Beitrag erscheint höchstens als
Datum und Titel unter „Demnächst“, und nur mit `geplant_zeigen: true`. So
steht hier nie ein Text, den es auf LinkedIn noch nicht gibt.

Die Seite lädt nichts von LinkedIn nach. Die Grafiken kommen aus `bilder/` der
Quelle und werden beim Lauf nach `assets/beitraege/` kopiert und mitcommittet.

Ändert sich ein Text, wird er **in der Quelle** geändert; danach laufen die
Generatoren in **beiden** Webseiten-Repos.

### Partnerlogos

Seit dem 25.09.2026 trägt jede Partnerkarte das Logo des Partners, sofern er
eines geliefert hat. Die Dateien liegen in `logo/` der gemeinsamen Quelle und
werden beim Lauf nach `assets/partner/` kopiert und mitcommittet; von fremden
Servern wird nichts geladen. Liefert ein Partner eine helle Fassung
(`logo_dunkelmodus`), schaltet die Seite im Dunkelmodus darauf um, mit
denselben Klassen wie die eigene Wortmarke. Ohne Logo bleibt die Karte bei
Name, Text und Verweis.

## Auffindbarkeit

Stand 25.09.2026, drei Grundlagen nachgeholt:

- `robots.txt` und `sitemap.xml` liegen jetzt vor. Die Sitemap führt die fünf
  echten Seiten; `leistungen.html` und `kontakt.html` sind nur Merkzettel für
  alte Lesezeichen und bleiben ausgeschlossen. Ändert sich der Seitenbestand,
  gehört die Sitemap von Hand nachgezogen.
- Jede Seite trägt Angaben für die Linkvorschau (Open Graph). Das Bild ist
  `assets/dlivr-link-vorschau-20260925.png`, 1200 × 630, aus der Wortmarke und
  den Markenfarben des Design-Systems v1.3.1 gesetzt. Bei einem neuen Bild
  einen neuen Dateinamen verwenden, sonst zeigen die Plattformen weiter das
  alte aus ihrem Zwischenspeicher.
- `beitraege.html` verweist mit `canonical` auf die Fassung von mi-tool.tech.
  Dieselben Beitragstexte stehen auf beiden Webseiten; welche als Original
  gilt, steht im Kopf der gemeinsamen Quelle unter `kanonische_seite`. Dreht
  man das dort um, folgen beide Generatoren.

## Auslieferung · 26.09.2026

Hostinger uebernimmt den Zweig `main` ueber die Git-Anbindung von hPanel — und
zwar ganz: Was im Zweig liegt, liegt in `public_html`. Bis zum 26.09.2026 waren
darum `werkzeug/*.py`, `README.md`, `pruefungen/` und `.gitignore` ueber
dlivr.eu mit HTTP 200 zu lesen.

Seitdem sperrt eine `.htaccess` die Arbeitsdateien: `*.md`, `*.py`, `*.sh`,
`*.toml`, `*.yml`, die Verzeichnisse `werkzeug/`, `pruefungen/` und
`live-abzug/`, alles was mit `.git` beginnt, sowie `.DS_Store`. Oeffentlich
bleiben die `.html`-Seiten, `assets/`, `css/`, `robots.txt` und `sitemap.xml`.
Verzeichnislisten sind aus.

Die Datei setzt bewusst **keine** Kopfzeilen und **keine** Umleitungen. Wer
Inhaltssicherheitsregeln oder HSTS will, entscheidet das getrennt — beides
wirkt sofort auf die ganze Domaene.

Neue Datei im Repo? Dann gehoert sie entweder zu den oeffentlichen Pfaden oder
in die Sperrliste.

## Qualitätscheck · 30.09.2026

Ein Durchgang über beide Sites. In dlivr.eu war alles Ausgelieferte in
Ordnung — Seiten, Sitemap, interne Verweise, die `.htaccess` vom 26.09.2026
(`werkzeug/` und `README.md` antworten jetzt mit 404 bzw. 403, der alte
`.pyc` ist weg). Gerichtet wurden zwei Kleinigkeiten:

**`referenzen.html` bekommt Link-Vorschaudaten.** `partner.html` und
`beitraege.html` trugen `og:`-Angaben, `referenzen.html` nicht: Wer die Seite
in LinkedIn oder einem Messenger teilte, bekam keinen Titel und kein Bild.
`werkzeug/referenzen-erzeugen.py` setzt sie jetzt wie die Partnerseite; die
Seite ist neu erzeugt.

**`robots.txt` sprach von „den drei Weiterleitungsseiten“** und sperrte zwei.
Es waren immer zwei — `leistungen.html` und `kontakt.html`.

Offen und nicht hier zu erledigen: Für dlivr.eu gibt es **keinen
DMARC-Eintrag** (`_dmarc.dlivr.eu` ist leer) und keinen DKIM-Selektor. SPF
steht mit `-all` auf Microsoft 365. Ein erster Eintrag zum Mitlesen wäre
`_dmarc.dlivr.eu  TXT  "v=DMARC1; p=none; rua=mailto:ft@dlivr.eu"`; scharf
gestellt wird er erst, wenn die Berichte zeigen, dass alles Legitime
durchkommt.

Die Liste „Demnächst“ auf `beitraege.html` altert wie ihr Gegenstück auf
mi-tool.tech — beide kommen aus derselben Quelle. Ein vergangener Termin
fällt in `mi-tool-website/werkzeug/pruefen.py` als Warnung auf; ein eigener
Prüfer hier wäre dieselbe Meldung ein zweites Mal.

## Startseite mit Linien und Formularbeispiel · 05.10.2026

Auf Franks „Bitte alles umsetzen“ nach dem Vorschlag vom selben Tag.

**Strichgrafiken der Leistungen.** Jede der sechs Leistungskarten trägt statt
des kleinen Symbols eine eigene Strichgrafik in Kupfer (`--accent`): vom
Durcheinander zur Richtung, eine Lücke überbrücken, das Fahrzeug, ein Ablauf
mit Prüfung am Ende, drei Überschneidungen, Meilensteine bis zur Übergabe.
Sie führen die Linie der drei Schritte im Kopf weiter und zeichnen sich beim
ersten Sichtkontakt einmal (`pathLength="1"`, CSS-Animation).

**Formularbeispiel.** Im PDF-Abschnitt ersetzt ein Prüfprotokoll in HTML das
frühere Standbild (`assets/pdf-formular-beispiel.svg`, ausgetragen). Es füllt
sich einmal in fünf Schritten aus: Kopfdaten aus einem Textbaustein,
eindeutige Auswahl „i. O.“/„n. i. O.“ mit Kürzel und Uhrzeit, ein
unbeantworteter Punkt sichtbar, offene Mängel zusammengefasst. Es zeigt nur,
was Franks Beiträge vom 17.09., 24.09. und 01.10.2026 öffentlich zusagen;
eine bedingte Einblendung ist bewusst nicht dabei.

**Kein mi-tool-Nachbau hier.** Die Suchvorführung von mi-tool.tech läuft
nicht auch auf dlivr.eu: in DLIVR-Kupfer wäre sie keine echte
mi-tool-Oberfläche, und für mi-tool-Blau im Dunkelmodus gibt es im
Design-System keine freigegebenen Werte. Der Abschnitt zeigt weiter das echte
Bildschirmfoto vom 28.09.2026.

Bewegung in `assets/linien.js`, ohne Bibliothek (IntersectionObserver, Rest
CSS). Einmal beim Sichtkontakt, keine Schleife; ohne JavaScript, bei
reduzierter Bewegung und im Druck steht sofort der Endzustand, denn das HTML
trägt ihn. Geprüft: Desktop 1440 und Telefon 393, hell und dunkel, reduzierte
Bewegung, ohne JavaScript, Druck. `style.css?v=` auf allen Seiten und in den
Generatoren nachgezogen.

## Zwei Angebote und Cache-Zeile · 05.10.2026

Auf Franks Wunsch, die beiden Seiten aktiver zu verbinden: Vor dem Kontakt
steht `#angebote` „Zwei Angebote. Ein Ansprechpartner.“ — DLIVR mit den
PDF-Formularen (Knopf zum Formularbeispiel) und mi-tool mit Knopf zu
mi-tool.tech; Gegenstück auf mi-tool.tech. Im mi-tool-Abschnitt ist aus dem
Textverweis ein Knopf geworden („mi-tool.tech ansehen“, dazu „Die Suche in
Aktion“).

`.htaccess`: HTML-Seiten tragen jetzt `Cache-Control: no-cache,
must-revalidate`, wie auf mi-tool.tech. Ohne die Zeile zeigte ein Browser am
05.10. Minuten nach dem Ausrollen noch die alte Startseite.

