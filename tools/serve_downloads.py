# -*- coding: utf-8 -*-
"""Локальный сервер для скачивания файлов защиты.

Отдаёт index.html как страницу со ссылками, а .pptx/.docx/.zip/.md
с заголовком Content-Disposition: attachment — браузер сразу сохраняет файл.
"""
import os
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTACH = {".pptx", ".docx", ".zip", ".md", ".pptx"}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        ext = os.path.splitext(path)[1].lower()
        if ext in ATTACH:
            name = os.path.basename(path)
            self.send_header("Content-Disposition",
                             f'attachment; filename*=UTF-8\'\'{urllib.parse.quote(name)}')
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"http://0.0.0.0:{port}/", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
