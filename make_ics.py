#!/usr/bin/env python3
"""Genera nat-bday.ics para el cumple de Nat (31 OCT 2026).

Para actualizar el evento (lugar, hora, descripcion):
  1. edita los campos de abajo
  2. sube SEQ en 1
  3. corre:  python3 make_ics.py
  4. sube el cambio:  git add -A ; git commit -m update ; git push
Los que se SUSCRIBIERON (webcal) ven el cambio solos.
"""

import pathlib

# ------------------------------------------------------------------ EDITA AQUI
SUMMARY = "🩸2️⃣9️⃣ Nat's Vampire Bday🩸31 OCT - Final Chapter of my 20s"
LOCATION = "Por definir 🔜"
START = "20261031T200000"   # 31 oct 2026, 20:00 (hora CDMX)
END = "20261101T030000"     # 1 nov 2026, 03:00 (madrugada)
DESCRIPTION = (
    "Final Chapter of my 20s 🩸\n"
    "Dress code: vampiro.\n"
    "Lugar por definir — si te suscribiste al calendario, la ubicación aparece aquí solita."
)
REMINDER_MINUTES = 120      # aviso X min antes. Pon 0 para no poner alarma.
SEQ = 1                     # SUBE ESTO EN 1 EN CADA CAMBIO (obliga el refresco)
# ------------------------------------------------------------------------------

UID = "nat-vampire-bday-31oct2026@calmingsnakes.github.io"
TZID = "America/Mexico_City"

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:America/Mexico_City
BEGIN:STANDARD
DTSTART:19700101T000000
TZOFFSETFROM:-060000
TZOFFSETTO:-060000
TZNAME:CST
END:STANDARD
END:VTIMEZONE"""


def esc(text: str) -> str:
    """Escapa valores de texto segun RFC 5545."""
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def fold(line: str) -> str:
    """Pliega a maximo 75 octetos por linea fisica, sin partir multibyte."""
    if len(line.encode("utf-8")) <= 75:
        return line
    parts, cur, limit = [], b"", 75
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > limit:
            parts.append(cur)
            cur = b""
            limit = 74  # la linea de continuacion gasta 1 octeto en el espacio
        cur += b
    parts.append(cur)
    return "\r\n ".join(p.decode("utf-8") for p in parts)


lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//calmingsnakes//nat-bday//ES",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:🩸 Nat's Vampire Bday",
    "X-WR-TIMEZONE:" + TZID,
]
lines += VTIMEZONE.split("\n")
lines += [
    "BEGIN:VEVENT",
    "UID:" + UID,
    "DTSTAMP:20261006T215200Z",
    "SEQUENCE:" + str(SEQ),
    "DTSTART;TZID=" + TZID + ":" + START,
    "DTEND;TZID=" + TZID + ":" + END,
    "SUMMARY:" + esc(SUMMARY),
    "LOCATION:" + esc(LOCATION),
    "DESCRIPTION:" + esc(DESCRIPTION),
    "STATUS:CONFIRMED",
    "TRANSP:OPAQUE",
]
if REMINDER_MINUTES:
    lines += [
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        "DESCRIPTION:" + esc(SUMMARY),
        "TRIGGER:-PT" + str(REMINDER_MINUTES) + "M",
        "END:VALARM",
    ]
lines += ["END:VEVENT", "END:VCALENDAR"]

ics = "\r\n".join(fold(l) for l in lines) + "\r\n"

# --- autocontrol: nada de LF sueltos ni lineas fisicas de mas de 75 octetos ---
physical = ics.split("\r\n")
assert ics.count("\n") == ics.count("\r\n"), "hay LF sueltos (finales de linea mezclados)"
assert all(len(l.encode("utf-8")) <= 75 for l in physical), "hay lineas de mas de 75 octetos"
assert physical[0] == "BEGIN:VCALENDAR" and physical[-2] == "END:VCALENDAR", "estructura rota"
for tag in ("BEGIN:VEVENT", "END:VEVENT", "BEGIN:VTIMEZONE", "END:VTIMEZONE"):
    assert physical.count(tag) == 1, f"falta o sobra {tag}"

out = pathlib.Path(__file__).with_name("nat-bday.ics")
out.write_bytes(ics.encode("utf-8"))
print("escrito:", out, len(ics.encode("utf-8")), "bytes |", len(physical) - 1, "lineas | validacion OK")
