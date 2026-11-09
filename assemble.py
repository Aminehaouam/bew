import re, os, sys, json, tempfile
from pypdf import PdfReader, PdfWriter
from letter import build
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'base.pdf')
def slug(name):
    n=name.lower()
    n=re.sub(r'\b(gmbh|co\.? ?kg|kg|ag|mbh|e\.k\.|ohg|se|ug|und|&)\b','',n)
    n=n.replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    n=re.sub(r'[^a-z0-9]+','_',n).strip('_')
    return n
def make(firm, outdir):
    tmp=os.path.join(outdir,'_p2.pdf')
    build(tmp, firm['addr'], firm['date'], firm['betreff'], firm['anrede'], firm['p1'], firm.get('beruf'))
    base=PdfReader(BASE); new=PdfReader(tmp)
    w=PdfWriter()
    for i,p in enumerate(base.pages):
        w.add_page(new.pages[0] if i==1 else p)
    fn=f"Amine_Haouam_Ausbildung_Elektroniker_{firm.get('file') or slug(firm['name'])}.pdf"
    with open(os.path.join(outdir,fn),'wb') as f: w.write(f)
    os.remove(tmp); return fn
if __name__=='__main__':
    firms=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
    for f in firms: print(make(f,out))
