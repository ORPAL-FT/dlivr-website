#!/usr/bin/env python3
"""Schreibt partner.html aus der gemeinsamen Quelle GEMEINSAM/inhalte/partner.json.

Gegenstueck zum gleichnamigen Skript im Repo mi-tool-website: dieselbe Quelle,
dieselben Regeln, das Layout von dlivr.eu. Die Seite bleibt statisch — hier
entsteht fertiges HTML, das committet wird.

Gebaut wird nur, was freigegeben ist; bei Partnern ist der Schalter `aktiv`.
Die Regeln stehen in schema.md der Quelle und sind in werkzeug/inhalte.py
nachgebildet, das sich diese Datei mit referenzen-erzeugen.py teilt.

Hier steht nur noch das Layout von dlivr.eu: wie eine Karte aussieht, wie die
Seite ueberschrieben ist, welcher Rahmen darum liegt. Quelle lesen, sieben,
schreiben und pruefen macht der gemeinsame Unterbau.

    python3 werkzeug/partner-erzeugen.py [--quelle PFAD] [--pruefen]
"""

from __future__ import annotations

import html

import inhalte
from inhalte import WURZEL

ZIEL = WURZEL / "partner.html"

KATEGORIEN = ["IT-Systemhaus", "Beratung", "Automatisierung"]

BESCHREIBUNG = ("Die Partner von DLIVR: Systemhaus, Beratung und Automatisierung "
                "rund um Digitalisierung und Prozesse im Mittelstand.")


def karte(eintrag: dict, logos: tuple[str | None, str | None] = (None, None)) -> str:
    name = html.escape(eintrag["name"])
    url = html.escape(eintrag["url"], quote=True)
    text = html.escape(eintrag["beschreibung"])
    kennung = html.escape(eintrag["id"], quote=True)
    fahne = html.escape(eintrag["kategorie"])
    return (
        f'<article class="card service-card" id="partner-{kennung}">\n'
        f"{inhalte.logo_bild(*logos)}"
        f'<p class="label"><span>{fahne}</span></p>\n'
        f"<h3>{name}</h3>\n"
        f"<p>{text}</p>\n"
        f'<a class="text-link" href="{url}" rel="noopener external">{name} besuchen '
        f'<span aria-hidden="true">&#8599;</span></a>\n'
        "</article>"
    )


def rumpf(liste: list[dict], logos: dict[str, tuple[str | None, str | None]]) -> str:
    if not liste:
        # Leere Seite, kein Abbruch und kein Raten — so steht es in schema.md.
        return (
            '<p class="eyebrow">Partner</p>\n<h1>Partner</h1>\n'
            '<p class="intro">Derzeit ist kein Eintrag freigegeben.</p>\n'
        )
    karten = "\n".join(karte(e, logos.get(e["id"], (None, None)))
                       for e in inhalte.sortiert(liste, KATEGORIEN))
    return (
        '<p class="eyebrow">Partner</p>\n'
        "<h1>Gemeinsam mehr<br>als allein.</h1>\n"
        '<p class="intro">Manche Vorhaben brauchen mehr als eine Rolle. Mit diesen '
        "Häusern arbeite ich zusammen, wenn Systeme, Beratung oder Automatisierung "
        "über das hinausgehen, was ich selbst abdecke.</p>\n"
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
<link rel="canonical" href="https://dlivr.eu/partner.html">
<meta property="og:title" content="Partner &ndash; DLIVR">
<meta property="og:description" content="{beschreibung}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://dlivr.eu/partner.html">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="DLIVR">
<meta property="og:image" content="https://dlivr.eu/assets/dlivr-link-vorschau-20260925.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DLIVR &ndash; Beratung und Umsetzung f&uuml;r den Mittelstand.">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f2ef">
<meta name="color-scheme" content="light dark">
<script src="assets/theme.js?v=20260914-anchor-focus"></script>
<title>Partner · DLIVR</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/style.css?v=7f5ca38c2ea9">
</head>
<body>
<!-- Erzeugt von werkzeug/partner-erzeugen.py aus GEMEINSAM/inhalte/partner.json
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
    raise SystemExit(inhalte.erzeuge("partner", "aktiv", ZIEL, seite, __doc__))
