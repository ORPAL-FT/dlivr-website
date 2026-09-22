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
assert frei['status']=='freigegeben' and frei['version']=='1.3.1',frei
print(f"DLIVR: heller Tokenadapter passt zum Design-System {frei['version']} ({frei['git_tag']}).")
