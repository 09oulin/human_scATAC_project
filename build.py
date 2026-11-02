"""Build a portable static motif atlas from the original HTML and reconciled TSVs."""
import re,json,csv,base64,hashlib,shutil
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parent
src=ROOT/'source';out=ROOT/'dist';(out/'logos').mkdir(parents=True,exist_ok=True)
s=(src/'motif_table_0927_final.html').read_text()
meta=json.JSONDecoder().raw_decode(s.split('const _META = ',1)[1])[0]
rows=json.loads(re.search(r'<script type="application/json" class="rc">(.*?)</script>',s,re.S)[1])
def read(n):return list(csv.DictReader((src/(n+'.tsv')).open(),delimiter='\t'))
summary={r['motif_name']:r for r in read('motif_summary')}
counts=read('motif_counts_by_subtype'); cells=read('celltype_summary');by=defaultdict(list)
for r in counts:
 r['count']=int(r['count']);by[r['motif_name']].append(r)
assert len(rows)==len(summary)==461
assert len({r['annotation3'] for r in rows})==len(rows)
clean=[]
for r in rows:
 key=r['annotation3'];assert key in summary
 total=int(summary[key]['total_instances']);assert sum(x['count'] for x in by[key])==total,(key,total)
 item={k:v for k,v in r.items() if not meta['image_column'][meta['columns'].index(k)]}
 for field in ['logo (fwd)','logo (rev)','reference_logo0','hdma_logo0']:
  v=r.get(field,'')
  if not v:continue
  if '<img' in v:
   v=re.search('src=[\"\']([^\"\']+)',v)[1]
  v=v.split('base64,')[-1];data=base64.b64decode(v,validate=True);assert data[:8]==b'\x89PNG\r\n\x1a\n'
  name=hashlib.sha256(data).hexdigest()[:20]+'.png';(out/'logos'/name).write_bytes(data);item[field]='logos/'+name
 item.update(total_instances=total,category=summary[key]['category'],n_subtypes=len({x['subtype'] for x in by[key]}))
 item['motif_string']=re.sub('<[^>]+>',' / ',item['motif_string']);clean.append(item)
(out/'data.js').write_text('window.ATLAS='+json.dumps({'motifs':clean,'counts':counts,'cells':cells},ensure_ascii=False,separators=(',',':'))+';')
(out/'downloads').mkdir(exist_ok=True)
for p in src.glob('*.tsv'):shutil.copy2(p,out/'downloads'/p.name)
fields=[k for k in clean[0] if k not in ['logo (fwd)','logo (rev)','reference_logo0','hdma_logo0']]
with (out/'downloads'/'motif_annotations.tsv').open('w') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(clean)
print(f'Validated {len(clean)} unique motifs; {len(counts)} subtype records; all totals reconcile. Instances: {sum(r["total_instances"] for r in clean):,}')

# Pack PNGs into sixteen deduplicated JS assets for portable GitHub uploads.
for prefix in '0123456789abcdef':
 packed={'logos/'+p.name:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() for p in sorted((out/'logos').glob(prefix+'*.png'))}
 (out/('logos-'+prefix+'.js')).write_text('window.MOTIF_LOGOS=Object.assign(window.MOTIF_LOGOS||{},'+json.dumps(packed,separators=(',',':'))+');')
