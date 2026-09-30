#!/usr/bin/env python3
"""Prepara las fotos reales del cliente para la web.

Rota las que vinieron de costado, recorta al felpudo, empareja luz y contraste
y exporta a un tamaño unico. Las originales NO se tocan.
"""
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SRC = "/var/lib/freelancer/projects/40372299"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "img", "fotos")
os.makedirs(OUT, exist_ok=True)

# nombre destino -> (archivo, giro, recorte relativo (izq, arr, der, ab), centrado)
# El giro se aplica ANTES del recorte; el recorte va en fracciones 0-1.
# El centrado decide que parte se conserva al ajustar al encuadre 3:2.
JOBS = {
    "scienza":    ("felpudosargentinos1.jpeg",       None,       (0.00, 0.20, 1.00, 0.95), (0.5, 0.5)),
    "magazzino":  ("felpudosargentinos2.jpeg",       "cw",       (0.05, 0.02, 0.98, 0.98), (0.5, 0.5)),
    "sportclub":  ("felpudosargentinos3.jpeg",       "ccw",      (0.02, 0.02, 0.98, 0.98), (0.5, 0.45)),
    "meister":    ("felpudosargentinos4.jpeg",       "ccw",      (0.06, 0.00, 1.00, 0.94), (0.42, 0.30)),
    "lluvia":     ("felpudosargentinos5-lluvia.jpeg", None,      (0.00, 0.38, 1.00, 1.00), (0.5, 0.5)),
    "supermerc":  ("felpudosargentinos6.jpeg",       None,       (0.00, 0.36, 1.00, 1.00), (0.5, 0.5)),
    "hutch":      ("felpudosargentinos7.jpeg",       None,       (0.02, 0.10, 0.98, 0.95), (0.5, 0.5)),
    # antifatiga: se elige la 6 (pasillo en una cerveceria, sin personas ni marcas).
    # NO se usa antifatiga3.jpeg: es un folleto de ViniloPlus, otra empresa.
    "antifatiga": ("antifatiga6.jpeg",               None,       (0.00, 0.28, 1.00, 1.00), (0.5, 0.6)),
}

TARGET = (1200, 800)   # 3:2 para las tarjetas de producto


def rotate(im, how):
    if how == "cw":
        return im.transpose(Image.ROTATE_270)
    if how == "ccw":
        return im.transpose(Image.ROTATE_90)
    return im


def crop_rel(im, box):
    w, h = im.size
    l, t, r, b = box
    return im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))


def fit(im, size, centering=(0.5, 0.5)):
    """Recorta para llegar al encuadre pedido sin deformar."""
    return ImageOps.fit(im, size, method=Image.LANCZOS, centering=centering)


def polish(im):
    """Retoque contenido: nivela, levanta un poco el contraste y define."""
    im = ImageOps.autocontrast(im, cutoff=(0.4, 0.4))
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=62, threshold=3))
    return im


if __name__ == "__main__":
    for name, (src, how, box, cen) in JOBS.items():
        im = Image.open(os.path.join(SRC, src)).convert("RGB")
        im = crop_rel(rotate(im, how), box)
        im = polish(fit(im, TARGET, cen))
        path = os.path.join(OUT, f"{name}.jpg")
        im.save(path, quality=86, optimize=True, progressive=True)
        print(f"{name:10s} {im.size[0]}x{im.size[1]}  {os.path.getsize(path)//1024} KB")
