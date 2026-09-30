# Felpudos Argentinos — landing

Landing de una sola página para **felpudosargentinos.com**: fábrica de felpudos
personalizados con el logo del cliente.

## Estado

Maqueta visual v2, pendiente de aprobación. Los textos y el logo son propios.
Ya están integradas las 7 fotos reales que mandó el cliente (`assets/img/fotos/`,
procesadas con `tools/fotos.py`). **Faltan fotos de dos productos**: alfombras
antideslizantes y tapetes antifatiga — esas dos tarjetas siguen con ilustración.

## Estructura

| Sección | Contenido |
|---|---|
| Hero | Propuesta de valor, CTA a WhatsApp, felpudo destacado |
| 01 Productos | Los seis: con y sin logo, días de lluvia, antideslizantes, antifatiga, vinílicos, extra duty tipo 3M |
| 02 Rubros | 12 rubros + galería para fotos reales |
| 03 Nosotros | Diferenciales de fábrica + métricas |
| 04 Contacto | Datos directos + formulario |

## Archivos

```
index.html               página completa
assets/css/style.css     estilos (un solo archivo, con variables de color)
assets/js/main.js        menú móvil, animaciones al hacer scroll, formulario
assets/fonts/            Archivo + Manrope autoalojadas (sin llamadas externas)
assets/img/              logo, favicon y renders de los seis productos
tools/gen_mats.py        genera los renders de felpudo (Pillow)
tools/shots.py           capturas de control (Playwright)
```

## Datos a reemplazar antes de publicar

- WhatsApp: ya es el real, `+54 9 11 6466 3605`.
- Correo de contacto: `ventas@felpudosargentinos.com`.
- Enlaces de Instagram y Facebook en el pie.
- Métricas de la sección *Nosotros* (años, cantidad de comercios, plazos).
- El formulario hoy abre WhatsApp con los datos cargados. Al subirlo al hosting se
  cambia por envío por correo desde el servidor.

## Probar en local

```sh
python3 -m http.server 8931
# http://127.0.0.1:8931/
```

Es HTML estático: se sube por FTP a `public_html` y funciona. Sin base de datos y
sin dependencias externas.

## Paleta

| | |
|---|---|
| Tinta (goma) | `#12171C` |
| Hueso (papel) | `#F4F1EA` |
| Celeste | `#6FB3E0` / `#3D8CC4` |
| WhatsApp | `#25D366` |
