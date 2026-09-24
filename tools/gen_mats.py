#!/usr/bin/env python3
"""Genera renders de felpudos (vista cenital) para la maqueta de Felpudos Argentinos.

Son imagenes provisorias: cuando el cliente envie las fotos reales, se reemplazan
por las fotos retocadas manteniendo el mismo encuadre y proporcion.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(BASE, "assets", "fonts")
OUT = os.path.join(BASE, "assets", "img")
ARCHIVO = os.path.join(FONTS, "Archivo-var.ttf")

INK = (18, 23, 28)
CELESTE = (111, 179, 224)
BONE = (244, 241, 234)

random.seed(7)


def font(size, weight=700, width=100):
    f = ImageFont.truetype(ARCHIVO, size)
    try:
        f.set_variation_by_axes([weight, width])  # eje 1 = Weight, eje 2 = Width
    except Exception:
        pass
    return f


def noise_layer(size, amount=14, blur=0.6):
    w, h = size
    n = Image.new("L", (w, h))
    px = n.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = random.randint(128 - amount, 128 + amount)
    return n.filter(ImageFilter.GaussianBlur(blur))


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius, fill=255)
    return m


def centered(draw, text, f, cx, y, fill):
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    draw.text((cx - (r - l) / 2 - l, y), text, font=f, fill=fill)
    return b - t


def base_mat(w, h, body=(30, 36, 43)):
    """Cuerpo del felpudo con textura de goma."""
    mat = Image.new("RGB", (w, h), body)
    tex = noise_layer((w, h), amount=16, blur=0.5).convert("RGB")
    mat = Image.blend(mat, tex, 0.10)
    return mat


def add_border(d, w, h, inset, color=CELESTE, width=7, radius=16):
    d.rounded_rectangle([inset, inset, w - inset, h - inset], radius, outline=color, width=width)


def brand(d, w, cy, scale=1.0, color=BONE, accent=CELESTE, sub="ARGENTINOS"):
    fs = int(58 * scale)
    f1 = font(fs, weight=800, width=92)
    f2 = font(int(fs * 0.44), weight=500, width=100)
    centered(d, "FELPUDOS", f1, w // 2, cy, color)
    bar_w = int(120 * scale)
    by = cy + int(fs * 1.16)
    d.rounded_rectangle([w // 2 - bar_w // 2, by, w // 2 + bar_w // 2, by + int(6 * scale)],
                        int(3 * scale), fill=accent)
    centered(d, " ".join(sub), f2, w // 2, by + int(20 * scale), color)


def finish(mat, w, h, radius=22, shadow=True):
    """Recorta esquinas y agrega sombra sobre fondo transparente."""
    mat.putalpha(rounded_mask((w, h), radius))
    if not shadow:
        return mat
    pad = 46
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [pad + 6, pad + 18, pad + w - 6, pad + h + 14], radius + 4, fill=(8, 12, 16, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    canvas.alpha_composite(sh)
    canvas.alpha_composite(mat, (pad, pad))
    return canvas


# ---------------------------------------------------------------- productos
def mat_impreso(w=900, h=620):
    """PVC 8 mm con logo impreso a color."""
    mat = base_mat(w, h, (26, 31, 38))
    d = ImageDraw.Draw(mat)
    # superficie: micro-relieve de rayas finas
    for y in range(0, h, 6):
        d.line([(0, y), (w, y)], fill=(34, 40, 48), width=1)
    add_border(d, w, h, 34, CELESTE, 8, 20)
    brand(d, w, int(h * 0.36), scale=1.35)
    f = font(21, weight=600, width=100)
    centered(d, "BIENVENIDOS", f, w // 2, int(h * 0.74), (150, 163, 176))
    return finish(mat, w, h)


def mat_calado(w=900, h=620):
    """PVC 12 mm con logo calado (troquelado) y base contrastante."""
    mat = base_mat(w, h, (22, 26, 32))
    d = ImageDraw.Draw(mat)
    # celdas caladas tipico del felpudo perforado
    step, pad = 34, 40
    for y in range(pad, h - pad, step):
        for x in range(pad, w - pad, step):
            d.rounded_rectangle([x, y, x + step - 12, y + step - 12], 4,
                                fill=(13, 16, 20), outline=(38, 45, 54), width=1)
    # ventana central donde va el logo calado
    bx0, by0, bx1, by1 = int(w * .16), int(h * .3), int(w * .84), int(h * .7)
    d.rounded_rectangle([bx0, by0, bx1, by1], 14, fill=(28, 34, 41))
    brand(d, w, int(h * 0.36), scale=1.2, color=CELESTE, accent=BONE)
    add_border(d, w, h, 24, (58, 68, 80), 6, 18)
    return finish(mat, w, h)


def mat_fibra(w=900, h=620):
    """Fibra sintetica atrapa-polvo con logo inyectado."""
    mat = base_mat(w, h, (38, 44, 52))
    # pelo de fibra: ruido grueso direccional
    tex = noise_layer((w, h), amount=60, blur=0.35).convert("RGB")
    mat = Image.blend(mat, tex, 0.5)
    mat = mat.filter(ImageFilter.GaussianBlur(0.35))
    d = ImageDraw.Draw(mat)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, outline=(20, 24, 29), width=26)
    brand(d, w, int(h * 0.36), scale=1.3, color=BONE, accent=CELESTE)
    f = font(20, weight=600, width=100)
    centered(d, "ATRAPA POLVO Y HUMEDAD", f, w // 2, int(h * 0.74), (176, 188, 200))
    return finish(mat, w, h)


def mat_hero(w=1180, h=760):
    """Pieza principal del hero: felpudo grande con logo del cliente."""
    mat = base_mat(w, h, (24, 29, 35))
    d = ImageDraw.Draw(mat)
    for y in range(0, h, 7):
        d.line([(0, y), (w, y)], fill=(32, 38, 46), width=1)
    add_border(d, w, h, 42, CELESTE, 10, 24)
    add_border(d, w, h, 62, (46, 55, 65), 3, 16)
    brand(d, w, int(h * 0.34), scale=1.85)
    f = font(25, weight=600, width=100)
    centered(d, "T U   L O G O   A C Á", f, w // 2, int(h * 0.735), (140, 154, 168))
    return finish(mat, w, h)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = {
        "producto-impreso.png": mat_impreso,
        "producto-calado.png": mat_calado,
        "producto-fibra.png": mat_fibra,
        "hero-felpudo.png": mat_hero,
    }
    for name, fn in jobs.items():
        img = fn()
        path = os.path.join(OUT, name)
        img.save(path)
        print(f"{name}  {img.size[0]}x{img.size[1]}")
