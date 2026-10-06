# 🩸 Nat's Vampire Bday — 31 OCT 2026

Liga "agregar a calendario" para mandar por WhatsApp.

- **Landing (la que se comparte):** https://calmingsnakes.github.io/nat-bday/
- **ICS directo:** https://calmingsnakes.github.io/nat-bday/nat-bday.ics (`content-type: text/calendar`)
- **Suscripción:** `webcal://calmingsnakes.github.io/nat-bday/nat-bday.ics`

## Cómo funciona el "el lugar se define después"

| Quien lo agrega con… | ¿Recibe el lugar cuando se defina? |
|---|---|
| `webcal://` (suscribirse) | **Sí** — iOS refresca calendarios suscritos y aparece solo |
| `https://…/nat-bday.ics` (sólo agregar) | No — es una copia fija; hay que reabrir la liga |

## Actualizar el lugar / la hora

Editar `make_ics.py` (bloque `EDITA AQUI`), **subir `SEQ` en 1** y correr:

```bash
bash deploy.sh
```

`deploy.sh` regenera el `.ics` (con autocontrol de formato RFC 5545: CRLF, plegado a 75
octetos, bloques BEGIN/END) y hace push a `main`; GitHub Pages lo publica en ~1 min.
Si el lugar cambia, también actualizar el chip `.loc` de `index.html`.
