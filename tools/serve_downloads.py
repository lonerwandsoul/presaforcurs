# -*- coding: utf-8 -*-
"""Локальный сервер для скачивания файлов защиты.

* index.html — страница со ссылками
* .pptx/.docx/.zip/.md — отдаются с Content-Disposition: attachment,
  чтобы браузер сразу сохранял файл, а не пытался открыть его inline.

Запуск: python3 tools/serve_downloads.py   (порт из PORT, по умолчанию 8080)
"""
import os
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTACH = {".pptx", ".docx", ".zip", ".md"}

MIME_FIX = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".md": "text/markdown; charset=utf-8",
    ".zip": "application/zip",
}


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"          # keep-alive: страница грузит 15 картинок

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return MIME_FIX.get(ext) or super().guess_type(path)

    def end_headers(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        ext = os.path.splitext(path)[1].lower()
        if ext in ATTACH:
            name = os.path.basename(path)
            self.send_header(
                "Content-Disposition",
                "attachment; filename*=UTF-8''" + urllib.parse.quote(name),
            )
        self.send_header("Cache-Control", "no-store")
        self.send_header("Accept-Ranges", "none")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    srv = Server(("0.0.0.0", port), Handler)
    print(f"serving {ROOT} on http://0.0.0.0:{port}/", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
