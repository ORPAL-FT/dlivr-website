# dlivr-website

⚠️ **Dieses Repo liefert dlivr.eu nicht aus.** Das ist die wichtigste Angabe hier,
und sie war bis zum 01.09.2026 nirgends festgehalten.

## Der Befund

Die GitHub-Pages-Konfiguration dieses Repos zeigt auf `dlivr.eu` und der Bau läuft
durch. Ausgeliefert wird die Domain aber von **nginx**, nicht von GitHub Pages —
vermutlich vom Hostinger-Webhosting. Nachweis am 01.09.2026:

| | |
|---|---|
| `https://dlivr.eu/` | HTTP 200, `server: nginx` |
| `https://dlivr.eu/css/style.css` | **HTTP 404** — obwohl die Datei hier liegt |
| Pages-Bau | `built`, Commit `f32d15e` |

Es sind **zwei verschiedene Seiten**:

| | in diesem Repo | live unter dlivr.eu |
|---|---|---|
| Aufbau | `index.html`, `leistungen.html`, `kontakt.html` + `css/style.css` | eine Datei, Styles inline |
| Titel | — | „DLIVR · Frank Töpfer" |
| Schriften | System-Stack | Bebas Neue, Syne, Inter (Google Fonts) |
| Akzent | `#2f8f6f` (seit 01.09.2026) | `#c0392b` Rot |

## `live-abzug/`

Weil die Live-Seite **weder in einem Repo noch lokal auf der Platte** existiert,
liegt hier ein Abzug: `live-abzug/dlivr-eu_2026-09-01.html`, geholt mit `curl` von
der laufenden Seite.

Er ist eigenständig — alle Styles inline, keine lokalen Assets. Nach außen
verweist er nur auf Google Fonts und auf Kontaktziele (LinkedIn, Mail, Telefon).

**Der Abzug ist eine Sicherung, keine Quelle.** Wer die Live-Seite ändert, ändert
sie dort, wo sie tatsächlich liegt — der Abzug veraltet ab dem Moment, in dem das
geschieht. Er existiert, damit die Seite nicht verloren ist, wenn das Hosting
ausfällt oder jemand sie überschreibt.

## Was noch zu klären ist

- **Wo liegt die Quelle wirklich?** Vermutlich Hostinger-Webhosting; über das
  hPanel festzustellen.
- **Welche Seite soll gelten?** Die hier im Repo ist eine ältere Generation. Wenn
  die Live-Seite die richtige ist, gehört sie hierher — und die alte ins Archiv.
- **Welche Farbe führt DLIVR?** Die Layout-Vorgabe (Skill `dlivr-layout`, Wiki
  `corporate-design`) nennt Grün `#2f8f6f`. Die Live-Seite führt Rot `#c0392b`.
  Solange das nicht entschieden ist, widersprechen sich Vorgabe und Außenauftritt.

## Kleinigkeit im Abzug

Auf der Live-Seite steht eine Telefonnummer mit Leerzeichen:
`tel:+4965839904 1`. Sieht nach einem Tippfehler aus — in einem `tel:`-Link kann
das dazu führen, dass die Wahl abbricht.
