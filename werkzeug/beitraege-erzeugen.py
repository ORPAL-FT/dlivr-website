#!/usr/bin/env python3
"""Schreibt beitraege.html aus der gemeinsamen Quelle GEMEINSAM/inhalte/beitraege.json.

Gegenstueck zum gleichnamigen Skript im Repo mi-tool-website: dieselbe Quelle,
dieselben Regeln, das Layout von dlivr.eu. Die Seite bleibt statisch — hier
entsteht fertiges HTML, das committet wird.

Die Seite laedt nichts von LinkedIn nach: kein Einbettungsskript, keine fremde
Grafik. Der Text ist unsere eigene Fassung, die Grafik kommt aus bilder/ der
Quelle und wird beim Lauf nach assets/beitraege kopiert. Der Verweis auf den
Beitrag ist ein gewoehnlicher Link.

Gebaut wird nur, was freigegeben ist; die Regeln stehen in schema.md der Quelle
und sind unten in `baubar()` und `demnaechst()` nachgebildet:

* Ein Beitrag mit `veroeffentlicht_am` erscheint vollstaendig.
* Ein geplanter Beitrag erscheint nur als Datum und Titel unter „Demnaechst“,
  und nur mit `geplant_zeigen: true`.
* Ein geplanter Beitrag mit verstrichenem Termin erscheint nicht und wird
  gemeldet — dann fehlt `veroeffentlicht_am` in der Quelle.

    python3 werkzeug/beitraege-erzeugen.py [--quelle PFAD] [--pruefen]
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys

WURZEL = pathlib.Path(__file__).resolve().parents[1]
QUELLE_VORGABE = WURZEL.parents[2] / "GEMEINSAM" / "inhalte" / "beitraege.json"
ZIEL = WURZEL / "beitraege.html"
BILDORDNER = WURZEL / "assets" / "beitraege"
DIESE_SEITE = "dlivr"

MONATE = ["Januar", "Februar", "Maerz", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]


def heute() -> datetime.date:
    return datetime.date.today()


def datum(wert: str) -> datetime.date:
    return datetime.date.fromisoformat(wert)


def lesbar(wert: str) -> str:
    d = datum(wert)
    return f"{d.day}. {MONATE[d.month - 1]} {d.year}"


def fuer_diese_seite(eintrag: dict) -> bool:
    return DIESE_SEITE in eintrag.get("seiten", [])


def baubar(eintrag: dict) -> bool:
    if not fuer_diese_seite(eintrag):
        return False
    if not eintrag.get("veroeffentlicht_am"):
        return False
    return bool((eintrag.get("text") or "").strip())


def demnaechst(eintrag: dict) -> bool:
    if not fuer_diese_seite(eintrag):
        return False
    if eintrag.get("veroeffentlicht_am"):
        return False
    if eintrag.get("geplant_zeigen") is not True:
        return False
    return datum(eintrag["datum"]) >= heute()


def grund(eintrag: dict) -> str:
    if not fuer_diese_seite(eintrag):
        return "nicht fuer diese Seite"
    if eintrag.get("veroeffentlicht_am"):
        return "veroeffentlicht, aber ohne Text"
    if eintrag.get("geplant_zeigen") is not True:
        return "geplant, nicht freigegeben"
    return "geplant, Termin verstrichen — veroeffentlicht_am fehlt"


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
    start = (WURZEL / "index.html").read_text(encoding="utf-8")
    kopf = teil(start, "header", "site-header").replace('href="#', 'href="index.html#')
    kopf = kopf.replace(' aria-current="location"', "")
    fuss = teil(start, "footer", "site-footer").replace('href="#', 'href="index.html#')
    return kopf, fuss


def bild_uebernehmen(eintrag: dict, quelle: pathlib.Path, schreiben: bool) -> str | None:
    if not eintrag.get("bild"):
        return None
    herkunft = quelle.parent / eintrag["bild"]
    if not herkunft.is_file():
        raise SystemExit(f"Bild fehlt in der Quelle: {herkunft}")
    ziel = BILDORDNER / f"{eintrag['id']}{herkunft.suffix}"
    if schreiben:
        BILDORDNER.mkdir(parents=True, exist_ok=True)
        if not ziel.is_file() or ziel.read_bytes() != herkunft.read_bytes():
            shutil.copyfile(herkunft, ziel)
    return f"assets/beitraege/{ziel.name}"


def absaetze(text: str) -> str:
    teile = [t.strip() for t in re.split(r"\n\s*\n", text.strip()) if t.strip()]
    return "\n".join(f"<p>{html.escape(t).replace(chr(10), '<br>')}</p>" for t in teile)


def karte(eintrag: dict, bildpfad: str | None) -> str:
    kennung = html.escape(eintrag["id"], quote=True)
    titel = html.escape(eintrag["titel"])
    untertitel = html.escape(eintrag.get("untertitel") or "")
    wann = lesbar(eintrag["veroeffentlicht_am"])
    teile = [f'<article class="card" id="beitrag-{kennung}">',
             f'<p class="label"><span>{wann}</span></p>',
             f"<h3>{titel}</h3>"]
    if untertitel:
        teile.append(f"<p><strong>{untertitel}</strong></p>")
    if bildpfad:
        alt = html.escape(eintrag.get("alttext") or titel, quote=True)
        teile.append(f'<img src="{bildpfad}" alt="{alt}" loading="lazy" decoding="async">')
    teile.append(absaetze(eintrag["text"]))
    if eintrag.get("linkedin_url"):
        url = html.escape(eintrag["linkedin_url"], quote=True)
        teile.append(f'<a class="text-link" href="{url}" rel="noopener external">'
                     'Beitrag auf LinkedIn <span aria-hidden="true">&#8599;</span></a>')
    teile.append("</article>")
    return "\n".join(teile)


def vorschau(eintrag: dict) -> str:
    """Ein geplanter Beitrag: Datum und Titel, kein Text, kein Bild."""
    kennung = html.escape(eintrag["id"], quote=True)
    uhr = html.escape(eintrag.get("uhrzeit") or "")
    zeit = f"{lesbar(eintrag['datum'])}, {uhr} Uhr" if uhr else lesbar(eintrag["datum"])
    return (f'<article class="card service-card" id="geplant-{kennung}">\n'
            f'<p class="label"><span>{zeit}</span></p>\n'
            f'<h3>{html.escape(eintrag["titel"])}</h3>\n'
            f'<p>{html.escape(eintrag.get("kampagne") or "")}</p>\n'
            "</article>")


def gruppen(liste: list[dict]) -> list[tuple[str, list[dict]]]:
    reihenfolge: list[str] = []
    for eintrag in liste:
        if eintrag["kampagne"] not in reihenfolge:
            reihenfolge.append(eintrag["kampagne"])
    return [(k, sorted((e for e in liste if e["kampagne"] == k),
                       key=lambda e: (e.get("sortierung", 0), e["datum"])))
            for k in reihenfolge]


def rumpf(gebaut: list[tuple[dict, str | None]], geplant: list[dict]) -> str:
    if not gebaut and not geplant:
        return ('<p class="eyebrow">Beitr&auml;ge</p>\n<h1>Beitr&auml;ge</h1>\n'
                '<p class="intro">Derzeit ist kein Beitrag freigegeben.</p>\n')
    teile = ['<p class="eyebrow">Beitr&auml;ge</p>\n',
             "<h1>Was ich auf<br>LinkedIn schreibe.</h1>\n",
             '<p class="intro">Jeder Beitrag steht hier so, wie er ver&ouml;ffentlicht '
             "wurde. Diese Seite l&auml;dt nichts von LinkedIn nach; wer dort mitlesen "
             "m&ouml;chte, folgt dem Verweis am Beitrag.</p>\n"]
    if gebaut:
        bilder = {e["id"]: p for e, p in gebaut}
        for kampagne, eintraege in gruppen([e for e, _ in gebaut]):
            teile.append(f"<h2>{html.escape(kampagne)}</h2>\n")
            karten = "\n".join(karte(e, bilder[e["id"]]) for e in eintraege)
            teile.append(f'<div class="cards">\n{karten}\n</div>\n')
    if geplant:
        teile.append('<h2 id="demnaechst">Demn&auml;chst</h2>\n')
        teile.append("<p>Diese Beitr&auml;ge sind terminiert. Der Text erscheint hier, "
                     "sobald er auf LinkedIn steht.</p>\n")
        karten = "\n".join(vorschau(e) for e in sorted(geplant, key=lambda e: e["datum"]))
        teile.append(f'<div class="cards services">\n{karten}\n</div>\n')
    return "".join(teile)


def stilblatt() -> str:
    """Den Stilverweis von index.html uebernehmen, samt Fingerprint."""
    start = (WURZEL / "index.html").read_text(encoding="utf-8")
    treffer = re.search(r'<link rel="stylesheet" href="([^"]+)">', start)
    if not treffer:
        raise SystemExit("index.html hat keinen Stilverweis — beitraege.html nicht zu bauen.")
    return treffer.group(1)


def seite(daten: dict, gebaut: list[tuple[dict, str | None]], geplant: list[dict],
          stand: str) -> str:
    kopf, fuss = rahmen()
    beschreibung = ("Die LinkedIn-Beitraege von DLIVR und mi-tool: Archivsuche, "
                    "PDF-Formulare und Digitalisierung im Mittelstand.")
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{beschreibung}">
<link rel="canonical" href="https://dlivr.eu/beitraege.html">
<meta name="theme-color" content="#f4f2ef">
<meta name="color-scheme" content="light dark">
<script src="assets/theme.js?v=20260914-anchor-focus"></script>
<title>Beitr&auml;ge &middot; DLIVR</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{stilblatt()}">
</head>
<body>
<!-- Erzeugt von werkzeug/beitraege-erzeugen.py aus GEMEINSAM/inhalte/beitraege.json
     (Stand {daten.get('stand', 'unbekannt')}, Commit {stand}). Nicht von Hand aendern:
     Text, Bild und Freigabe stehen in der Quelle, nicht hier. -->
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{kopf}

<main id="inhalt" tabindex="0" aria-label="Seiteninhalt">
<section class="section"><div class="wrap">
{rumpf(gebaut, geplant)}</div></section>
</main>

{fuss}

</body>
</html>
"""


def haupt() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__,
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    zerleger.add_argument("--quelle", type=pathlib.Path, default=QUELLE_VORGABE,
                          help=f"beitraege.json der gemeinsamen Quelle (Vorgabe: {QUELLE_VORGABE})")
    zerleger.add_argument("--pruefen", action="store_true",
                          help="nichts schreiben, nur melden, ob beitraege.html aktuell ist")
    wahl = zerleger.parse_args()

    if not wahl.quelle.is_file():
        print(f"Quelle fehlt: {wahl.quelle}", file=sys.stderr)
        return 2
    daten = json.loads(wahl.quelle.read_text(encoding="utf-8"))
    alle = daten.get("beitraege", [])

    schreiben = not wahl.pruefen
    gebaut = [(e, bild_uebernehmen(e, wahl.quelle, schreiben)) for e in alle if baubar(e)]
    gebaut.sort(key=lambda p: (p[0].get("sortierung", 0), p[0]["datum"]))
    geplant = [e for e in alle if demnaechst(e)]
    uebrig = [e for e in alle if not baubar(e) and not demnaechst(e)]

    text = seite(daten, gebaut, geplant, quellstand(wahl.quelle))

    if wahl.pruefen:
        alt = ZIEL.read_text(encoding="utf-8") if ZIEL.exists() else ""
        ohne = lambda s: re.sub(r"Commit [0-9a-f]+\)", "Commit -)", s)
        if ohne(alt) == ohne(text):
            print(f"beitraege.html ist aktuell ({len(gebaut)} veroeffentlicht, "
                  f"{len(geplant)} geplant).")
            return 0
        print("beitraege.html weicht von der Quelle ab — Generator laufen lassen.", file=sys.stderr)
        return 1

    ZIEL.write_text(text, encoding="utf-8")
    print(f"beitraege.html geschrieben: {len(gebaut)} veroeffentlicht, {len(geplant)} geplant.")
    for eintrag, _ in gebaut:
        print(f"  gebaut      {eintrag['id']:<32} {eintrag['veroeffentlicht_am']}")
    for eintrag in geplant:
        print(f"  demnaechst  {eintrag['id']:<32} {eintrag['datum']}")
    for eintrag in uebrig:
        print(f"  uebergangen {eintrag['id']:<32} {grund(eintrag)}")
    verfallen = [e for e in uebrig
                 if fuer_diese_seite(e) and not e.get("veroeffentlicht_am")
                 and e.get("geplant_zeigen") is True and datum(e["datum"]) < heute()]
    if verfallen:
        print(f"{len(verfallen)} Beitrag/Beitraege sind terminiert gewesen und stehen ohne "
              "veroeffentlicht_am da — in der Quelle nachtragen.", file=sys.stderr)
    if not gebaut and not geplant:
        print("Kein Beitrag freigegeben — die Seite ist leer und gehoert aus der "
              "Navigation genommen.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(haupt())
