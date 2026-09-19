#!/usr/bin/env python3
"""Serve the reader-facing atlas from the repository root."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import html
from urllib.parse import urlsplit
import markdown

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = Path(self.translate_path(urlsplit(self.path).path)).resolve()
        if not path.is_relative_to(ROOT) or any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            self.send_error(404)
            return None
        if path.suffix == '.md' and path.is_file():
            import io
            source = path.read_text(encoding='utf-8')
            converter = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'])
            body = converter.convert(source)
            title = source.splitlines()[0].lstrip('# ').strip()
            page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<link rel="stylesheet" href="/site/reader.css"></head><body>
<nav><a href="/site/">Research atlas</a> · <a href="/reports/themes/README.md">Themes</a> ·
<a href="/reports/expanded-taxonomy-v1.md">All subthemes</a> · <a href="/reports/directions/README.md">Research directions</a></nav>
<div class="reading-layout"><aside aria-label="Article contents">{converter.toc}</aside><main><article>{body}</article></main></div>
</body></html>'''.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(page)))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            return io.BytesIO(page)
        return super().send_head()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 8765), QuietHandler)
    print("Atlas available at http://127.0.0.1:8765/site/", flush=True)
    server.serve_forever()
