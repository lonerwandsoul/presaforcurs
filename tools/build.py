# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import Canvas, W, H, SCALE, ROOT
from slides import SLIDES
from pptx import Presentation
from pptx.util import Emu
from deck import EMU

OUT_PPTX = os.path.join(ROOT, "Презентация_Аналитика_ФАВОРИТ.pptx")
OUT_PREV = os.path.join(ROOT, "previews")


def render_pngs(only=None):
    os.makedirs(OUT_PREV, exist_ok=True)
    for i, fn in enumerate(SLIDES, 1):
        if only and i not in only:
            continue
        img = Image.new("RGBA", (W * SCALE, H * SCALE), (255, 255, 255, 255))
        d = Canvas("pil", img=img, draw=ImageDraw.Draw(img))
        fn(d)
        img.convert("RGB").resize((W * 2, H * 2), Image.LANCZOS).save(
            os.path.join(OUT_PREV, f"slide-{i:02d}.png"))
        print("png", i)


def render_pptx():
    prs = Presentation()
    prs.slide_width = Emu(W * EMU)
    prs.slide_height = Emu(H * EMU)
    blank = prs.slide_layouts[6]
    for fn in SLIDES:
        slide = prs.slides.add_slide(blank)
        # белый фон по умолчанию
        c = Canvas("pptx", slide=slide)
        fn(c)
    prs.save(OUT_PPTX)
    print("saved", OUT_PPTX)


if __name__ == "__main__":
    only = None
    if len(sys.argv) > 1:
        only = {int(a) for a in sys.argv[1:] if a.isdigit()}
    render_pngs(only)
    if only is None:
        render_pptx()


# --------------------------------------------------------------- заметки
def add_notes():
    from pptx import Presentation
    from speech import NOTES
    prs = Presentation(OUT_PPTX)
    for i, slide in enumerate(prs.slides, 1):
        if i in NOTES:
            slide.notes_slide.notes_text_frame.text = NOTES[i]
    prs.save(OUT_PPTX)
    print("notes added")


# ----------------------------------------------------------------- речь
def speech_md():
    from speech import SPEECH, TITLE, QA, TIPS
    words = [len(s[3].split()) for s in SPEECH]
    all_words = sum(words)
    rate = all_words / 285.0          # слов в секунду (доклад ≈ 4 мин 45 с)
    total = int(all_words / rate)
    lines = [f"# Доклад на защиту курсовой работы", "",
             f"**Тема:** {TITLE}", "",
             "**ПМ.05 Проектирование и разработка информационных систем** · "
             "специальность 09.02.07 · группа 44 СПО", "",
             "**Докладчик:** Семиглазов Данил Вячеславович  ",
             "**Руководитель:** Колесникова С.Н., преподаватель высшей квалификационной категории",
             "", f"**Хронометраж:** 12–15 слайдов, доклад 4–5 минут "
                 f"(по методическим указаниям). Ориентировочное время речи — "
                 f"{total // 60} мин {total % 60:02d} с при темпе ~120 слов/мин.", "",
             "---", "", "## Текст доклада", ""]

    t = 0
    for i, (tag, name, secs, text) in enumerate(SPEECH):
        w = words[i]
        dur = int(round(w / rate))
        mm, ss = divmod(t, 60)
        t2 = t + dur
        mm2, ss2 = divmod(t2, 60)
        lines += [f"### {name}",
                  f"*{mm}:{ss:02d}–{mm2}:{ss2:02d} · {w} слов · ≈{dur} с*", "",
                  f"> {text}", ""]
        t = t2

    lines += ["---", "", "## Ответы на вероятные вопросы комиссии", ""]
    for q, a in QA:
        lines += [f"**{q}**", "", a, ""]

    lines += ["---", "", "## Чек-лист перед защитой", ""]
    lines += [f"- [ ] {t}" for t in TIPS]
    lines += ["", "---", "",
              "## План демонстрации системы (если попросят показать)", "",
              "| Шаг | Что открыть | Что сказать |", "|---|---|---|",
              "| 1 | Дашборд | Четыре KPI считаются из базы, прогноз выручки — линейный тренд |",
              "| 2 | Заказы | Портфель и статусы; сменить статус прямо в таблице |",
              "| 3 | Производство | Выпуск по цехам, брак, загрузка; добавить запись |",
              "| 4 | Качество | Потери по причинам, диаграмма Парето |",
              "| 5 | Финансы | Выручка, себестоимость, прибыль, рентабельность |",
              "| 6 | Отчёты | Сводная таблица, CSV, журнал действий |", ""]
    open(os.path.join(ROOT, "Речь_на_защиту.md"), "w", encoding="utf-8").write("\n".join(lines))
    print("speech md ok")


def speech_docx():
    import docx
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from speech import SPEECH, TITLE, QA, TIPS

    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(14)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.first_line_indent = Cm(1.25)
    st.paragraph_format.space_after = Pt(0)
    for s in doc.sections:
        s.left_margin = Cm(3); s.right_margin = Cm(1.5)
        s.top_margin = Cm(2); s.bottom_margin = Cm(2)

    def h(text, size=16, center=False, space_before=12, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(size)
        r.font.name = "Times New Roman"
        return p

    def body(text, italic=False, indent=True, size=14):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if not indent:
            p.paragraph_format.first_line_indent = Cm(0)
        r = p.add_run(text)
        r.italic = italic
        r.font.size = Pt(size)
        r.font.name = "Times New Roman"
        return p

    h("ДОКЛАД НА ЗАЩИТУ КУРСОВОЙ РАБОТЫ", 16, center=True, space_before=0)
    h(TITLE, 15, center=True, space_after=10)
    body("ПМ.05 Проектирование и разработка информационных систем. "
         "Специальность 09.02.07 Информационные системы и программирование",
         indent=False, size=12)
    body("Выполнил: Семиглазов Данил Вячеславович, группа 44 СПО. "
         "Руководитель: Колесникова С.Н.", indent=False, size=12)
    body("Презентация: 15 слайдов, доклад 4–5 минут (по методическим указаниям).",
         indent=False, size=12)

    h("ТЕКСТ ДОКЛАДА", 16, space_before=18)
    for tag, name, secs, text in SPEECH:
        h(f"{name}  ({tag})", 14, space_before=12, space_after=4)
        body(text)

    doc.add_page_break()
    h("ОТВЕТЫ НА ВОПРОСЫ КОМИССИИ", 16, space_before=0)
    for q, a in QA:
        p = body(q, indent=False)
        p.runs[0].bold = True
        body(a)

    doc.add_page_break()
    h("ЧЕК-ЛИСТ ПЕРЕД ЗАЩИТОЙ", 16, space_before=0)
    for t in TIPS:
        body("☐  " + t, indent=False)

    h("ПЛАН ДЕМОНСТРАЦИИ СИСТЕМЫ", 16, space_before=18)
    plan = [("Дашборд", "Четыре KPI считаются из базы, прогноз выручки — линейный тренд"),
            ("Заказы", "Портфель и статусы, смена статуса прямо в таблице"),
            ("Производство", "Выпуск по цехам, брак, загрузка, добавление записи"),
            ("Качество", "Потери по причинам, диаграмма Парето"),
            ("Финансы", "Выручка, себестоимость, прибыль, рентабельность"),
            ("Отчёты", "Сводная таблица, CSV, журнал действий")]
    for i, (a, b) in enumerate(plan, 1):
        body(f"{i}. {a} — {b}.", indent=False, size=13)

    doc.save(os.path.join(ROOT, "Речь_на_защиту.docx"))
    print("speech docx ok")


if __name__ == "__main__" and os.environ.get("FULL"):
    add_notes(); speech_md(); speech_docx()
