# DLIVR-Website

## Aktueller Stand · 14.09.2026

Die lokale Website wurde mit Franks Freigabe an den Stil von Mi-Tool angeglichen:
Helvetica-Systemschrift, dunkler Einstieg, helle Inhaltsflächen, feine Linien und
Blau `#1c69d4` als Akzent. Startseite, Leistungen und Kontakt verwenden dieselbe
Navigation und Gestaltung. Mi-Tool ist auf Start- und Leistungsseite als
Praxisbeispiel verlinkt; Inhalte stammen aus dem aktuellen Mi-Tool-Marketingprojekt.
Das dortige Logo wurde als lokale SVG-Datei übernommen.

**Lokal umgesetzt und auf GitHub aktualisiert.** Frank klärt den Umzug vom bisherigen
Hosting zu Hostinger. Es wurden keine DNS-, Hosting- oder GitHub-Pages-Einstellungen
geändert. Eine Veröffentlichung auf dem Zielhosting steht noch aus.

## Dateien und Vorschau

- `index.html`: Einstieg, drei Schwerpunkte, Mi-Tool und Kurzprofil.
- `leistungen.html`: sechs Leistungsbereiche und Mi-Tool.
- `kontakt.html`: Kontakt, Anbieterangaben und bestehender Datenschutztext.
- `css/style.css`: gemeinsame Gestaltung und responsive Ansichten.
- `assets/mi-tool-logo.svg`: Mi-Tool-Logo aus dem Marketingprojekt.

Statische HTML-Seiten ohne Build, externe Schriftdateien oder JavaScript.
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
Sie ist nicht die Quelle dieser Überarbeitung. Der aktuelle Live-Stand konnte am
13.09.2026 nicht abgerufen werden.

## Vor der späteren Veröffentlichung klären

- Zielverzeichnis und Auslieferung bei Hostinger mit Frank abstimmen.
- E-Mail-Adresse bestätigen: hier bleibt die bisherige Repository-Adresse
  `frank.toepfer@dlivr-design.com`; der historische Live-Abzug nennt `ft@dlivr.eu`.
- Bestehenden Datenschutztext auf das tatsächliche Hosting und den Umgang mit
  Anfragen abstimmen. Er wurde bei der Layoutarbeit nicht inhaltlich überarbeitet.
- Nur die drei HTML-Dateien sowie `css/` und `assets/` ausliefern; die historische
  Sicherung und Repository-Dateien gehören nicht zur neuen Website.

Der Telefonlink wurde an die sichtbare Nummer `+49 (0)6583 – 990 41` angeglichen
(`tel:+49658399041`); zuvor enthielt er eine zusätzliche Null.

## Prüfung der Überarbeitung

Alle drei Seiten bei 320, 768 und 1440 Pixeln im Browser geprüft; keine
horizontalen Überläufe. Startseite zusätzlich bei 390 Pixeln visuell geprüft.
Lokale Verweise, Assets, Abschnittsziele und eindeutige IDs geprüft; Navigation
im Browser betätigt. `git diff --check` ohne Befund.
