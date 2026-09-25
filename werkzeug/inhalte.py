#!/usr/bin/env python3
"""Gemeinsamer Unterbau der Seiten aus GEMEINSAM/inhalte.

partner.html und referenzen.html kommen aus derselben Quelle, tragen dieselben
Baustopp-Regeln und werden auf demselben Weg erzeugt. Alles, was beide gleich
machen, steht hier; in den beiden Generatoren bleibt nur, was das Layout der
Seite betrifft. So koennen Partner und Referenzen nicht auseinanderlaufen:
wer eine Regel aendert, aendert sie fuer beide.

Gegenstueck zur gleichnamigen Datei im Repo mi-tool-website. Der Inhalt ist
bis auf Wurzel, Seitenkennung und die beiden Logoklassen derselbe; getrennt
bleibt er, weil jede Webseite ihr Repo allein auscheckt.

Nicht enthalten ist beitraege-erzeugen.py. Die Beitragsseite hat eigene
Regeln (`veroeffentlicht_am`, `geplant_zeigen`, verstrichene Termine) und
bleibt vorerst fuer sich; sie kann spaeter nachziehen.

Kein eigenständiges Skript — wird von partner-erzeugen.py und
referenzen-erzeugen.py eingebunden.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Callable

WURZEL = pathlib.Path(__file__).resolve().parents[1]
QUELLORDNER = WURZEL.parents[2] / "GEMEINSAM" / "inhalte"
LOGOORDNER = WURZEL / "assets" / "partner"
DIESE_SEITE = "dlivr"


def baubar(eintrag: dict, schalter: str) -> bool:
    """Die Baustopp-Regeln aus schema.md der Quelle.

    `schalter` ist das Feld, das die Freigabe traegt: bei Partnern `aktiv`
    (muss `True` sein), bei Referenzen `freigegeben_am` (muss ein Datum
    tragen). Alles andere gilt fuer beide gleich.
    """
    if DIESE_SEITE not in eintrag.get("seiten", []):
        return False
    if not freigegeben(eintrag, schalter):
        return False
    if not (eintrag.get("beschreibung") or "").strip():
        return False
    return True


def freigegeben(eintrag: dict, schalter: str) -> bool:
    wert = eintrag.get(schalter)
    if schalter == "aktiv":
        return wert is True
    return bool((wert or "").strip())


def uebergangen_grund(eintrag: dict, schalter: str) -> str:
    """Warum ein Eintrag nicht gebaut wurde — in der Reihenfolge der Regeln."""
    if DIESE_SEITE not in eintrag.get("seiten", []):
        return "nicht fuer diese Seite"
    if not freigegeben(eintrag, schalter):
        return f"nicht freigegeben ({schalter})"
    return "ohne Beschreibung"


def quellstand(quelle: pathlib.Path) -> str:
    """Commit der Quelle, damit der Wochencheck beide Webseiten vergleichen kann."""
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
    """Kopf und Fuss aus index.html, auf eine Unterseite umgeschrieben.

    Nicht abgeschrieben, sondern uebernommen (`href="#..."` wird
    `href="index.html#..."`), so wie impressum.html und datenschutz.html es
    tragen. Aendert sich die Navigation der Startseite, zieht der naechste
    Lauf sie mit.
    """
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


def sortiert(liste: list[dict], reihenfolge: list[str]) -> list[dict]:
    """Nach Kategorie und Sortierung. Kategorien, die in `reihenfolge` fehlen,
    haengen hinten dran — alphabetisch, damit die Ausgabe nicht von der
    Dateireihenfolge abhaengt."""
    rang = {k: i for i, k in enumerate(reihenfolge)}
    return sorted(liste, key=lambda e: (rang.get(e["kategorie"], len(rang)),
                                        e["kategorie"], e.get("sortierung", 0), e["name"]))


def erzeuge(schluessel: str, schalter: str, ziel: pathlib.Path,
            seite: Callable[[dict, list[dict], str, dict], str],
            beschreibung: str) -> int:
    """Der gemeinsame Ablauf: Quelle lesen, sieben, bauen, schreiben oder pruefen.

    `seite` bekommt die Rohdaten, die baubaren Eintraege, den Quellcommit und
    die Logopfade und liefert die fertige Seite. Nur diese Funktion kennt das
    Layout; alles davor und danach ist fuer Partner und Referenzen gleich.
    """
    vorgabe = QUELLORDNER / f"{schluessel}.json"
    zerleger = argparse.ArgumentParser(description=beschreibung,
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    zerleger.add_argument("--quelle", type=pathlib.Path, default=vorgabe,
                          help=f"{schluessel}.json der gemeinsamen Quelle (Vorgabe: {vorgabe})")
    zerleger.add_argument("--pruefen", action="store_true",
                          help=f"nichts schreiben, nur melden, ob {ziel.name} aktuell ist")
    wahl = zerleger.parse_args()

    if not wahl.quelle.is_file():
        print(f"Quelle fehlt: {wahl.quelle}", file=sys.stderr)
        return 2
    daten = json.loads(wahl.quelle.read_text(encoding="utf-8"))

    alle = daten.get(schluessel, [])
    gebaut = [e for e in alle if baubar(e, schalter)]
    uebergangen = [e for e in alle if not baubar(e, schalter)]
    logos = {e["id"]: logo_uebernehmen(e, wahl.quelle, not wahl.pruefen) for e in gebaut}
    text = seite(daten, gebaut, quellstand(wahl.quelle), logos)

    if wahl.pruefen:
        alt = ziel.read_text(encoding="utf-8") if ziel.exists() else ""
        # Der Quellcommit wechselt bei jedem Commit der Quelle; er allein ist
        # kein Grund, die Seite als veraltet zu melden.
        ohne = lambda s: re.sub(r"Commit [0-9a-f]+\)", "Commit -)", s)
        if ohne(alt) == ohne(text):
            print(f"{ziel.name} ist aktuell ({len(gebaut)} {schluessel.capitalize()}).")
            return 0
        print(f"{ziel.name} weicht von der Quelle ab — Generator laufen lassen.", file=sys.stderr)
        return 1

    ziel.write_text(text, encoding="utf-8")
    print(f"{ziel.name} geschrieben: {len(gebaut)} {schluessel.capitalize()}.")
    for eintrag in gebaut:
        hell, dunkel = logos[eintrag["id"]]
        bild = "ohne Logo" if not hell else ("Logo hell und dunkel" if dunkel else "ein Logo")
        print(f"  gebaut      {eintrag['id']:<12} {eintrag['kategorie']:<16} {bild}")
    for eintrag in uebergangen:
        print(f"  uebergangen {eintrag['id']:<12} {uebergangen_grund(eintrag, schalter)}")
    if not gebaut:
        print("Kein Eintrag freigegeben — die Seite ist leer und gehoert "
              "aus der Navigation genommen.", file=sys.stderr)
    return 0
