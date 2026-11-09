import sys, io, os
HERE=os.path.dirname(os.path.abspath(__file__))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
pdfmetrics.registerFont(TTFont('C',os.path.join(HERE,'fonts','Carlito-Regular.ttf')))
pdfmetrics.registerFont(TTFont('CB',os.path.join(HERE,'fonts','Carlito-Bold.ttf')))
W,H=595.3,841.9; L=85.08; R=510.3
def sigimg():
    a=Image.open(os.path.join(HERE,'sig-000.png')).convert('RGB'); m=Image.open(os.path.join(HERE,'sig-001.png'))
    a.putalpha(m); return ImageReader(a)
def wrap(t,font,size,width):
    out=[];cur=''
    for w in t.replace('Online-','Online- ').split(' '):
        c=(cur+(''if cur.endswith('Online-') else ' ')+w).strip()
        if pdfmetrics.stringWidth(c,font,size)<=width: cur=c
        else: out.append(cur);cur=w
    out.append(cur);return out
P2=("Während meines Bachelorstudiums der Elektrotechnik habe ich Grundkenntnisse in elektrischen Systemen und Anlagen erworben, die ich während mehrerer Praktika bei SONELGAZ, dem nationalen Energieversorger Algeriens, praktisch anwenden und vertiefen konnte. Dabei ist mir bewusst geworden, wie wichtig ein korrekter Verteileraufbau, die richtige Reihenfolge der Schutzgeräte und eine saubere Stromkreisbeschriftung sind. Die Arbeit im Team während dieser Praktika hat mir besonders gefallen, weil ich viel von erfahrenen Kollegen lernen konnte und meine Pünktlichkeit sowie die sorgfältige Umsetzung von Anweisungen geschätzt wurden.")
P3=("In der Ausbildung reizt mich vor allem die praktische Seite des Berufs: wie man elektrische Anlagen installiert, prüft und Fehler behebt. Aus all diesen Gründen möchte ich meine Ausbildung bei Ihnen absolvieren, denn die Tätigkeit als Elektroniker für Energie- und Gebäudetechnik entspricht genau meinem beruflichen Ziel, und ich möchte mich langfristig bei Ihnen engagieren.")
P4="Vielen Dank für die Berücksichtigung meiner Bewerbung. Ich freue mich auf ein Online-Vorstellungsgespräch."
def build(path, addr, date, betreff, anrede, p1, beruf=None):
    global P3
    P3x=P3.replace('Elektroniker für Energie- und Gebäudetechnik',beruf) if beruf else P3
    c=canvas.Canvas(path,pagesize=(W,H))
    def base(top,size): return H-top-size*0.95  # top = bbox yMin approx
    def line(x,top,t,font='C',size=11,right=False):
        y=H-(top+11.52)
        c.setFont(font,size)
        (c.drawRightString if right else c.drawString)(R if right else x,y,t)
    for i,t in enumerate(["Amine Haouam","Cite elzouhour 1","12017 Tebessa","Algerien"]): line(0,70.07+13.44*i,t,right=True)
    for i,t in enumerate(addr): line(L,137.15+13.44*i,t)
    line(0,190.9,"Tebessa, "+date,right=True)
    y=238.77
    for t in wrap(betreff,'CB',14,R-L): line(L,y+2.25,t,'CB',14); y+=17.04
    ytop=y+ (293.63-238.77-2*17.04)
    line(L,ytop,anrede.strip()); y=ytop+32
    for para in (p1,P2,P3x,P4):
        for t in wrap(para,'C',11,R-L+0.5): line(L,y,t); y+=12
        y+=20
    # closing
    y-=20
    line(L,y+20.04,"Mit freundlichen Grüßen")
    c.drawImage(sigimg(),L+7.53,H-(y+20.04+14+29.1)+5.56,86.7,29.1,mask='auto')
    c.save()
if __name__=='__main__':
    build('/tmp/w/test.pdf',["Axalta Coating Systems Germany GmbH & Co. KG","Personalabteilung","Christbusch 25","42285 Wuppertal"],"10.11.2026",
     "Bewerbung um eine Ausbildung zum Elektroniker für Energie- und Gebäudetechnik (m/w/d)","Sehr geehrte Damen und Herren,\n\n",
     "bei Ihnen spricht mich besonders an, dass Sie mit Ihren elektrischen Isoliermaterialien auch für den Energiemarkt arbeiten, deshalb möchte ich meine Ausbildung zum Elektroniker für Energie- und Gebäudetechnik gern in Ihrem Unternehmen machen. In einem Industrieunternehmen mit so vielen technischen Anlagen kann ich viel Praxis sammeln. Der Beruf verbindet Technik mit praktischer Arbeit, und genau das suche ich.")
