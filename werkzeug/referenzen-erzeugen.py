#!/usr/bin/env python3
"""Schreibt referenzen.html aus der gemeinsamen Quelle GEMEINSAM/inhalte/referenzen.json.

Gegenstueck zu partner-erzeugen.py und zum gleichnamigen Skript im Repo
mi-tool-website: dieselbe Quelle, dieselben Regeln, das Layout von dlivr.eu.
Nur der Schalter ist ein anderer. Bei Partnern entscheidet `aktiv`, ob gebaut
wird; bei Referenzen `freigegeben_am` — und das Datum traegt die Freigabe
**des Kunden**, nicht die von Frank. Ohne dieses Datum erscheint ein Kunde
nirgends, auch nicht mit Namen.

Steht kein Eintrag frei, entsteht trotzdem eine Seite: leer, mit einem Satz,
und ohne Eintrag in der Navigation. Der Generator raet nichts und bricht nicht
ab — so steht es in schema.md der Quelle.

    python3 werkzeug/referenzen-erzeugen.py [--quelle PFAD] [--pruefen]

Ein Zitat des Kunden steht hier nicht: dafuer braucht es eine eigene
schriftliche Freigabe, und die Quelle fuehrt kein Feld dafuer. Die Karte zeigt
Name, Leistung, den Satz aus `beschreibung` (er nennt auch den Ort) und,
falls vorhanden, das Logo.
"""

from __future__ import annotations

import html

import inhalte
from inhalte import WURZEL

ZIEL = WURZEL / "referenzen.html"

# Reihenfolge der Gruppen; die Liste steht in schema.md der Quelle.
# Kategorien, die hier fehlen, haengen alphabetisch hinten dran.
KATEGORIEN = ["Autohaus", "Handwerk"]

BESCHREIBUNG = ("Haeuser, die mit DLIVR arbeiten — genannt mit ihrer "
                "ausdruecklichen Zustimmung.")


def karte(eintrag: dict, logos: tuple[str | None, str | None] = (None, None)) -> str:
    name = html.escape(eintrag["name"])
    url = html.escape(eintrag["url"], quote=True)
    leistung = html.escape(eintrag["leistung"])
    text = html.escape(eintrag["beschreibung"])
    kennung = html.escape(eintrag["id"], quote=True)
    fahne = html.escape(eintrag["kategorie"])
    return (
        f'<article class="card service-card" id="referenz-{kennung}">\n'
        f"{inhalte.logo_bild(*logos)}"
        f'<p class="label"><span>{fahne}</span></p>\n'
        f"<h3>{name}</h3>\n"
        f'<p class="service-lead">{leistung}</p>\n'
        f"<p>{text}</p>\n"
        f'<a class="text-link" href="{url}" rel="noopener external">{name} besuchen '
        f'<span aria-hidden="true">&#8599;</span></a>\n'
        "</article>"
    )


def rumpf(liste: list[dict], logos: dict[str, tuple[str | None, str | None]]) -> str:
    if not liste:
        # Leere Seite, kein Abbruch und kein Raten — so steht es in schema.md.
        # Kein Kundenname ohne Freigabedatum, auch nicht als Andeutung.
        return (
            '<p class="eyebrow">Referenzen</p>\n<h1>Referenzen</h1>\n'
            '<p class="intro">Derzeit ist kein Eintrag freigegeben.</p>\n'
        )
    karten = "\n".join(karte(e, logos.get(e["id"], (None, None)))
                       for e in inhalte.sortiert(liste, KATEGORIEN))
    return (
        '<p class="eyebrow">Referenzen</p>\n'
        "<h1>Wo die Arbeit<br>schon steht.</h1>\n"
        '<p class="intro">Diese Häuser arbeiten mit dem, was hier entsteht. Jedes '
        "steht hier, weil es einer Nennung ausdrücklich zugestimmt hat — und nur "
        "mit dem, was es selbst freigegeben hat.</p>\n"
        f'<div class="cards services">\n{karten}\n</div>\n'
    )


def seite(daten: dict, liste: list[dict], stand: str,
          logos: dict[str, tuple[str | None, str | None]]) -> str:
    kopf, fuss = inhalte.rahmen()
    beschreibung = BESCHREIBUNG
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{beschreibung}">
<link rel="canonical" href="https://dlivr.eu/referenzen.html">
<meta name="theme-color" content="#f4f2ef">
<meta name="color-scheme" content="light dark">
<script src="assets/theme.js?v=20260914-anchor-focus"></script>
<title>Referenzen · DLIVR</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/style.css?v=7f5ca38c2ea9">
</head>
<body>
<!-- Erzeugt von werkzeug/referenzen-erzeugen.py aus GEMEINSAM/inhalte/referenzen.json
     (Stand {daten.get('stand', 'unbekannt')}, Commit {stand}). Nicht von Hand aendern:
     Text und Freigabe stehen in der Quelle, nicht hier. -->
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{kopf}

<main id="inhalt" tabindex="0" aria-label="Seiteninhalt">
<section class="section"><div class="wrap">
{rumpf(liste, logos)}</div></section>
</main>

{fuss}

</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(inhalte.erzeuge("referenzen", "freigegeben_am", ZIEL, seite, __doc__))
