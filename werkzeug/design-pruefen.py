from pathlib import Path
import json,re
r=Path(__file__).resolve().parents[1]
ds=r.parents[2]/'GEMEINSAM'/'design-system'
assert ds.is_dir(),f'Design-System nicht gefunden: {ds}'
b=json.loads((ds/'tokens'/'marken'/'dlivr.json').read_text())
frei=json.loads((ds/'freigabe.json').read_text())
css=(r/'css/style.css').read_text();adapter=(r/'werkzeug/design/dlivr-hell.css').read_text()
assert css.startswith(adapter),'Tokenadapter fehlt'
for var,value in re.findall(r'(--[\w-]+):\s*([^;]+);',adapter):
 assert value in b['farben'].values(),(var,value)
# 1.4.1 (07.10.2026) aendert nur den dunklen Wert von status.info; DLIVR-Werte unveraendert.
# 1.5.0 (07.10.2026) ergaenzt space.section; 1.6.0 (08.10.2026) nur Logofarben fuer mi-tool.
# DLIVR-Werte in beiden unveraendert; die Wertpruefung oben laeuft gegen den aktuellen Stand.
# 1.7.0/1.7.1 (09.10.2026) ergaenzen terminal.accent und kunde.*; 1.8.0 den DLIVR-Dunkelmodus
# (eigene Datei); 1.9.0 (10.10.2026) nur LCF-Graustufen. Helle DLIVR-Farbwerte unveraendert.
# Seit 13.10.2026 keine feste Versionsnummer mehr: geprueft wird gegen die freigegebene
# Version aus freigabe.json; die Wertpruefung oben bricht ab, wenn sich ein DLIVR-Wert aendert.
assert frei['status']=='freigegeben',frei
print(f"DLIVR: heller Tokenadapter passt zum Design-System {frei['version']} ({frei['git_tag']}).")
# Seit 28.10.2026: Formmaße der Angebotskarten (border.kasten, border.kasten.width,
# radius.kasten) stehen außerhalb des Farbadapters; Name und Wert müssen dem
# DS-Adapter css/dlivr-hell.css entsprechen.
ds_css=dict(re.findall(r'(--[\w-]+):\s*([^;]+);',(ds/'css'/'dlivr-hell.css').read_text()))
for var in ('--border-kasten','--border-kasten-width','--radius-kasten'):
 wert=re.search(re.escape(var)+r':\s*([^;]+);',css)
 assert wert and ds_css.get(var)==wert.group(1).strip(),(var,wert and wert.group(1),ds_css.get(var))
print('DLIVR: Formmaße der Angebotskarten passen zum Design-System-Adapter.')
# Seit 06.10.2026: Impressum und Datenschutz wortgleich mit mi-tool.tech,
# Quelle GEMEINSAM/inhalte/rechtstexte. Abweichung bricht ab.
import subprocess,sys
lauf=subprocess.run([sys.executable,str(r/'werkzeug'/'rechtstexte-erzeugen.py'),'--pruefen'],capture_output=True,text=True)
assert lauf.returncode==0,(lauf.stdout or lauf.stderr).strip()
print(lauf.stdout.strip())
