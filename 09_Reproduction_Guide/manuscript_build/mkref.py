from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import sys
body=float(sys.argv[1]) if len(sys.argv)>1 else 11
ls=float(sys.argv[2]) if len(sys.argv)>2 else 1.08
d=Document('ref_default.docx')
S={s.name:s for s in d.styles}
for sec in d.sections:
    sec.page_height=Cm(29.7); sec.page_width=Cm(21.0)
    for m in ('left_margin','right_margin','top_margin','bottom_margin'): setattr(sec,m,Cm(2.54))
def setfont(st,size,bold=None,italic=None):
    st.font.name='Times New Roman'; st.font.size=Pt(size); st.font.color.rgb=RGBColor(0,0,0)
    rpr=st.element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=rpr.makeelement(qn('w:rFonts'),{}); rpr.append(rf)
    for a in list(rf.attrib):
        if 'Theme' in a or 'theme' in a: del rf.attrib[a]
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),'Times New Roman')
    if bold is not None: st.font.bold=bold
    if italic is not None: st.font.italic=italic
for name in ['Normal','Body Text','First Paragraph','Block Text','Footnote Text','Caption','Image Caption','Table Caption','Bibliography']:
    st=S[name]; small=name in ('Caption','Image Caption','Table Caption','Footnote Text')
    setfont(st,9.5 if small else body)
    pf=st.paragraph_format; pf.space_before=Pt(0); pf.space_after=Pt(3 if small else 4); pf.line_spacing=1.0 if small else ls
    if name in ('Body Text','First Paragraph','Normal','Image Caption'): pf.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
for name,size in [('Title',15),('Heading 1',12),('Heading 2',11),('Heading 3',11)]:
    st=S[name]; setfont(st,size,bold=True,italic=False)
    st.paragraph_format.space_before=Pt(8 if name!='Title' else 0); st.paragraph_format.space_after=Pt(3)
    st.paragraph_format.keep_with_next=True; st.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
d.save('reference.docx')
d=Document('reference.docx'); S={s.name:s for s in d.styles}
setfont(S['Compact'],9.5); S['Compact'].paragraph_format.space_after=Pt(1); S['Compact'].paragraph_format.line_spacing=1.0
d.save('reference.docx')
