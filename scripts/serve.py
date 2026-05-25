#!/usr/bin/env python3
"""Server lokal untuk Spatial Second Brain.
Usage: python3 scripts/server.py
       Buka http://localhost:8000
"""
import http.server
import socketserver
import os

PORT = 8000
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]} {args[2]}")

print(f"\n  🧠 Spatial Second Brain")
print(f"  ─────────────────────")
print(f"  Buka: http://localhost:{PORT}")
print(f"  Ctrl+C untuk stop\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
