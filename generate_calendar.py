import yaml
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import uuid

TZ_AR = ZoneInfo("America/Argentina/Buenos_Aires")

def ics_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")

def dtstamp_utc() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

data = yaml.safe_load(Path("events.yaml").read_text(encoding="utf-8"))
events = data.get("events", [])

docs = Path("docs")
docs.mkdir(exist_ok=True)

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//alist-calendar//weekly//ES",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Eventos A-List (confirmados) — Argentina (GMT-3)",
    "X-WR-TIMEZONE:America/Argentina/Buenos_Aires",
]
stamp = dtstamp_utc()

for ev in events:
    title = ev["title"]
    date_str = ev["date"]
    start_local = ev.get("start_local")
    tz_local = ev.get("tz_local")
    duration = int(ev.get("duration_minutes", 60))
    location = ev.get("location", "")
    broadcast = ev.get("broadcast", {})
    people = ev.get("confirmed_people", {})
    notes = ev.get("notes", [])

    lines += ["BEGIN:VEVENT", f"UID:{uuid.uuid4()}@alist-calendar", f"DTSTAMP:{stamp}"]
    lines.append(f"SUMMARY:{ics_escape(title)}")
    if location:
        lines.append(f"LOCATION:{ics_escape(location)}")

    desc_lines = []
    if start_local and tz_local:
        local_tz = ZoneInfo(tz_local)
        local_dt = datetime.fromisoformat(f"{date_str}T{start_local}:00").replace(tzinfo=local_tz)
        ar_start = local_dt.astimezone(TZ_AR)
        ar_end = (local_dt + timedelta(minutes=duration)).astimezone(TZ_AR)

        # SOLO hora Argentina en la descripción
        desc_lines.append(f"Hora Argentina (GMT-3): {ar_start.strftime('%d/%m %H:%M')}–{ar_end.strftime('%H:%M')}")

        lines.append(f"DTSTART;TZID=America/Argentina/Buenos_Aires:{fmt_dt(ar_start)}")
        lines.append(f"DTEND;TZID=America/Argentina/Buenos_Aires:{fmt_dt(ar_end)}")
    else:
        # all-day
        d0 = datetime.fromisoformat(date_str).date()
        lines.append(f"DTSTART;VALUE=DATE:{d0.strftime('%Y%m%d')}")
        lines.append(f"DTEND;VALUE=DATE:{(d0 + timedelta(days=1)).strftime('%Y%m%d')}")
        desc_lines.append("Hora Argentina: por anunciar (evento sin horario oficial publicado).")

    tv = broadcast.get("tv", [])
    streaming = broadcast.get("streaming", [])
    if tv:
        desc_lines.append("TV: " + ", ".join(tv))
    if streaming:
        desc_lines.append("Streaming: " + ", ".join(streaming))

    red = broadcast.get("red_carpet", {})
    if red.get("confirmed"):
        where = red.get("where", "")
        desc_lines.append("Red carpet confirmado: " + (where or "Sí (detalle por anunciar)"))
    else:
        desc_lines.append("Red carpet: no confirmado oficialmente.")

    def fmt_people(label, arr):
        if arr:
            desc_lines.append(f"{label}: " + ", ".join(arr))
        else:
            desc_lines.append(f"{label}: (sin confirmaciones oficiales publicadas)")

    fmt_people("Celebrities A-list confirmadas", people.get("a_list", []))
    fmt_people("Celebrities B-list confirmadas", people.get("b_list", []))
    fmt_people("Argentinos confirmados", people.get("argentines", []))

    for n in notes:
        desc_lines.append(n)

    desc = "\n".join(desc_lines)
    lines.append("DESCRIPTION:" + ics_escape(desc))

    lines.append("END:VEVENT")

lines.append("END:VCALENDAR")
(docs / "calendar.ics").write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")

# Archivo “keep-alive” para que GitHub no desactive el cron por inactividad
(docs / "last_updated.txt").write_text(datetime.utcnow().isoformat() + "Z\n", encoding="utf-8")
print("OK: docs/calendar.ics actualizado")
