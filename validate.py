"""Check the committed website without needing the private source snapshot."""
from pathlib import Path
from html.parser import HTMLParser
import json
ROOT=Path(__file__).resolve().parent/'dist'
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k not in ('href','src') or not v or v.startswith(('https:','http:','#','data:')): continue
   assert not v.startswith('/'),f'Absolute asset path breaks repository Pages: {v}'
   assert (ROOT/v).is_file(),f'Missing asset: {v}'
Links().feed((ROOT/'index.html').read_text())
s=(ROOT/'data.js').read_text();assert s.startswith('window.ATLAS=')
packed={}
for prefix in '0123456789abcdef':
 text=(ROOT/('logos-'+prefix+'.js')).read_text(); packed.update(json.loads(text.split('||{},',1)[1][:-2]))
a=json.loads(s[len('window.ATLAS='):-1]);ids={m['annotation3'] for m in a['motifs']};assert len(ids)==len(a['motifs'])
totals={k:0 for k in ids}
for row in a['counts']:
 assert row['motif_name'] in ids
 assert row['count']>=0
 totals[row['motif_name']]+=row['count']
for m in a['motifs']:
 assert m['total_instances']==totals[m['annotation3']]
 for k in ['logo (fwd)','logo (rev)','reference_logo0','hdma_logo0']:
  if m.get(k):
   import base64
   assert base64.b64decode(packed[m[k]].split(',',1)[1],validate=True).startswith(b'\x89PNG\r\n\x1a\n')
print(f'OK: {len(ids)} motifs, {len(a["counts"])} subtype records, all totals and local assets validated.')
