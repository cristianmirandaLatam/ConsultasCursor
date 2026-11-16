from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from lxml import etree
import copy
import sys

OUT = sys.argv[1]
FONT = "Segoe UI"
NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'

WHITE = "FFFFFF"
LAVENDER = "E0E7FF"
SOFT = "C7D2FE"
BLUE_LABEL = "93C5FD"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])
sp_tree = slide.shapes._spTree


def grad_xml(stops, angle=None, path=None):
    gs = "".join(
        f'<a:gs pos="{int(p*1000)}"><a:srgbClr val="{c}"><a:alpha val="{int(a*1000)}"/></a:srgbClr></a:gs>'
        for p, c, a in stops
    )
    if path:
        shade = f'<a:path path="{path}"><a:fillToRect l="50000" t="50000" r="50000" b="50000"/></a:path>'
    else:
        shade = f'<a:lin ang="{int(angle*60000)}" scaled="0"/>'
    return f'<a:gradFill {NS} rotWithShape="1"><a:gsLst>{gs}</a:gsLst>{shade}</a:gradFill>'


def set_fill_xml(shape, fill_xml):
    spPr = shape._element.spPr
    for tag in ("a:solidFill", "a:gradFill", "a:noFill"):
        for el in spPr.findall(qn(tag)):
            spPr.remove(el)
    new = etree.fromstring(fill_xml)
    geom = spPr.find(qn("a:prstGeom"))
    geom.addnext(new)


def set_line(shape, color=None, alpha=100, width=1.0):
    ln = shape.line
    if color is None:
        ln.fill.background()
        return
    ln.width = Pt(width)
    spPr = shape._element.spPr
    ln_el = spPr.find(qn("a:ln"))
    for el in list(ln_el):
        if el.tag in (qn("a:solidFill"), qn("a:noFill")):
            ln_el.remove(el)
    solid = etree.fromstring(
        f'<a:solidFill {NS}><a:srgbClr val="{color}"><a:alpha val="{int(alpha*1000)}"/></a:srgbClr></a:solidFill>'
    )
    ln_el.insert(0, solid)


def add_shape(kind, x, y, w, h, fill_xml=None, line=None, line_alpha=100, line_w=1.0, radius=None):
    shp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = radius
    if fill_xml:
        set_fill_xml(shp, fill_xml)
    set_line(shp, line, line_alpha, line_w)
    return shp


def add_text(x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, italic=False, spacing=None, line_spacing=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        r = p.add_run()
        r.text = t
        f = r.font
        f.name = FONT
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = RGBColor.from_string(color)
        if spacing is not None:
            r._r.get_or_add_rPr().set("spc", str(spacing))
    return tb


def add_card_text(shape, paragraphs):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.32)
    tf.margin_top = Inches(0.3)
    tf.margin_bottom = Inches(0.2)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for i, (text, size, color, bold, space_after) in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(space_after)
        p.line_spacing = 1.15
        r = p.add_run()
        r.text = text
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(color)


# Fondo: degradado índigo -> morado -> tinte rojo (sin negro puro)
bg = slide.background
bg_fill = bg.fill
bg_fill.gradient()
bg_el = slide._element.cSld.bg
bgPr = bg_el.find(qn("p:bgPr"))
for el in list(bgPr):
    if el.tag in (qn("a:gradFill"), qn("a:solidFill"), qn("a:noFill")):
        bgPr.remove(el)
bg_grad = etree.fromstring(grad_xml(
    [(0, "17175A", 100), (48, "2B1B6B", 100), (100, "5A1A5C", 100)], angle=32))
bgPr.insert(0, bg_grad)

# Brillos: magenta/rojo a la derecha, azul arriba a la izquierda
add_shape(MSO_SHAPE.OVAL, 7.4, 2.6, 9.0, 8.0,
          fill_xml=grad_xml([(0, "C2245F", 70), (45, "9D1F6A", 35), (100, "5A1A5C", 0)], path="circle"))
add_shape(MSO_SHAPE.OVAL, -2.6, -2.8, 7.6, 5.6,
          fill_xml=grad_xml([(0, "3F6BFF", 38), (60, "4B3BD6", 12), (100, "2B1B6B", 0)], path="circle"))

# Franja superior
add_shape(MSO_SHAPE.RECTANGLE, 0, 0, 13.333, 0.07,
          fill_xml=grad_xml([(0, "3B82F6", 100), (55, "8B3DFF", 100), (100, "E11D74", 100)], angle=0))

# Encabezado
add_text(0.7, 0.62, 6, 0.3, "AGENTE EVALUADOR", 13, BLUE_LABEL, bold=True, spacing=200)
add_text(0.7, 1.0, 9.5, 1.2, "Analista QA", 66, WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
add_text(0.7, 2.27, 10, 0.6, "La conclusión de cada caso que falló", 26, LAVENDER)

# Tarjetas
cards = [
    ("Solo los fallidos",
     "Después del experimento, toma únicamente los casos que no pasaron.",
     "3B82F6"),
    ("Revisa la evidencia",
     "Conversación, expectativa del caso y definiciones del catálogo.",
     "8B3DFF"),
    ("Entrega la causa",
     "Indica si el problema fue del bot, del caso o de la definición, y propone el ajuste.",
     "E11D74"),
]
card_w = (13.333 - 1.4 - 0.7) / 3
card_y = 3.25
card_h = 2.45
for i, (title, body, accent) in enumerate(cards):
    x = 0.7 + i * (card_w + 0.35)
    card = add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, card_y, card_w, card_h,
                     fill_xml=grad_xml([(0, "221E66", 78), (100, "1A1650", 82)], angle=90),
                     line="7C8CFF", line_alpha=45, line_w=1.0, radius=0.07)
    add_card_text(card, [
        (title, 22, WHITE, True, 10),
        (body, 16, SOFT, False, 0),
    ])
    add_shape(MSO_SHAPE.RECTANGLE, x + 0.32, card_y + 0.0, 0.9, 0.06,
              fill_xml=grad_xml([(0, accent, 100), (100, accent, 100)], angle=0))

# Chips de causas
chips = [
    ("Bot decidió mal", "1E3A8A"),
    ("Usuario simulado se salió", "2A2F8F"),
    ("Caso mal planteado", "3B1F80"),
    ("Definiciones superpuestas", "5B1C7E"),
    ("Faltan datos", "7A1B5E"),
]
chip_y = 6.0
chip_h = 0.5
gap = 0.14
widths = [len(t) * 0.092 + 0.5 for t, _ in chips]
total = sum(widths) + gap * (len(chips) - 1)
x = 0.7
for (text, color), w in zip(chips, widths):
    chip = add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, chip_y, w, chip_h,
                     fill_xml=grad_xml([(0, color, 85), (100, color, 85)], angle=0),
                     line="93C5FD", line_alpha=40, line_w=0.75, radius=0.5)
    tf = chip.text_frame
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor.from_string("DBEAFE")
    x += w + gap

# Pie
add_text(0.7, 6.85, 11.93, 0.4, "No cambia el puntaje. Explica por qué falló.", 18,
         LAVENDER, align=PP_ALIGN.CENTER, italic=False)

prs.save(OUT)
print("saved", OUT)
