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
assert frei['status']=='freigegeben' and frei['version']=='1.4.1',frei
print(f"DLIVR: heller Tokenadapter passt zum Design-System {frei['version']} ({frei['git_tag']}).")
# Seit 06.10.2026: Impressum und Datenschutz wortgleich mit mi-tool.tech,
# Quelle GEMEINSAM/inhalte/rechtstexte. Abweichung bricht ab.
import subprocess,sys
lauf=subprocess.run([sys.executable,str(r/'werkzeug'/'rechtstexte-erzeugen.py'),'--pruefen'],capture_output=True,text=True)
assert lauf.returncode==0,(lauf.stdout or lauf.stderr).strip()
print(lauf.stdout.strip())
