from pathlib import Path
import json,re
r=Path(__file__).resolve().parents[1];b=json.loads((r/'werkzeug/design/dlivr.json').read_text());css=(r/'css/style.css').read_text();adapter=(r/'werkzeug/design/dlivr-hell.css').read_text()
assert css.startswith(adapter),'Tokenadapter fehlt'
for var,value in re.findall(r'(--[\w-]+):\s*([^;]+);',adapter):
 assert value in b['farben'].values(),(var,value)
assert json.loads((r/'werkzeug/design/basis.json').read_text())['version']=='1.3.1'
print('DLIVR: heller Tokenadapter und Regelbasis 1.3.1 vorhanden.')
