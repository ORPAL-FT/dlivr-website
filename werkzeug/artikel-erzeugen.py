#!/usr/bin/env python3
"""Schreibt artikel.html und je Artikel artikel-<id>.html aus
GEMEINSAM/inhalte/artikel.json.

Gegenstueck zu werkzeug/artikel-erzeugen.py in mi-tool-website (07.10.2026,
Plan B „Musterbetrieb“), mit dem Layout dieser Seite: die Textseiten-Klassen
`legal-page`/`legal` wie Impressum und Datenschutz, Partnerkarten wie auf
partner.html. Dieselben Artikel stehen auf beiden Webseiten; `kanonische_seite`
im Kopf der Quelle sagt, welche Fassung das Original ist (Stand 07.10.2026:
mi-tool). Diese Seite verweist dann mit `canonical` dorthin. Die Anker der
Zwischentitel (`#station-1` …, `#fazit`) sind auf beiden Seiten gleich.

Baustopp-Regeln wie in schema.md der Quelle: `"dlivr"` in `seiten`,
`freigegeben_am` traegt ein Datum, die Textdatei ist vorhanden und nicht leer.

    python3 werkzeug/artikel-erzeugen.py [--quelle PFAD] [--pruefen]

Der Text kennt bewusst nur wenig Markdown: Absaetze, `## ` Zwischentitel,
Listen mit `- `, `**fett**`, `*kursiv*` und Links `[Text](Adresse)`. Alles
andere wird als Text ausgegeben.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys

import inhalte
from inhalte import WURZEL, DIESE_SEITE, rahmen, quellstand

UEBERSICHT = WURZEL / "artikel.html"
QUELLE_VORGABE = inhalte.QUELLORDNER / "artikel.json"
ADRESSEN = {"dlivr": "https://dlivr.eu/", "mi-tool": "https://mi-tool.tech/"}

BESCHREIBUNG = ("Artikel von Frank Töpfer zu Aftersales, papierloser "
                "Werkstatt und Digitalisierung im Mittelstand.")

KENNUNG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERWEIS = re.compile(r"\[([^\]]+)\]\(((?:https://|mailto:|#|[a-z0-9-]+\.html)[^)\s]*)\)")
BETONT = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*")


def uebergangen_grund(eintrag: dict, quelle: pathlib.Path) -> str | None:
    if DIESE_SEITE not in eintrag.get("seiten", []):
        return "nicht fuer diese Seite"
    if not (eintrag.get("freigegeben_am") or "").strip():
        return "nicht freigegeben (freigegeben_am)"
    datei = quelle.parent / (eintrag.get("text_datei") or "")
    if not eintrag.get("text_datei") or not datei.is_file():
        return f"Textdatei fehlt: {eintrag.get('text_datei')}"
    if not datei.read_text(encoding="utf-8").strip():
        return "Textdatei leer"
    return None


def kennungen_pruefen(alle: list[dict]) -> None:
    gesehen: set[str] = set()
    for eintrag in alle:
        kennung = eintrag.get("id") or ""
        if not KENNUNG.match(kennung):
            raise SystemExit(f"Ungueltige id in artikel.json: {kennung!r} (erlaubt: a-z, 0-9, -)")
        if kennung in gesehen:
            raise SystemExit(f"Doppelte id in artikel.json: {kennung}")
        gesehen.add(kennung)


def betont(text: str) -> str:
    teile, letzte = [], 0
    for treffer in BETONT.finditer(text):
        teile.append(html.escape(text[letzte:treffer.start()]))
        if treffer.group(1) is not None:
            teile.append(f"<strong>{html.escape(treffer.group(1))}</strong>")
        else:
            teile.append(f"<em>{html.escape(treffer.group(2))}</em>")
        letzte = treffer.end()
    teile.append(html.escape(text[letzte:]))
    return "".join(teile)


def zeile(text: str) -> str:
    teile, letzte = [], 0
    for treffer in VERWEIS.finditer(text):
        teile.append(betont(text[letzte:treffer.start()]))
        ziel = html.escape(treffer.group(2), quote=True)
        extern = ' rel="noopener external"' if ziel.startswith("https://") else ""
        teile.append(f'<a href="{ziel}"{extern}>{betont(treffer.group(1))}</a>')
        letzte = treffer.end()
    teile.append(betont(text[letzte:]))
    return "".join(teile)


def anker(titel: str, vergeben: set[str]) -> str:
    """Gleiche Regel wie in mi-tool-website, damit `#station-2` auf beiden
    Seiten denselben Abschnitt trifft."""
    nummer = re.match(r"^(\d+)\.\s", titel)
    if nummer:
        basis = f"station-{nummer.group(1)}"
    else:
        erstes = re.split(r"[\s:–—-]+", titel.strip())[0].lower()
        erstes = erstes.translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}))
        basis = re.sub(r"[^a-z0-9]+", "-", erstes).strip("-") or "abschnitt"
    kennung, n = basis, 2
    while kennung in vergeben:
        kennung, n = f"{basis}-{n}", n + 1
    vergeben.add(kennung)
    return kennung


def text_html(text: str) -> str:
    bloecke, vergeben = [], set()
    for block in re.split(r"\n\s*\n", text.strip()):
        zeilen = [z.strip() for z in block.strip().splitlines() if z.strip()]
        if not zeilen:
            continue
        if len(zeilen) == 1 and zeilen[0].startswith("## "):
            titel = zeilen[0][3:].strip()
            bloecke.append(f'<h2 id="{anker(titel, vergeben)}">{zeile(titel)}</h2>')
        elif all(z.startswith("- ") for z in zeilen):
            punkte = "".join(f"<li>{zeile(z[2:])}</li>" for z in zeilen)
            bloecke.append(f"<ul>{punkte}</ul>")
        else:
            bloecke.append(f"<p>{zeile(' '.join(zeilen))}</p>")
    return "\n".join(bloecke)


def partnerkarten(eintrag: dict, partner: dict[str, dict], logos: dict) -> str:
    """Die genannten Partner als Karten wie auf partner.html. Der Artikel nennt
    sie ohnehin; `aktiv` gilt fuer partner.html, nicht hier."""
    karten = []
    for kennung in eintrag.get("partner") or []:
        p = partner.get(kennung)
        if not p:
            continue
        name = html.escape(p["name"])
        url = html.escape(p["url"], quote=True)
        karten.append(
            '<article class="card service-card">\n'
            f"{inhalte.logo_bild(*logos.get(kennung, (None, None)))}"
            f"<h3>{name}</h3>\n<p>{html.escape(p['beschreibung'])}</p>\n"
            f'<a class="text-link" href="{url}" rel="noopener external">{name} besuchen '
            '<span aria-hidden="true">&#8599;</span></a>\n</article>'
        )
    if not karten:
        return ""
    return ('<section class="section"><div class="wrap">\n'
            '<div class="section-heading"><h2 id="partner">Die genannten Partner</h2></div>\n'
            f'<div class="cards">\n{chr(10).join(karten)}\n</div>\n'
            "</div></section>\n")


def stilblatt() -> str:
    start = (WURZEL / "index.html").read_text(encoding="utf-8")
    treffer = re.search(r'<link rel="stylesheet" href="([^"]+)">', start)
    if not treffer:
        raise SystemExit("index.html hat keinen Stilverweis — Artikelseiten nicht zu bauen.")
    return treffer.group(1)


def kanonisch(daten: dict, pfad: str) -> str:
    original = daten.get("kanonische_seite") or DIESE_SEITE
    zeile_ = f'<link rel="canonical" href="{ADRESSEN.get(original, ADRESSEN[DIESE_SEITE])}{pfad}">'
    if original == DIESE_SEITE:
        return zeile_
    return (zeile_ + "\n<!-- Dieselben Artikel stehen auf mi-tool.tech. Dort liegt laut\n"
            "     kanonische_seite in GEMEINSAM/inhalte/artikel.json das Original. -->")


def kopfdaten(daten: dict, titel: str, beschreibung: str, pfad: str, art: str) -> str:
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{beschreibung}">
{kanonisch(daten, pfad)}
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschreibung}">
<meta property="og:type" content="{art}">
<meta property="og:url" content="https://dlivr.eu/{pfad}">
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
<title>{titel} &middot; DLIVR</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{stilblatt()}">
</head>
<body>
<!-- Erzeugt von werkzeug/artikel-erzeugen.py aus GEMEINSAM/inhalte/artikel.json
     (Stand {daten.get('stand', 'unbekannt')}, Commit {{stand}}). Nicht von Hand aendern:
     Text und Freigabe stehen in der Quelle, nicht hier. -->
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
"""


def datum_lang(iso: str) -> str:
    j, m, t = iso.split("-")
    monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
              "August", "September", "Oktober", "November", "Dezember"]
    return f"{int(t)}. {monate[int(m) - 1]} {j}"


def einzelseite(daten: dict, eintrag: dict, text: str, stand: str,
                partner: dict[str, dict], logos: dict) -> str:
    kopf, fuss = rahmen()
    titel = html.escape(eintrag["titel"])
    untertitel = (f'<p class="intro">{betont(eintrag["untertitel"])}</p>\n'
                  if (eintrag.get("untertitel") or "").strip() else "")
    datum = eintrag["freigegeben_am"]
    pfad = f"artikel-{eintrag['id']}.html"
    return (kopfdaten(daten, titel, html.escape(eintrag["beschreibung"], quote=True), pfad, "article")
            .replace("{stand}", stand) + f"""{kopf}

<main id="inhalt" tabindex="0" aria-label="Seiteninhalt">
<section class="section legal-page"><div class="wrap legal">
<p class="eyebrow"><a href="artikel.html">Artikel</a></p>
<h1>{titel}</h1>
{untertitel}<article>
{text_html(text)}
<p><em>{html.escape(eintrag['autor'])}</em> · <time datetime="{datum}">{datum_lang(datum)}</time></p>
</article>
<p><a href="artikel.html">Alle Artikel</a></p>
</div></section>
{partnerkarten(eintrag, partner, logos)}</main>

{fuss}

</body>
</html>
""")


def uebersicht(daten: dict, liste: list[dict], stand: str) -> str:
    kopf, fuss = rahmen()
    if liste:
        karten = "\n".join(
            f'<article class="card service-card" id="artikel-{html.escape(e["id"], quote=True)}">\n'
            f'<p class="label"><span>{html.escape(e["autor"])} · '
            f'<time datetime="{e["freigegeben_am"]}">{datum_lang(e["freigegeben_am"])}</time></span></p>\n'
            f"<h3>{html.escape(e['titel'])}</h3>\n<p>{html.escape(e['beschreibung'])}</p>\n"
            f'<a class="text-link" href="artikel-{html.escape(e["id"], quote=True)}.html">Artikel lesen '
            '<span aria-hidden="true">&rarr;</span></a>\n</article>'
            for e in liste)
        rumpf = f'<div class="cards services">\n{karten}\n</div>\n'
    else:
        rumpf = '<p class="intro">Derzeit ist kein Artikel freigegeben.</p>\n'
    return (kopfdaten(daten, "Artikel", html.escape(BESCHREIBUNG, quote=True), "artikel.html", "website")
            .replace("{stand}", stand) + f"""{kopf}

<main id="inhalt" tabindex="0" aria-label="Seiteninhalt">
<section class="section"><div class="wrap">
<p class="eyebrow">Artikel</p>
<h1>Aus der Praxis.</h1>
<p class="intro">Längere Texte darüber, wie Werkzeuge im Aftersales zusammenspielen
und wo Digitalisierung im Betrieb wirklich ansetzt.</p>
{rumpf}</div></section>
</main>

{fuss}

</body>
</html>
""")


def haupt() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__,
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    zerleger.add_argument("--quelle", type=pathlib.Path, default=QUELLE_VORGABE,
                          help=f"artikel.json der gemeinsamen Quelle (Vorgabe: {QUELLE_VORGABE})")
    zerleger.add_argument("--pruefen", action="store_true",
                          help="nichts schreiben, nur melden, ob die Artikelseiten aktuell sind")
    wahl = zerleger.parse_args()

    if not wahl.quelle.is_file():
        print(f"Quelle fehlt: {wahl.quelle}", file=sys.stderr)
        return 2
    daten = json.loads(wahl.quelle.read_text(encoding="utf-8"))
    stand = quellstand(wahl.quelle)
    partnerdatei = wahl.quelle.parent / "partner.json"
    partner = ({p["id"]: p for p in json.loads(partnerdatei.read_text(encoding="utf-8")).get("partner", [])}
               if partnerdatei.is_file() else {})

    alle = sorted(daten.get("artikel", []), key=lambda e: (e.get("sortierung", 0), e["id"]))
    kennungen_pruefen(alle)
    gebaut = [e for e in alle if uebergangen_grund(e, wahl.quelle) is None]
    uebergangen = [e for e in alle if uebergangen_grund(e, wahl.quelle) is not None]

    for eintrag in gebaut:
        for kennung in eintrag.get("partner") or []:
            if kennung not in partner:
                print(f"  Partner {kennung!r} aus artikel {eintrag['id']} fehlt in partner.json",
                      file=sys.stderr)
    genannte = {k for e in gebaut for k in (e.get("partner") or []) if k in partner}
    logos = {k: inhalte.logo_uebernehmen(partner[k], partnerdatei, not wahl.pruefen) for k in genannte}

    soll: dict[pathlib.Path, str] = {UEBERSICHT: uebersicht(daten, gebaut, stand)}
    for eintrag in gebaut:
        text = (wahl.quelle.parent / eintrag["text_datei"]).read_text(encoding="utf-8")
        soll[WURZEL / f"artikel-{eintrag['id']}.html"] = einzelseite(daten, eintrag, text, stand, partner, logos)
    veraltet = [p for p in WURZEL.glob("artikel-*.html") if p not in soll]

    if wahl.pruefen:
        ohne = lambda s: re.sub(r"Commit [0-9a-f-]+\)", "Commit -)", s)
        abweichend = [p.name for p, t in soll.items()
                      if not p.exists() or ohne(p.read_text(encoding="utf-8")) != ohne(t)]
        abweichend += [f"{p.name} (nicht mehr baubar)" for p in veraltet]
        if not abweichend:
            print(f"Artikelseiten sind aktuell ({len(gebaut)} Artikel).")
            return 0
        print("Weicht von der Quelle ab — Generator laufen lassen: " + ", ".join(abweichend), file=sys.stderr)
        return 1

    for pfad, text in soll.items():
        pfad.write_text(text, encoding="utf-8")
    for pfad in veraltet:
        pfad.unlink()
    print(f"artikel.html geschrieben: {len(gebaut)} Artikel.")
    for eintrag in gebaut:
        print(f"  gebaut      artikel-{eintrag['id']}.html")
    for eintrag in uebergangen:
        print(f"  uebergangen {eintrag['id']:<20} {uebergangen_grund(eintrag, wahl.quelle)}")
    for pfad in veraltet:
        print(f"  entfernt    {pfad.name}")
    if not gebaut:
        print("Kein Artikel freigegeben — artikel.html ist leer und gehoert "
              "aus Navigation und Sitemap.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(haupt())
