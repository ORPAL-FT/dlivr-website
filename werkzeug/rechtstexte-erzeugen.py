#!/usr/bin/env python3
"""Setzt Impressum und Datenschutz aus GEMEINSAM/inhalte/rechtstexte ein.

Beide Websites (mi-tool.tech und dlivr.eu) tragen seit dem 06.10.2026
wortgleiche Rechtstexte. Der Text steht nur in der Quelle; hier wird er
zwischen die Marken RECHTSTEXT:ANFANG und RECHTSTEXT:ENDE der jeweiligen Seite
geschrieben. Kopf, Fuss und Layout bleiben, wie sie sind. Einziger Platzhalter
in der Quelle ist {{angaben}}, die CSS-Klasse der Angabenlisten dieser Seite.

Dasselbe Skript liegt in beiden Website-Repos; es unterscheidet sich nur in
ANGABEN_KLASSE.

    python3 werkzeug/rechtstexte-erzeugen.py [--quelle PFAD] [--pruefen]

`--pruefen` schreibt nichts und endet mit 1, wenn eine Seite von der Quelle
abweicht. design-pruefen.py ruft das bei jedem Lauf auf.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parents[1]
QUELLE = WURZEL.parents[2] / "GEMEINSAM" / "inhalte" / "rechtstexte"
SEITEN = ["impressum", "datenschutz"]
ANGABEN_KLASSE = "contact-details"

ANFANG = "<!-- RECHTSTEXT:ANFANG"
ENDE = "<!-- RECHTSTEXT:ENDE -->"
BEREICH = re.compile(re.escape(ANFANG) + r".*?" + re.escape(ENDE), re.S)


def baustein(quelle: pathlib.Path, name: str) -> str:
    text = (quelle / f"{name}.html").read_text(encoding="utf-8").strip()
    text = text.replace("{{angaben}}", ANGABEN_KLASSE)
    rest = re.findall(r"\{\{[^}]*\}\}", text)
    if rest:
        raise SystemExit(f"{name}.html: unbekannte Platzhalter {sorted(set(rest))}")
    return (f"{ANFANG} aus GEMEINSAM/inhalte/rechtstexte/{name}.html, nicht von Hand "
            f"aendern; neu schreiben mit werkzeug/rechtstexte-erzeugen.py -->\n"
            f"{text}\n{ENDE}")


def main() -> int:
    teile = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    teile.add_argument("--quelle", type=pathlib.Path, default=QUELLE)
    teile.add_argument("--pruefen", action="store_true")
    args = teile.parse_args()

    if not args.quelle.is_dir():
        print(f"Quelle fehlt: {args.quelle}", file=sys.stderr)
        return 1

    abweichend = []
    for name in SEITEN:
        ziel = WURZEL / f"{name}.html"
        alt = ziel.read_text(encoding="utf-8")
        if len(BEREICH.findall(alt)) != 1:
            print(f"{ziel.name}: Marken RECHTSTEXT:ANFANG/ENDE fehlen oder doppelt",
                  file=sys.stderr)
            return 1
        neu = BEREICH.sub(lambda _: baustein(args.quelle, name), alt)
        if neu == alt:
            continue
        abweichend.append(ziel.name)
        if not args.pruefen:
            ziel.write_text(neu, encoding="utf-8")

    if args.pruefen:
        if abweichend:
            print("Weicht von der gemeinsamen Quelle ab: " + ", ".join(abweichend))
            return 1
        print("Rechtstexte gleich der gemeinsamen Quelle.")
        return 0
    print("Geschrieben: " + (", ".join(abweichend) or "nichts, schon aktuell"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
