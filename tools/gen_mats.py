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
# Los seis productos que vende el cliente. Cada uno tiene una superficie
# distinta para que se distingan de un vistazo en la grilla.

def p_logo(w=900, h=620):
    """Felpudos con y sin logo — PVC liso con el logo impreso."""
    mat = base_mat(w, h, (26, 31, 38))
    d = ImageDraw.Draw(mat)
    for y in range(0, h, 6):
        d.line([(0, y), (w, y)], fill=(34, 40, 48), width=1)
    add_border(d, w, h, 34, CELESTE, 8, 20)
    brand(d, w, int(h * 0.36), scale=1.35)
    f = font(21, weight=600, width=100)
    centered(d, "BIENVENIDOS", f, w // 2, int(h * 0.74), (150, 163, 176))
    return finish(mat, w, h)


def p_lluvia(w=900, h=620):
    """Felpudos para dias de lluvia — fibra absorbente con gotas."""
    mat = base_mat(w, h, (34, 42, 52))
    tex = noise_layer((w, h), amount=54, blur=0.4).convert("RGB")
    mat = Image.blend(mat, tex, 0.44)
    d = ImageDraw.Draw(mat, "RGBA")
    # gotas de agua sobre la superficie
    for _ in range(90):
        x, y = random.randint(28, w - 28), random.randint(28, h - 28)
        r = random.randint(4, 11)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 200, 236, 40))
        d.arc([x - r, y - r, x + r, y + r], 200, 330, fill=(198, 226, 245, 110), width=2)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, outline=(22, 28, 35), width=26)
    brand(d, w, int(h * 0.36), scale=1.3, color=BONE, accent=CELESTE)
    f = font(20, weight=600, width=100)
    centered(d, "D Í A S   D E   L L U V I A", f, w // 2, int(h * 0.74), (176, 200, 220))
    return finish(mat, w, h)


def p_antideslizante(w=900, h=620):
    """Alfombras antideslizantes — goma nervada de agarre."""
    mat = base_mat(w, h, (23, 28, 34))
    d = ImageDraw.Draw(mat)
    # nervaduras: relieve marcado con luz arriba y sombra abajo
    for y in range(24, h - 24, 16):
        d.line([(24, y), (w - 24, y)], fill=(46, 55, 66), width=6)
        d.line([(24, y + 4), (w - 24, y + 4)], fill=(14, 18, 23), width=3)
    # franja de seguridad en los bordes
    for yy in (16, h - 26):
        d.rectangle([16, yy, w - 16, yy + 10], fill=CELESTE)
    box = [int(w * .17), int(h * .28), int(w * .83), int(h * .72)]
    d.rounded_rectangle(box, 12, fill=(26, 32, 39))
    brand(d, w, int(h * 0.36), scale=1.25, color=BONE, accent=CELESTE)
    return finish(mat, w, h)


def p_antifatiga(w=900, h=620):
    """Tapetes antifatiga — espuma gruesa con borde biselado y relieve rombo."""
    mat = base_mat(w, h, (30, 36, 44))
    d = ImageDraw.Draw(mat)
    # bisel perimetral (el canto inclinado tipico del antifatiga)
    for i, c in enumerate([(52, 62, 74), (44, 53, 64), (37, 45, 55)]):
        o = 10 + i * 9
        d.rounded_rectangle([o, o, w - o, h - o], 18, outline=c, width=9)
    # relieve de rombos
    step = 46
    for y in range(52, h - 40, step):
        for x in range(52, w - 40, step):
            d.polygon([(x, y - 14), (x + 16, y), (x, y + 14), (x - 16, y)],
                      outline=(56, 67, 80))
    box = [int(w * .18), int(h * .3), int(w * .82), int(h * .7)]
    d.rounded_rectangle(box, 12, fill=(30, 36, 44))
    brand(d, w, int(h * 0.36), scale=1.25, color=BONE, accent=CELESTE)
    f = font(19, weight=600, width=100)
    centered(d, "C O N F O R T   D E   P I E", f, w // 2, int(h * 0.735), (150, 163, 176))
    return finish(mat, w, h)


def p_vinilico(w=900, h=620):
    """Felpudos vinilicos — maraña de hilo de vinilo (tipo espagueti)."""
    mat = base_mat(w, h, (21, 26, 32))
    d = ImageDraw.Draw(mat)
    # bucles de vinilo entrelazados
    for _ in range(950):
        x, y = random.randint(18, w - 18), random.randint(18, h - 18)
        r = random.randint(9, 19)
        a = random.randint(0, 359)
        tone = random.choice([(48, 58, 70), (39, 48, 58), (58, 70, 84)])
        d.arc([x - r, y - r, x + r, y + r], a, a + random.randint(140, 260),
              fill=tone, width=3)
    box = [int(w * .17), int(h * .29), int(w * .83), int(h * .71)]
    d.rounded_rectangle(box, 12, fill=(24, 30, 37))
    brand(d, w, int(h * 0.36), scale=1.25, color=CELESTE, accent=BONE)
    add_border(d, w, h, 22, (54, 64, 76), 6, 18)
    return finish(mat, w, h)


def p_extraduty(w=900, h=620):
    """Alfombras extra duty de alto transito — rizo denso."""
    mat = base_mat(w, h, (19, 23, 29))
    d = ImageDraw.Draw(mat)
    # rizo cerrado: puntos densos en tresbolillo
    step = 13
    for row, y in enumerate(range(20, h - 14, step)):
        off = (step // 2) if row % 2 else 0
        for x in range(20 + off, w - 14, step):
            t = random.choice([(40, 48, 58), (33, 40, 49), (48, 58, 70)])
            d.ellipse([x, y, x + 6, y + 6], fill=t)
    box = [int(w * .16), int(h * .29), int(w * .84), int(h * .71)]
    d.rounded_rectangle(box, 12, fill=(22, 27, 34))
    brand(d, w, int(h * 0.36), scale=1.28, color=BONE, accent=CELESTE)
    f = font(19, weight=600, width=100)
    centered(d, "A L T O   T R Á N S I T O", f, w // 2, int(h * 0.735), (150, 163, 176))
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, outline=(13, 16, 20), width=18)
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
        "prod-logo.png": p_logo,
        "prod-lluvia.png": p_lluvia,
        "prod-antideslizante.png": p_antideslizante,
        "prod-antifatiga.png": p_antifatiga,
        "prod-vinilico.png": p_vinilico,
        "prod-extraduty.png": p_extraduty,
        "hero-felpudo.png": mat_hero,
    }
    for name, fn in jobs.items():
        img = fn()
        img.save(os.path.join(OUT, name))
        print(f"{name}  {img.size[0]}x{img.size[1]}")
