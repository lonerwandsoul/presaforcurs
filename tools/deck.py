# -*- coding: utf-8 -*-
"""
Дизайн-движок презентации: один и тот же layout рисуется
в PNG (для предпросмотра) и в PPTX (итоговый файл).

Единицы: 1280 x 720 "u"; 1 u = 9525 EMU = 0.75 pt.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

W, H = 1280, 720
EMU = 9525
SCALE = 2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- палитра
INK      = "0B1524"
NAVY     = "0E1B2E"
NAVY2    = "16263D"
BLUE     = "2F6BFF"
BLUE_D   = "1D4ED8"
TEAL     = "0FAF9B"
AMBER    = "E8A33D"
RED      = "E05252"
WHITE    = "FFFFFF"
LIGHT    = "F4F6FA"
CARD     = "FFFFFF"
TXT      = "14202F"
MUTED    = "6C7C92"
LINE     = "DFE5EE"
SOFT     = "EEF2F9"

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PPT_FONT = "Segoe UI"

_font_cache = {}


def _pil_font(size_px, bold=False):
    key = (int(size_px), bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG, int(size_px))
    return _font_cache[key]


def measure(txt, size, bold=False):
    """ширина строки в u"""
    f = _pil_font(size * SCALE, bold)
    return f.getlength(txt) / SCALE


def wrap(text, size, width, bold=False):
    """перенос по словам, возвращает список строк"""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if measure(trial, size, bold) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def _rgb(hexs):
    return RGBColor.from_string(hexs)


class Canvas:
    def __init__(self, mode, slide=None, img=None, draw=None):
        self.mode = mode
        self.slide = slide
        self.img = img
        self.d = draw

    # ------------------------------------------------------------ фигуры
    def rect(self, x, y, w, h, fill=None, radius=0, alpha=None,
             line=None, line_w=1.0, shadow=False, dash=None):
        if self.mode == "pil":
            x0, y0, x1, y1 = [int(v * SCALE) for v in (x, y, x + w, y + h)]
            r = int(radius * SCALE)
            layer = Image.new("RGBA", (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            f = None
            if fill:
                f = tuple(int(fill[i:i + 2], 16) for i in (0, 2, 4)) + (
                    int(255 * alpha) if alpha is not None else 255,)
            ln = tuple(int(line[i:i + 2], 16) for i in (0, 2, 4)) if line else None
            ld.rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius=r,
                                 fill=f, outline=ln,
                                 width=max(1, int(line_w * SCALE)))
            if shadow:
                sh = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
                sd = ImageDraw.Draw(sh)
                sd.rounded_rectangle([x0 + int(3 * SCALE), y0 + int(6 * SCALE),
                                      x1 + int(3 * SCALE), y1 + int(9 * SCALE)],
                                     radius=r, fill=(11, 21, 36, 26))
                sh = sh.filter(ImageFilter.GaussianBlur(int(7 * SCALE)))
                self.img.alpha_composite(sh)
            self.img.alpha_composite(layer, (x0, y0))
            return
        # ---- pptx
        shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
        shp = self.slide.shapes.add_shape(shape_type, Emu(int(x * EMU)), Emu(int(y * EMU)),
                                          Emu(int(w * EMU)), Emu(int(h * EMU)))
        if radius:
            try:
                shp.adjustments[0] = min(0.5, radius / min(w, h))
            except Exception:
                pass
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = _rgb(fill)
            if alpha is not None:
                srgb = shp.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
                a = etree.SubElement(srgb, qn("a:alpha"))
                a.set("val", str(int(alpha * 100000)))
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = _rgb(line)
            shp.line.width = Pt(line_w * 0.75)
            if dash:
                from pptx.enum.dml import MSO_LINE_DASH_STYLE
                shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        else:
            shp.line.fill.background()
        if shadow:
            spPr = shp._element.spPr
            eff = etree.SubElement(spPr, qn("a:effectLst"))
            sh = etree.SubElement(eff, qn("a:outerShdw"))
            sh.set("blurRad", str(int(16 * EMU)))
            sh.set("dist", str(int(5 * EMU)))
            sh.set("dir", "5400000")
            sh.set("algn", "ctr")
            sh.set("rotWithShape", "0")
            clr = etree.SubElement(sh, qn("a:srgbClr"))
            clr.set("val", "0B1524")
            al = etree.SubElement(clr, qn("a:alpha"))
            al.set("val", "11000")
        shp.text_frame.word_wrap = True
        return shp

    def circle(self, cx, cy, r, fill=None, alpha=None, line=None, line_w=1.0):
        self.rect(cx - r, cy - r, 2 * r, 2 * r, fill, radius=r, alpha=alpha,
                  line=line, line_w=line_w)

    def line(self, x1, y1, x2, y2, color=LINE, width=1.0, dash=False):
        if self.mode == "pil":
            c = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            if dash:
                self._dashed(x1, y1, x2, y2, c, int(width * SCALE))
            else:
                self.d.line([x1 * SCALE, y1 * SCALE, x2 * SCALE, y2 * SCALE],
                            fill=c, width=max(1, int(width * SCALE)))
            return
        from pptx.enum.shapes import MSO_CONNECTOR
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        con = self.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                              Emu(int(x1 * EMU)), Emu(int(y1 * EMU)),
                                              Emu(int(x2 * EMU)), Emu(int(y2 * EMU)))
        con.line.color.rgb = _rgb(color)
        con.line.width = Pt(width * 0.75)
        if dash:
            con.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        return con

    def _dashed(self, x1, y1, x2, y2, color, width, dash=8, gap=6):
        import math
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        n = dist / (dash + gap)
        for i in range(int(n) + 1):
            t0 = (i * (dash + gap)) / dist
            t1 = min(1, (i * (dash + gap) + dash) / dist)
            if t0 >= 1:
                break
            self.d.line([x1 + dx * t0, y1 + dy * t0, x1 + dx * t1, y1 + dy * t1],
                        fill=color, width=width)

    def arrow(self, x1, y1, x2, y2, color=MUTED, width=1.6, head=7):
        self.line(x1, y1, x2, y2, color, width)
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        for s in (0.5, -0.5):
            ax = x2 - head * math.cos(ang - s)
            ay = y2 - head * math.sin(ang - s)
            self.line(x2, y2, ax, ay, color, width)

    # ------------------------------------------------------------- текст
    def text(self, x, y, w, txt, size=18, color=TXT, bold=False, align="left",
             lh=1.24, max_w=None, upper=False, opacity=None, anchor="top",
             italic=False):
        width = max_w if max_w else w
        content = txt.upper() if upper else txt
        text_color = color
        if opacity is not None:
            # смешиваем с подложкой визуально только в PIL
            pass
        lines = wrap(content, size, width, bold)
        if self.mode == "pil":
            c = tuple(int(text_color[i:i + 2], 16) for i in (0, 2, 4))
            if opacity is not None:
                c = c + (int(255 * opacity),)
            f = _pil_font(size * SCALE, bold)
            step = size * lh
            block_h = step * len(lines)
            yy = y
            if anchor == "middle":
                yy = y - block_h / 2 + step * 0.12
            for i, ln in enumerate(lines):
                lw = f.getlength(ln) / SCALE
                xx = x
                if align == "center":
                    xx = x + (width - lw) / 2
                elif align == "right":
                    xx = x + width - lw
                self.d.text((xx * SCALE, (yy + i * step) * SCALE), ln,
                            font=f, fill=c, anchor="la")
            return block_h

        # pptx
        box_h = size * lh * len(lines) / 0.75 + 4
        tb = self.slide.shapes.add_textbox(Emu(int(x * EMU)), Emu(int(y * EMU)),
                                           Emu(int(width * EMU)), Emu(int(box_h * EMU)))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.margin_left = 0; tf.margin_right = 0
        tf.margin_top = 0; tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                       "right": PP_ALIGN.RIGHT}[align]
        p.line_spacing = lh
        for i, ln in enumerate(lines):
            run = p.add_run()
            run.text = ln
            run.font.size = Pt(size * 0.75)
            run.font.bold = bold
            run.font.italic = italic
            run.font.name = PPT_FONT
            run.font.color.rgb = _rgb(text_color)
            if i != len(lines) - 1:
                p.add_line_break()
        return size * lh * len(lines)

    # ------------------------------------------------------------ картинка
    def image(self, path, x, y, w, h=None, radius=0, crop=None, border=None):
        path = os.path.join(ROOT, path) if not os.path.isabs(path) else path
        if self.mode == "pil":
            im = Image.open(path).convert("RGBA")
            if crop:
                l, t, r, b = crop
                im = im.crop((int(l * im.width), int(t * im.height),
                              int(r * im.width), int(b * im.height)))
            tw, th = int(w * SCALE), int((h if h else w * im.height / im.width) * SCALE)
            im = im.resize((tw, th), Image.LANCZOS)
            if radius:
                mask = Image.new("L", (tw, th), 0)
                ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=int(radius * SCALE), fill=255)
                im.putalpha(mask)
            self.img.alpha_composite(im, (int(x * SCALE), int(y * SCALE)))
            return
        pic = self.slide.shapes.add_picture(path, Emu(int(x * EMU)), Emu(int(y * EMU)),
                                            Emu(int(w * EMU)),
                                            Emu(int((h if h else w) * EMU)) if h else None)
        if crop:
            l, t, r, b = crop
            pic.crop_left, pic.crop_top, pic.crop_right, pic.crop_bottom = l, t, r, b
        if radius:
            # скругление маской через picture fill не поддерживается — оставляем прямоугольник
            pass
        if border:
            pic.line.color.rgb = _rgb(border)
            pic.line.width = Pt(0.75)

    # ------------------------------------------------------- фон слайда
    def bg(self, color=WHITE):
        self.rect(0, 0, W, H, fill=color)

    def gradient_bg(self, c1, c2, angle="diag"):
        if self.mode == "pil":
            base = Image.new("RGB", (int(W * SCALE), int(H * SCALE)), tuple(int(c1[i:i + 2], 16) for i in (0, 2, 4)))
            top = Image.new("RGB", (int(W * SCALE), int(H * SCALE)), tuple(int(c2[i:i + 2], 16) for i in (0, 2, 4)))
            mask = Image.new("L", (int(W * SCALE), int(H * SCALE)))
            md = ImageDraw.Draw(mask)
            for i in range(int(W * SCALE)):
                md.line([(i, 0), (i, int(H * SCALE))], fill=int(255 * min(1, i / (W * SCALE) * 1.15)))
            base = Image.composite(top, base, mask)
            self.img.paste(base, (0, 0))
            return
        shp = self.slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Emu(W * EMU), Emu(H * EMU))
        shp.line.fill.background()
        shp.fill.gradient()
        shp.fill.gradient_angle = 315
        stops = shp.fill.gradient_stops
        stops[0].color.rgb = _rgb(c1)
        stops[0].position = 0.0
        stops[1].color.rgb = _rgb(c2)
        stops[1].position = 1.0


# ------------------------------------------------------------------ helpers
def eyebrow(d, x, y, text, color=BLUE, size=12):
    d.rect(x, y + 1, 26, 3, fill=color)
    d.text(x + 38, y - 5, 800, text, size=size, color=color, bold=True, upper=True)


def footer(d, num, dark=False, label="Аналитика эффективности ООО «ФАВОРИТ» · курсовая работа"):
    col = "8FA0B8" if dark else "9AA8BC"
    d.text(80, 674, 800, label, size=10.5, color=col)
    d.text(1120, 668, 80, f"{num:02d}", size=17, color=col, bold=True, align="right")


def slide_frame(d, num, eyebrow_txt, title, subtitle=None, dark=False, title_size=40, sub_w=980):
    d.bg(NAVY if dark else LIGHT)
    eyebrow(d, 80, 62, eyebrow_txt, BLUE if not dark else "6E9BFF")
    d.text(80, 88, 1120, title, size=title_size, color=WHITE if dark else TXT, bold=True, lh=1.14)
    yy = 88 + title_size * 1.14 * len(wrap(title, title_size, 1120, True)) + 10
    if subtitle:
        d.text(80, yy, sub_w, subtitle, size=15.5, color="9DB0C8" if dark else MUTED, lh=1.35)
    footer(d, num, dark=dark)


def card(d, x, y, w, h, radius=14, fill=CARD, shadow=True, line=None):
    return d.rect(x, y, w, h, fill=fill, radius=radius, shadow=shadow, line=line)
