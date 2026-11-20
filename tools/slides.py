# -*- coding: utf-8 -*-
"""Сборка презентации: 15 слайдов, 16:9."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import (Canvas, W, H, ROOT, INK, NAVY, NAVY2, BLUE, BLUE_D, TEAL, AMBER,
                  RED, WHITE, LIGHT, CARD, TXT, MUTED, LINE, SOFT, eyebrow,
                  slide_frame, card, wrap, measure, footer)

SCREENS = "assets/screens/"
SHOT_CROP = (0.177, 0.0, 1.0, 1.0)   # отрезаем тёмное меню слева

# ------------------------------------------------------------------ данные
TITLE = "Аналитика эффективности предприятия ООО «ФАВОРИТ»"


# ================================================================== слайды
def s01_title(d):
    d.gradient_bg(NAVY, "12233C")
    # декоративная геометрия
    d.circle(1180, 60, 260, fill="2F6BFF", alpha=0.10)
    d.circle(1240, 640, 180, fill="0FAF9B", alpha=0.08)
    for i in range(9):
        d.line(860 + i * 46, 0, 860 + i * 46, 720, color="1E3350", width=0.8)

    # логотип-марка
    d.rect(80, 58, 46, 46, fill=BLUE, radius=10)
    d.text(80, 70, 46, "Ф", size=22, color=WHITE, bold=True, align="center")
    d.text(140, 66, 420, "СМП «ФАВОРИТ ДИВАН»", size=13, color=WHITE, bold=True, upper=True)
    d.text(140, 86, 420, "мебельная фабрика полного цикла", size=12, color="8FA6C4")

    eyebrow(d, 80, 168, "Курсовая работа · ПМ.05 · 09.02.07", "7FA6FF")

    d.text(80, 196, 660, "Аналитика\nэффективности", size=46, color=WHITE, bold=True, lh=1.13)
    d.text(80, 314, 660, "предприятия", size=46, color="6E9BFF", bold=True, lh=1.13)
    d.rect(80, 382, 74, 4, fill=AMBER)
    d.text(80, 404, 610,
           "Веб-система для фабрики «Фаворит»: производство, качество, финансы, "
           "продажи и кадры — в одном контуре с автоматическими выводами и прогнозом.",
           size=15.5, color="B9C8DA", lh=1.45)

    # скриншот
    d.rect(742, 128, 500, 400, fill="0A1424", radius=16, alpha=0.55)
    d.image(SCREENS + "01_dashboard.png", 728, 114, 500, 383,
            radius=12, crop=SHOT_CROP, border="2B4364")
    d.text(728, 514, 500, "Скриншот интерфейса · главная страница (дашборд) · октябрь 2025",
           size=11, color="8FA6C4")

    # автор
    d.line(80, 596, 1200, 596, color="24405F", width=1)
    d.text(80, 616, 340, "Выполнил", size=11, color="7C93B0", upper=True, bold=True)
    d.text(80, 634, 420, "Семиглазов Данил Вячеславович", size=16, color=WHITE, bold=True)
    d.text(80, 658, 420, "группа 44 СПО · IV курс", size=12.5, color="8FA6C4")

    d.text(560, 616, 300, "Руководитель", size=11, color="7C93B0", upper=True, bold=True)
    d.text(560, 634, 380, "Колесникова С.Н.", size=16, color=WHITE, bold=True)
    d.text(560, 658, 380, "преподаватель высшей категории", size=12.5, color="8FA6C4")

    d.text(980, 616, 220, "2026", size=11, color="7C93B0", upper=True, bold=True, align="right")
    d.text(900, 634, 300, "ГБПОУ РО «КТСиА»", size=13.5, color=WHITE, bold=True, align="right")
    d.text(900, 656, 300, "г. Каменск-Шахтинский", size=12, color="8FA6C4", align="right")


def s02_problem(d):
    d.bg(NAVY)
    slide_frame(d, 2, "Актуальность", "Данные есть — системы нет",
                "Отчётность собирается вручную из разных источников — решения принимаются с задержкой",
                dark=True, sub_w=980)

    items = [
        ("01", "Данные разбросаны", "Выпуск и брак — на бумаге в цехах, продажи — в Excel, кадры — в отдельных файлах.", BLUE),
        ("02", "Отчёты вручную", "До двух рабочих дней в месяц на сборку сводки, цифры между собой не сходятся.", AMBER),
        ("03", "Нет оперативной картины", "Загрузка мощностей и рост брака видны только после закрытия месяца.", TEAL),
        ("04", "Решения «на глаз»", "Прибыль и рентабельность считаются приблизительно, по разным методикам.", RED),
    ]
    y = 230
    for num, ttl, txt, col in items:
        d.rect(80, y, 640, 92, fill="16283F", radius=12)
        d.rect(80, y, 4, 92, fill=col, radius=2)
        d.text(104, y + 20, 40, num, size=20, color=col, bold=True)
        d.text(160, y + 18, 520, ttl, size=17, color=WHITE, bold=True)
        d.text(160, y + 44, 530, txt, size=13, color="A9BAD0", lh=1.32)
        y += 104

    # правая колонка — цифры
    d.rect(760, 230, 440, 200, fill="0F2038", radius=14, line="26415F")
    d.text(792, 252, 380, "Подготовка одного отчёта", size=12.5, color="8FA6C4", upper=True, bold=True)
    d.text(792, 276, 380, "до 2 дней", size=52, color=WHITE, bold=True)
    d.text(792, 350, 380, "вручную, с переносом цифр из Excel", size=13, color="A9BAD0")
    d.text(792, 384, 380, "≈ 24 рабочих дня в год", size=13, color=AMBER, bold=True)

    d.rect(760, 452, 440, 168, fill="0F2038", radius=14, line="26415F")
    d.text(792, 472, 380, "Источников данных", size=12.5, color="8FA6C4", upper=True, bold=True)
    d.text(792, 496, 380, "4 → 1", size=46, color="6E9BFF", bold=True)
    d.text(792, 556, 380, "бумага · Excel · 1С · переписка\nстановится единой базой", size=13, color="A9BAD0", lh=1.4)

    d.text(760, 634, 440, "Итог: решения принимаются на глаз", size=13, color="8FA6C4", italic=True)


def s03_goal(d):
    slide_frame(d, 3, "Цель и задачи", "Что нужно было сделать",
                "Цель, объект и предмет работы, а также задачи, которые решались по ходу проекта")

    d.rect(80, 216, 470, 196, fill=CARD, radius=16, shadow=True)
    d.rect(80, 216, 470, 5, fill=BLUE, radius=3)
    d.text(108, 240, 400, "Цель работы", size=11.5, color=BLUE, upper=True, bold=True)
    d.text(108, 264, 414,
           "Спроектировать и разработать информационную систему «Аналитика эффективности "
           "предприятия» для ООО «ФАВОРИТ», которая автоматизирует сбор, расчёт и "
           "визуализацию показателей.", size=15.5, color=TXT, lh=1.42)

    d.rect(80, 430, 470, 100, fill=CARD, radius=14, shadow=True)
    d.text(108, 450, 400, "Объект", size=11.5, color=MUTED, upper=True, bold=True)
    d.text(108, 470, 414, "Веб-приложение для аналитики эффективности предприятия", size=14, color=TXT, lh=1.35)

    d.rect(80, 546, 470, 100, fill=CARD, radius=14, shadow=True)
    d.text(108, 566, 400, "Предмет", size=11.5, color=MUTED, upper=True, bold=True)
    d.text(108, 586, 414, "Процесс проектирования ИС, автоматизирующей сбор, расчёт и визуализацию показателей", size=13.5, color=TXT, lh=1.35)

    # задачи
    d.text(600, 216, 600, "Задачи", size=11.5, color=MUTED, upper=True, bold=True)
    tasks = [
        "Проанализировать предметную область и бизнес-процессы",
        "Сравнить готовые решения и обосновать выбор стека",
        "Сформулировать функциональные и нефункциональные требования",
        "Спроектировать архитектуру и модель данных (10 таблиц)",
        "Реализовать серверную часть, формы ввода и дашборд",
        "Разработать отчётность, экспорт CSV и провести тестирование",
    ]
    y = 244
    for i, t in enumerate(tasks, 1):
        d.rect(600, y, 48, 48, fill=SOFT, radius=12)
        d.text(600, y + 12, 48, str(i), size=18, color=BLUE, bold=True, align="center")
        d.text(664, y + 13, 530, t, size=14, color=TXT, lh=1.3)
        y += 64

    d.text(600, 636, 600, "Методы: анализ, сравнение, моделирование, проектирование БД, тестирование",
           size=12, color=MUTED)


def s04_object(d):
    slide_frame(d, 4, "Предметная область", "Объект автоматизации — мебельная фабрика",
                "ООО «ФАВОРИТ»: корпусная и мягкая мебель на заказ, три цеха, собственные каналы продаж")

    # процессная цепочка
    d.text(80, 212, 600, "Производственный процесс", size=11.5, color=MUTED, upper=True, bold=True)
    steps = ["Заказ\nклиента", "Конструктор\nи раскрой", "Цеха:\nмягкая и корпусная", "Сборка\nи контроль", "Отгрузка\nи продажа"]
    x = 80
    for i, s in enumerate(steps):
        d.rect(x, 236, 138, 74, fill=CARD, radius=12, shadow=True)
        d.rect(x, 236, 138, 3, fill=BLUE if i % 2 == 0 else TEAL, radius=2)
        d.text(x + 12, 252, 116, s, size=11.5, color=TXT, bold=True, lh=1.28)
        if i < 4:
            d.arrow(x + 140, 273, x + 154, 273, color="B9C6D8", width=1.4, head=5)
        x += 160

    # проблемы «как есть»
    d.text(80, 342, 600, "Проблемы «как есть»", size=11.5, color=RED, upper=True, bold=True)
    problems = [
        "выпуск и брак фиксируются в цехах на бумаге, затем переносятся в Excel;",
        "нет единого справочника цехов и категорий — периоды несопоставимы;",
        "финансы и производство ведут разные сотрудники, данные не связаны;",
        "нет оперативной картины загрузки мощностей и потерь от брака.",
    ]
    y = 366
    for p in problems:
        d.circle(90, y + 8, 3.5, fill=RED)
        d.text(106, y, 590, p, size=13, color=TXT, lh=1.34)
        y += 40

    # «как должно быть»
    d.rect(80, 540, 640, 106, fill="E9F7F4", radius=14)
    d.rect(80, 540, 5, 106, fill=TEAL, radius=3)
    d.text(104, 558, 590, "Как должно быть", size=11.5, color="0B7F71", upper=True, bold=True)
    d.text(104, 578, 596,
           "Данные вводятся один раз через веб-формы → хранятся в базе → показатели считаются "
           "SQL-запросами при открытии страницы.", size=13, color="0D4B44", lh=1.36)

    # роли
    x = 860
    d.text(x, 212, 340, "Пользователи системы", size=11.5, color=MUTED, upper=True, bold=True)
    roles = [
        ("Гость", "просмотр дашборда и разделов, без права изменения", "9AA8BC"),
        ("Сотрудник", "ввод и редактирование данных, смена статусов, плановые показатели", BLUE),
        ("Администратор", "всё то же + пользователи, роли, резервное копирование", TEAL),
    ]
    y = 240
    for name, desc, col in roles:
        d.rect(x, y, 340, 122, fill=CARD, radius=14, shadow=True)
        d.circle(x + 32, y + 38, 15, fill=col, alpha=0.14)
        d.circle(x + 32, y + 38, 6, fill=col)
        d.text(x + 58, y + 20, 262, name, size=15, color=TXT, bold=True)
        d.text(x + 58, y + 46, 264, desc, size=11.5, color=MUTED, lh=1.34)
        y += 134

    d.text(x, 650, 340, "Права разграничены\nчерез сессии и роли", size=11.5, color=MUTED, italic=True, lh=1.3)


def s05_choice(d):
    slide_frame(d, 5, "Обоснование решений", "Почему заказное веб-приложение",
                "Сравнение четырёх вариантов автоматизации аналитики на масштабе среднего предприятия")

    cols = [80, 330, 620, 940]
    d.rect(80, 212, 1120, 40, fill=NAVY, radius=8)
    heads = ["Вариант", "Достоинства", "Недостатки", "Вывод"]
    for i, hh in enumerate(heads):
        d.text(cols[i] + (18 if i == 0 else 14), 223, 300, hh, size=11.5, color=WHITE, bold=True, upper=True)

    rows = [
        ("Excel / Google Таблицы", "Быстрый старт, знакомый интерфейс",
         "Ручной ввод, ошибки, нет прав доступа", "Только малый объём"),
        ("1С:ERP", "Полный учёт и регламентированная отчётность",
         "Высокая стоимость, сложное внедрение", "Избыточно для задачи"),
        ("Power BI / DataLens", "Гибкая визуализация",
         "Нужны подготовленные данные и подписка", "Только надстройка"),
        ("Заказное веб-приложение на PHP", "Точное соответствие процессам, низкая стоимость",
         "Требует разработки и сопровождения", "Выбрано"),
    ]
    y = 256
    for i, (a, b, c, e) in enumerate(rows):
        chosen = i == 3
        d.rect(80, y, 1120, 78, fill="EAF1FF" if chosen else CARD, radius=10,
               shadow=not chosen, line=BLUE if chosen else None, line_w=1.4)
        d.text(cols[0] + 18, y + 20, 236, a, size=13.5, color=TXT, bold=True, lh=1.3)
        d.text(cols[1] + 14, y + 20, 280, b, size=12, color=TXT, lh=1.32)
        d.text(cols[2] + 14, y + 20, 300, c, size=12, color=MUTED, lh=1.32)
        if chosen:
            d.rect(cols[3] + 12, y + 24, 132, 30, fill=BLUE, radius=15)
            d.text(cols[3] + 12, y + 31, 132, "выбрано", size=11.5, color=WHITE, bold=True, align="center")
        else:
            d.text(cols[3] + 12, y + 22, 150, e, size=12, color=MUTED, lh=1.3)
        y += 85

    # стек
    d.text(80, 600, 400, "Стек и почему именно он", size=11.5, color=MUTED, upper=True, bold=True)
    stack = [("PHP 8 + PDO", 148), ("MySQL 8 / SQLite", 186), ("SVG-графики", 152), ("CSS + HTML", 140), ("OpenServer", 150)]
    x = 80
    for name, wdt in stack:
        d.rect(x, 626, wdt, 34, fill=WHITE, radius=17, line=LINE, line_w=1.2)
        d.text(x, 635, wdt, name, size=12, color=TXT, bold=True, align="center")
        x += wdt + 12
    d.text(920, 620, 280, "без фреймворков и CDN —\nработает без интернета", size=11.5, color=MUTED, lh=1.3)


def s06_arch(d):
    slide_frame(d, 6, "Проектирование", "Трёхуровневая архитектура",
                "Каждый уровень отвечает за своё: разметка, расчёты и хранение данных")

    layers = [
        ("Уровень представления", "HTML-шаблоны, analytics.css, 10 страниц разделов",
         "Дашборд · Заказы · Производство · Качество · Финансы · Продажи · Каналы · Кадры · Отчёты · Справочник", BLUE),
        ("Уровень бизнес-логики", "analytics_lib.php: an_monthly(), an_kpi(), an_line_chart(), an_bar_chart()",
         "Расчёт показателей, сравнение с планом, прогноз, CSRF, сессии, журнал действий", TEAL),
        ("Уровень данных", "MySQL 8 (favorit_db) или резервная SQLite; db.php + analytics_schema.php",
         "10 таблиц an_* и users, автосоздание схемы и демо-данных при первом запуске", AMBER),
    ]
    y = 218
    for i, (ttl, sub, det, col) in enumerate(layers):
        d.rect(80, y, 760, 118, fill=CARD, radius=14, shadow=True)
        d.rect(80, y, 6, 118, fill=col, radius=3)
        d.text(110, y + 20, 300, f"0{i+1}", size=11, color=col, bold=True, upper=True)
        d.text(146, y + 18, 660, ttl, size=17, color=TXT, bold=True)
        d.text(146, y + 46, 660, sub, size=12.5, color=TXT, lh=1.3)
        d.text(146, y + 82, 660, det, size=11.5, color=MUTED, lh=1.3)
        if i < 2:
            d.arrow(460, y + 120, 460, y + 136, color="B9C6D8", width=1.6, head=6)
        y += 142

    # правая колонка
    d.text(880, 218, 320, "Решения уровня", size=11.5, color=MUTED, upper=True, bold=True)
    points = [
        ("Поток данных", "форма → таблица → расчёт → KPI, график, CSV"),
        ("Единый источник", "ни одна цифра не вписана в HTML вручную"),
        ("Резерв БД", "MySQL недоступен → SQLite без правки кода"),
        ("Схема PRG", "после POST — редирект, дублей записей нет"),
        ("Без сборки", "копирование папки на хостинг — и всё работает"),
    ]
    y = 246
    for t, s in points:
        d.text(880, y, 320, t, size=13, color=TXT, bold=True)
        d.text(880, y + 20, 320, s, size=12, color=MUTED, lh=1.32)
        y += 74

    d.rect(880, 618, 320, 46, fill="EAF1FF", radius=10)
    d.text(898, 631, 290, "Время отклика страницы < 2 с", size=12, color=BLUE_D, bold=True)


def s07_data(d):
    slide_frame(d, 7, "Модель данных", "10 таблиц, связанных периодом и справочниками",
                "Помесячные записи по цехам и каналам — основа всех расчётов")

    d.rect(80, 224, 200, 96, fill=NAVY, radius=14)
    d.text(80, 244, 200, "ПЕРИОД", size=11, color="7FA6FF", bold=True, align="center")
    d.text(80, 264, 200, "месяц", size=24, color=WHITE, bold=True, align="center")
    d.text(80, 296, 200, "май–октябрь 2025", size=11, color="9DB0C8", align="center")

    groups = [
        ("Производство", ["an_production — выпуск, брак, часы, себестоимость",
                          "an_defects — причины брака и потери"], BLUE, 200),
        ("Коммерция", ["an_orders — портфель и статусы",
                       "an_sales — продажи по каналам",
                       "an_channels — план, затраты, лиды"], TEAL, 340),
        ("Справочники", ["an_categories, an_products — номенклатура и цены",
                         "an_staff — штат, отделы, оклады"], AMBER, 510),
        ("Управление", ["an_targets — план загрузки, брака, выручки",
                        "an_audit — журнал действий", "users — авторизация и роли"], "8B5CF6", 596),
    ]
    # вертикальная шина
    d.line(272, 274, 316, 274, color="C3CFDF", width=1.6)

    y = 206
    for name, items, col, hh in groups:
        d.line(316, y + 26, 372, y + 26, color="C3CFDF", width=1.6)
        lines = len(items)
        bh = 32 + lines * 25
        d.rect(380, y, 560, bh, fill=CARD, radius=13, shadow=True)
        d.rect(380, y, 5, bh, fill=col, radius=3)
        d.text(402, y + 10, 300, name, size=13, color=TXT, bold=True, upper=True)
        yy = y + 33
        for it in items:
            d.circle(410, yy + 7, 2.5, fill=col)
            d.text(422, yy, 500, it, size=11.5, color=MUTED, lh=1.22)
            yy += 25
        y += bh + 13

    # связи
    d.rect(978, 210, 222, 190, fill=CARD, radius=13, shadow=True)
    d.text(998, 226, 190, "Связи", size=11.5, color=MUTED, upper=True, bold=True)
    rels = ["1 : M — категория → продукция",
            "1 : M — канал → продажи",
            "план / факт — an_targets",
            "внешние ключи, каскад"]
    yy = 252
    for r in rels:
        d.circle(1002, yy + 7, 2.5, fill=BLUE)
        d.text(1012, yy, 178, r, size=11, color=TXT, lh=1.28)
        yy += 34

    d.rect(978, 398, 222, 252, fill="0E1B2E", radius=13)
    d.text(998, 414, 190, "Демо-данные", size=11, color="7FA6FF", upper=True, bold=True)
    facts = [("6", "месяцев"), ("18", "записей производства"), ("48", "заказов"),
             ("24", "случая брака"), ("10", "сотрудников")]
    yy = 436
    for v, f in facts:
        d.text(998, yy, 34, v, size=15, color=WHITE, bold=True)
        d.text(1040, yy + 3, 150, f, size=11, color="C6D3E4")
        yy += 31
    d.text(998, 600, 190, "создаются автоматически\nпри первом запуске", size=10.5, color="8FA6C4", lh=1.3)


def _kpi_row(d, x, y, w, value, label, note=None, color=TXT, gap=86):
    d.text(x, y, w, value, size=30, color=color, bold=True)
    d.text(x, y + 40, w, label, size=12, color=MUTED, upper=True, bold=True)
    if note:
        d.text(x, y + 58, w, note, size=10.5, color="93A1B5")


def s08_dashboard(d):
    slide_frame(d, 8, "Практическая часть · 1", "Дашборд: картина за пять секунд",
                "Четыре ключевых показателя, сводный график за шесть месяцев и автоматические выводы")

    d.rect(80, 214, 742, 428, fill=CARD, radius=14, shadow=True)
    d.image(SCREENS + "01_dashboard.png", 92, 226, 718, 404, radius=8, crop=SHOT_CROP)

    x = 872
    kpis = [("12 480", "Выпуск за месяц", "изделий · −1,0 % к сентябрю", TXT),
            ("8,54 млн ₽", "Выручка", "прибыль 834 820 ₽ · +0,9 %", "0B7F71"),
            ("2,4 %", "Коэффициент брака", "300 изделий · норма 3,0 %", RED),
            ("87 %", "Загрузка мощностей", "4 700 из 5 400 часов", "B07416")]
    y = 218
    for v, l, n, c in kpis:
        d.rect(x, y, 328, 88, fill=CARD, radius=12, shadow=True)
        d.text(x + 20, y + 14, 290, v, size=25, color=c, bold=True)
        d.text(x + 20, y + 50, 290, l, size=11, color=MUTED, bold=True, upper=True)
        d.text(x + 20, y + 68, 290, n, size=10.5, color="93A1B5")
        y += 96

    d.rect(x, 626, 328, 36, fill="EAF1FF", radius=10)
    d.text(x, 636, 328, "Прогноз выручки: 8 703 333 ₽", size=11.5, color=BLUE_D, bold=True, align="center")

    d.text(80, 648, 700, "Все значения считаются SQL-запросами из базы при открытии страницы", size=11, color=MUTED, italic=True)


def _shot_slide(d, num, eyebrow_txt, title, subtitle, img, bullets, kpis, note, fig=None):
    slide_frame(d, num, eyebrow_txt, title, subtitle)
    d.rect(80, 214, 700, 448, fill=CARD, radius=14, shadow=True)
    d.image(SCREENS + img, 92, 226, 676, 424, radius=8, crop=SHOT_CROP)
    if fig:
        d.text(92, 652, 620, fig, size=10, color=MUTED, italic=True)

    x = 812
    y = 222
    for v, l, c in kpis:
        d.text(x, y, 260, v, size=23, color=c, bold=True)
        d.text(x, y + 32, 260, l, size=11, color=MUTED, upper=True, bold=True)
        y += 74

    y += 10
    for b in bullets:
        d.circle(x + 4, y + 8, 3, fill=BLUE)
        hh = d.text(x + 18, y, 368, b, size=12.5, color=TXT, lh=1.34)
        y += max(46, hh + 14)

    d.text(812, 650, 300, note, size=10.5, color=MUTED, italic=True, lh=1.3)


def s09_production(d):
    _shot_slide(
        d, 9, "Практическая часть · 2", "Производство и качество",
        "Выпуск по цехам, динамика брака, потери в рублях и диаграмма Парето по причинам",
        "02_production.png",
        ["Форма: месяц, цех, категория, выпуск, брак, часы",
         "Загрузка = часы ÷ плановый фонд",
         "Потери от брака — в рублях и в доле выручки",
         "Диаграмма Парето: главная причина потерь"],
        [("12 480", "Выпуск, изделий", TXT), ("2,4 %", "Брак, 300 шт.", RED),
         ("87 %", "Загрузка цехов", "B07416")],
        "Каждая строка формы сразу меняет KPI на дашборде",
        fig="Скриншот из пояснительной записки (рис. 2) — раздел «Производственная аналитика»")


def s10_finance(d):
    _shot_slide(
        d, 10, "Практическая часть · 3", "Финансы и продажи",
        "Выручка, себестоимость, прибыль и рентабельность — по месяцам и по каналам",
        "03_finance.png",
        ["Рентабельность = прибыль ÷ выручка",
         "Средний чек = выручка ÷ число заказов",
         "Каналы: план/факт, CAC, конверсия",
         "Лидер — сайт: 3,93 млн ₽ (46 % выручки)"],
        [("8,54 млн ₽", "Выручка за октябрь", TXT), ("834 820 ₽", "Прибыль", "0B7F71"),
         ("9,8 %", "Рентабельность", "0B7F71")],
        "Финансовый и производственный контуры считаются из одной базы",
        fig="Скриншот из пояснительной записки (рис. 3) — раздел «Финансовая аналитика»")


def s11_orders(d):
    slide_frame(d, 11, "Практическая часть · 4", "Операционные разделы",
                "Заказы и кадры: данные, которые тоже питают аналитику")

    d.rect(80, 216, 552, 372, fill=CARD, radius=14, shadow=True)
    d.image(SCREENS + "04_orders.png", 92, 228, 528, 348, radius=8, crop=(0.177, 0.30, 1.0, 1.0))
    d.text(80, 600, 552, "Заказы: портфель, статусы, сроки и просрочка", size=13.5, color=TXT, bold=True)
    d.text(80, 622, 552, "Смена статуса прямо в таблице — показатели пересчитываются", size=11.5, color=MUTED)

    d.rect(656, 216, 544, 372, fill=CARD, radius=14, shadow=True)
    d.image(SCREENS + "07_hr.png", 668, 228, 520, 348, radius=8, crop=(0.177, 0.0, 1.0, 0.48))
    d.text(656, 600, 544, "Кадры: штат, ФОТ по отделам, приём и увольнение", size=13.5, color=TXT, bold=True)
    d.text(656, 622, 544, "10 сотрудников, ФОТ 726 000 ₽/мес, средняя зарплата 72 600 ₽", size=11.5, color=MUTED)


def s12_security(d):
    slide_frame(d, 12, "Практическая часть · 5", "Отчётность, роли и безопасность",
                "Сводный отчёт, плановые показатели, журнал действий и защита данных")

    d.rect(80, 214, 640, 418, fill=CARD, radius=14, shadow=True)
    d.image(SCREENS + "05_reports.png", 92, 226, 616, 394, radius=8, crop=SHOT_CROP)

    x = 750
    d.text(x, 218, 420, "Экспорт и контроль", size=11.5, color=MUTED, upper=True, bold=True)
    pts = [("CSV с BOM и «;»", "открывается в Excel без настройки кодировки"),
           ("Плановые показатели", "загрузка, допустимый брак, план выручки"),
           ("Журнал действий", "кто, когда и что изменил")]
    y = 244
    for t, s in pts:
        d.text(x, y, 420, t, size=13.5, color=TXT, bold=True)
        d.text(x, y + 21, 420, s, size=11.5, color=MUTED, lh=1.3)
        y += 66

    d.text(x, 438, 420, "Безопасность", size=11.5, color=MUTED, upper=True, bold=True)
    chips = [("PDO", "подготовленные выражения"), ("CSRF", "токен в каждой форме"),
             ("password_hash", "хранение паролей"), ("PRG", "нет дублей записей"),
             ("htmlspecialchars", "защита от XSS"), ("Роли", "гость / сотрудник / админ")]
    col_w, row_h = 216, 50
    for i, (a, b) in enumerate(chips):
        cx = x + (i % 2) * (col_w + 10)
        cy = 466 + (i // 2) * row_h
        d.rect(cx, cy, col_w, 44, fill=SOFT, radius=10)
        d.text(cx + 14, cy + 6, col_w - 28, a, size=11, color=BLUE_D, bold=True)
        d.text(cx + 14, cy + 24, col_w - 28, b, size=9.5, color=MUTED)

    d.text(80, 644, 700, "Журнал аудита выводится в разделе «Отчёты» и служит доказательством изменений", size=11, color=MUTED, italic=True)


def s13_tests(d):
    slide_frame(d, 13, "Тестирование", "15 тест-кейсов — все пройдены",
                "Функциональные проверки, негативные сценарии и сверка расчётов")

    d.rect(80, 214, 1120, 42, fill=NAVY, radius=8)
    heads = [(100, "№", 40), (150, "Проверка", 470), (640, "Ожидаемый результат", 470), (1090, "Статус", 90)]
    for cx, hh, ww in heads:
        d.text(cx, 225, ww, hh, size=11, color=WHITE, bold=True, upper=True)

    rows = [
        ("1", "Открытие дашборда без авторизации", "Показатели и графики отображаются"),
        ("3", "Отправка формы без обязательных полей", "Сообщение об ошибке, запись не создана"),
        ("6", "Экспорт отчёта в CSV", "Файл скачивается и открывается в Excel"),
        ("7", "Попытка SQL-инъекции в поле поиска", "Запрос обработан как текст"),
        ("9", "Смена статуса заказа в списке", "Статус сохранён, показатели пересчитаны"),
        ("15", "Смена роли пользователя администратором", "Роль сохранена, доступ ограничен"),
    ]
    y = 264
    for i, (n, a, b) in enumerate(rows):
        d.rect(80, y, 1120, 42, fill=CARD if i % 2 == 0 else "F8FAFD")
        d.text(100, y + 13, 40, n, size=12, color=MUTED, bold=True)
        d.text(150, y + 12, 470, a, size=12, color=TXT)
        d.text(640, y + 12, 440, b, size=12, color=MUTED)
        d.rect(1088, y + 10, 76, 22, fill="DDF3EA", radius=11)
        d.text(1088, y + 14, 76, "пройдено", size=9.5, color="0B7F71", bold=True, align="center")
        y += 44

    d.rect(80, 550, 540, 96, fill="EAF1FF", radius=14)
    d.text(102, 566, 500, "Сверка расчётов", size=11, color=BLUE_D, upper=True, bold=True)
    d.text(102, 588, 496, "сумма по цехам = итог месяца · брак ÷ выпуск = коэффициент брака ·\nвыручка − себестоимость = прибыль",
           size=11.5, color=TXT, lh=1.35)

    d.rect(650, 550, 550, 96, fill=CARD, radius=14, shadow=True)
    d.text(672, 566, 510, "Негативные сценарии", size=11, color=MUTED, upper=True, bold=True)
    d.text(672, 588, 506, "пустые поля, отрицательные значения, повторная отправка формы,\nнедоступность MySQL (переход на SQLite)",
           size=11.5, color=TXT, lh=1.35)

    d.text(80, 654, 1120, "Расхождений не обнаружено — система готова к опытной эксплуатации", size=11.5, color=MUTED, italic=True)


def s14_effect(d):
    d.bg(NAVY)
    slide_frame(d, 14, "Результат", "Что даёт система", dark=True,
                subtitle="Отчётность собирается автоматически, а не «к концу месяца»")

    d.rect(80, 226, 500, 250, fill="122A47", radius=16, line="27466B")
    d.text(108, 248, 440, "Подготовка отчётности", size=11.5, color="8FA6C4", upper=True, bold=True)
    d.text(108, 276, 220, "2 дня", size=44, color="8FA6C4", bold=True)
    d.text(300, 292, 90, "→", size=32, color=AMBER, bold=True)
    d.text(340, 276, 220, "5 минут", size=44, color=WHITE, bold=True)
    d.text(108, 342, 440, "Отчёт формируется из базы по кнопке, а не переносится\nиз Excel вручную",
           size=12.5, color="A9BAD0", lh=1.4)
    d.rect(108, 400, 200, 32, fill=AMBER, radius=16)
    d.text(108, 408, 200, "≈ 24 дня в год", size=11.5, color="3A2A08", bold=True, align="center")

    d.rect(80, 496, 500, 140, fill="0F2038", radius=14, line="26415F")
    d.text(108, 514, 440, "Экономический эффект", size=11.5, color="8FA6C4", upper=True, bold=True)
    d.text(108, 540, 440, "меньше ручной работы · видны потери от брака ·\nпрогноз выручки по фактическим данным",
           size=12.5, color="C6D3E4", lh=1.4)

    d.text(620, 226, 560, "Решённые задачи", size=11.5, color="8FA6C4", upper=True, bold=True)
    done = ["Проведён анализ предметной области и сформулированы требования",
            "Спроектированы архитектура и структура БД из 10 таблиц",
            "Реализованы 10 разделов, формы ввода и дашборд",
            "Разработан модуль визуализации, отчётность и экспорт CSV",
            "Проведено тестирование: 15 тест-кейсов пройдены",
            "Подготовлена документация по развёртыванию и эксплуатации"]
    y = 254
    for t in done:
        d.circle(628, y + 10, 8, fill="1E8F7C", alpha=0.28)
        d.text(624, y + 5, 20, "✓", size=11, color="4FD1B8", bold=True, align="center")
        d.text(650, y, 530, t, size=12.5, color="D7E1EE", lh=1.3)
        y += 40

    d.rect(620, 512, 560, 124, fill="122A47", radius=14, line="27466B")
    d.text(648, 530, 500, "Перспективы развития", size=11.5, color="8FA6C4", upper=True, bold=True)
    d.text(648, 554, 504, "интеграция с бухгалтерией · прогноз выпуска · права по отделам ·\nмобильная версия · авто-рассылка отчётов руководителям",
           size=12, color="C6D3E4", lh=1.4)


def s15_thanks(d):
    d.gradient_bg(NAVY, "13294A")
    d.circle(150, 640, 240, fill="2F6BFF", alpha=0.10)
    d.circle(1180, 90, 200, fill="0FAF9B", alpha=0.08)

    eyebrow(d, 80, 150, "Курсовая работа · 2026", "7FA6FF")
    d.text(80, 186, 760, "Спасибо\nза внимание!", size=58, color=WHITE, bold=True, lh=1.08)
    d.rect(80, 344, 74, 4, fill=AMBER)
    d.text(80, 372, 640, "Готов показать систему вживую: дашборд, добавление записи, "
                         "пересчёт показателей и выгрузку отчёта.", size=16, color="B9C8DA", lh=1.45)

    d.rect(80, 470, 620, 108, fill="101F36", radius=14, line="27466B")
    d.text(106, 490, 560, "Семиглазов Данил Вячеславович", size=17, color=WHITE, bold=True)
    d.text(106, 516, 560, "группа 44 СПО · ПМ.05 Проектирование и разработка ИС", size=12.5, color="8FA6C4")
    d.text(106, 540, 560, "Руководитель: Колесникова С.Н.", size=12.5, color="8FA6C4")

    # карточка с ключевыми цифрами
    d.rect(760, 186, 440, 390, fill="0F2038", radius=16, line="27466F")
    d.text(792, 210, 380, "Система в цифрах", size=11, color="7FA6FF", upper=True, bold=True)
    stats = [("10", "разделов аналитики"), ("10", "таблиц базы данных"),
             ("15", "тест-кейсов пройдено"), ("6", "месяцев демо-данных"),
             ("0", "внешних зависимостей")]
    y = 240
    for v, l in stats:
        d.text(792, y, 70, v, size=26, color=WHITE, bold=True, align="right")
        d.text(880, y + 8, 300, l, size=12.5, color="A9BAD0")
        y += 62

    d.text(760, 596, 440, "ГБПОУ РО «КТСиА» · г. Каменск-Шахтинский", size=11, color="8FA6C4")


SLIDES = [s01_title, s02_problem, s03_goal, s04_object, s05_choice, s06_arch,
          s07_data, s08_dashboard, s09_production, s10_finance, s11_orders,
          s12_security, s13_tests, s14_effect, s15_thanks]
