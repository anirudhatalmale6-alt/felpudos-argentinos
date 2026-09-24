#!/usr/bin/env python3
"""Capturas de la landing para revision visual (desktop + movil)."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "shots")
URL = "http://127.0.0.1:8931/index.html"

os.makedirs(OUT, exist_ok=True)


def run():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ---------------------------------------------------------- escritorio
        pg = b.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_timeout(1400)
        h = pg.evaluate("document.body.scrollHeight")
        print("alto total desktop:", h)
        y, i = 0, 1
        while y < h and i <= 8:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(900)
            pg.screenshot(path=os.path.join(OUT, f"desktop-{i}.png"))
            y += 760
            i += 1
        errs = pg.evaluate("window.__errs || []")
        pg.close()

        # --------------------------------------------------------------- movil
        pg = b.new_page(viewport={"width": 390, "height": 780}, device_scale_factor=1)
        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_timeout(1400)
        h = pg.evaluate("document.body.scrollHeight")
        print("alto total movil:", h)
        y, i = 0, 1
        while y < h and i <= 10:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(800)
            pg.screenshot(path=os.path.join(OUT, f"movil-{i}.png"))
            y += 740
            i += 1
        pg.close()
        b.close()
        print("errores js:", errs)


if __name__ == "__main__":
    sys.exit(run())
