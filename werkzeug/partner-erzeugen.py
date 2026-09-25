#!/usr/bin/env python3
"""Schreibt partner.html aus der gemeinsamen Quelle GEMEINSAM/inhalte/partner.json.

Gegenstueck zum gleichnamigen Skript im Repo mi-tool-website: dieselbe Quelle,
dieselben Regeln, das Layout von dlivr.eu. Die Seite bleibt statisch — hier
entsteht fertiges HTML, das committet wird.

Gebaut wird nur, was freigegeben ist; die Regeln stehen in schema.md der Quelle
und sind unten in `baubar()` nachgebildet.

Kopf und Fuss werden nicht abgeschrieben, sondern aus index.html genommen und
fuer eine Unterseite umgeschrieben (`href="#..."` wird `href="index.html#..."`),
so wie impressum.html und datenschutz.html es tragen. Aendert sich die
Navigation der Startseite, zieht der naechste Lauf sie mit.

    python3 werkzeug/partner-erzeugen.py [--quelle PFAD] [--pruefen]
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys

WURZEL = pathlib.Path(__file__).resolve().parents[1]
QUELLE_VORGABE = WURZEL.parents[2] / "GEMEINSAM" / "inhalte" / "partner.json"
ZIEL = WURZEL / "partner.html"
LOGOORDNER = WURZEL / "assets" / "partner"
DIESE_SEITE = "dlivr"

KATEGORIEN = ["IT-Systemhaus", "Beratung", "Automatisierung"]


def baubar(eintrag: dict) -> bool:
    """Die vier Baustopp-Regeln aus schema.md der Quelle."""
    if DIESE_SEITE not in eintrag.get("seiten", []):
        return False
    if eintrag.get("aktiv") is not True:
        return False
    if not (eintrag.get("beschreibung") or "").strip():
        return False
    return True


def quellstand(quelle: pathlib.Path) -> str:
    try:
        hash_ = subprocess.run(
            ["git", "-C", str(quelle.parent), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return "unbekannt"
    return hash_ or "unbekannt"


def teil(text: str, tag: str, klasse: str) -> str:
    treffer = re.search(rf'<{tag} class="{klasse}[^"]*">.*?</{tag}>', text, re.S)
    if not treffer:
        raise SystemExit(f"index.html hat kein <{tag} class=\"{klasse}\"> — Kopf/Fuss nicht zu uebernehmen.")
    return treffer.group(0)


def rahmen() -> tuple[str, str]:
    """Kopf und Fuss aus index.html, auf eine Unterseite umgeschrieben."""
    start = (WURZEL / "index.html").read_text(encoding="utf-8")
    kopf = teil(start, "header", "site-header").replace('href="#', 'href="index.html#')
    # Auf der Startseite markiert aria-current den Punkt "Start"; auf einer
    # Unterseite steht der Nutzer nicht dort.
    kopf = kopf.replace(' aria-current="location"', "")
    fuss = teil(start, "footer", "site-footer").replace('href="#', 'href="index.html#')
    return kopf, fuss


def logo_uebernehmen(eintrag: dict, quelle: pathlib.Path, schreiben: bool) -> tuple[str | None, str | None]:
    """Kopiert die Logodateien aus der Quelle nach assets/partner.

    Zurueck kommen die Pfade fuer helle und dunkle Flaeche. Fehlt die zweite
    Fassung, gilt die erste in beiden Modi; fehlt beides, zeigt die Karte nur
    den Namen — so steht es in schema.md der Quelle.
    """
    pfade: list[str | None] = []
    for feld in ("logo", "logo_dunkelmodus"):
        wert = eintrag.get(feld)
        if not wert:
            pfade.append(None)
            continue
        herkunft = quelle.parent / wert
        if not herkunft.is_file():
            raise SystemExit(f"Logo fehlt in der Quelle: {herkunft}")
        ziel = LOGOORDNER / f"{eintrag['id']}{'-weiss' if feld.endswith('dunkelmodus') else ''}{herkunft.suffix}"
        if schreiben:
            LOGOORDNER.mkdir(parents=True, exist_ok=True)
            if not ziel.is_file() or ziel.read_bytes() != herkunft.read_bytes():
                shutil.copyfile(herkunft, ziel)
        pfade.append(f"assets/partner/{ziel.name}")
    return pfade[0], pfade[1]


def logo_bild(hell: str | None, dunkel: str | None) -> str:
    """Das Logo als ein oder zwei <img>. Der Name steht als Ueberschrift
    daneben, das Logo ist darum fuer Vorlesewerkzeuge schmueckend."""
    if not hell:
        return ""
    if not dunkel:
        return f'<img class="partner-logo" src="{hell}" alt="" aria-hidden="true" loading="lazy" decoding="async">\n'
    return (f'<img class="partner-logo logo-on-light" src="{hell}" alt="" aria-hidden="true" loading="lazy" decoding="async">\n'
            f'<img class="partner-logo logo-on-dark" src="{dunkel}" alt="" aria-hidden="true" loading="lazy" decoding="async">\n')


def karte(eintrag: dict, logos: tuple[str | None, str | None] = (None, None)) -> str:
    name = html.escape(eintrag["name"])
    url = html.escape(eintrag["url"], quote=True)
    text = html.escape(eintrag["beschreibung"])
    kennung = html.escape(eintrag["id"], quote=True)
    fahne = html.escape(eintrag["kategorie"])
    return (
        f'<article class="card service-card" id="partner-{kennung}">\n'
        f"{logo_bild(*logos)}"
        f'<p class="label"><span>{fahne}</span></p>\n'
        f"<h3>{name}</h3>\n"
        f"<p>{text}</p>\n"
        f'<a class="text-link" href="{url}" rel="noopener external">{name} besuchen '
        f'<span aria-hidden="true">&#8599;</span></a>\n'
        "</article>"
    )


def sortiert(liste: list[dict]) -> list[dict]:
    rang = {k: i for i, k in enumerate(KATEGORIEN)}
    return sorted(liste, key=lambda e: (rang.get(e["kategorie"], len(rang)),
                                        e["kategorie"], e.get("sortierung", 0), e["name"]))


def rumpf(liste: list[dict], logos: dict[str, tuple[str | None, str | None]]) -> str:
    if not liste:
        # Leere Seite, kein Abbruch und kein Raten — so steht es in schema.md.
        return (
            '<p class="eyebrow">Partner</p>\n<h1>Partner</h1>\n'
            '<p class="intro">Derzeit ist kein Eintrag freigegeben.</p>\n'
        )
    karten = "\n".join(karte(e, logos.get(e["id"], (None, None))) for e in sortiert(liste))
    return (
        '<p class="eyebrow">Partner</p>\n'
        "<h1>Gemeinsam mehr<br>als allein.</h1>\n"
        '<p class="intro">Manche Vorhaben brauchen mehr als eine Rolle. Mit diesen '
        "Häusern arbeite ich zusammen, wenn Systeme, Beratung oder Automatisierung "
        "über das hinausgehen, was ich selbst abdecke.</p>\n"
        f'<div class="cards services">\n{karten}\n</div>\n'
    )


def seite(daten: dict, stand: str,
          logos: dict[str, tuple[str | None, str | None]]) -> str:
    liste = [e for e in daten.get("partner", []) if baubar(e)]
    kopf, fuss = rahmen()
    beschreibung = ("Die Partner von DLIVR: Systemhaus, Beratung und Automatisierung "
                    "rund um Digitalisierung und Prozesse im Mittelstand.")
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{beschreibung}">
<link rel="canonical" href="https://dlivr.eu/partner.html">
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


def haupt() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__,
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    zerleger.add_argument("--quelle", type=pathlib.Path, default=QUELLE_VORGABE,
                          help=f"partner.json der gemeinsamen Quelle (Vorgabe: {QUELLE_VORGABE})")
    zerleger.add_argument("--pruefen", action="store_true",
                          help="nichts schreiben, nur melden, ob partner.html aktuell ist")
    wahl = zerleger.parse_args()

    if not wahl.quelle.is_file():
        print(f"Quelle fehlt: {wahl.quelle}", file=sys.stderr)
        return 2
    daten = json.loads(wahl.quelle.read_text(encoding="utf-8"))

    gebaut = [e for e in daten.get("partner", []) if baubar(e)]
    uebergangen = [e for e in daten.get("partner", []) if not baubar(e)]
    logos = {e["id"]: logo_uebernehmen(e, wahl.quelle, not wahl.pruefen) for e in gebaut}
    text = seite(daten, quellstand(wahl.quelle), logos)

    if wahl.pruefen:
        alt = ZIEL.read_text(encoding="utf-8") if ZIEL.exists() else ""
        ohne = lambda s: re.sub(r"Commit [0-9a-f]+\)", "Commit -)", s)
        if ohne(alt) == ohne(text):
            print(f"partner.html ist aktuell ({len(gebaut)} Partner).")
            return 0
        print("partner.html weicht von der Quelle ab — Generator laufen lassen.", file=sys.stderr)
        return 1

    ZIEL.write_text(text, encoding="utf-8")
    print(f"partner.html geschrieben: {len(gebaut)} Partner.")
    for eintrag in gebaut:
        hell, dunkel = logos[eintrag["id"]]
        bild = "ohne Logo" if not hell else ("Logo hell und dunkel" if dunkel else "ein Logo")
        print(f"  gebaut      {eintrag['id']:<12} {eintrag['kategorie']:<16} {bild}")
    for eintrag in uebergangen:
        grund = ("nicht fuer diese Seite" if DIESE_SEITE not in eintrag.get("seiten", [])
                 else "nicht freigegeben (aktiv)" if eintrag.get("aktiv") is not True
                 else "ohne Beschreibung")
        print(f"  uebergangen {eintrag['id']:<12} {grund}")
    if not gebaut:
        print("Kein Eintrag freigegeben — die Seite ist leer und gehoert "
              "aus der Navigation genommen.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(haupt())
