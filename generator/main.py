from __future__ import annotations

import html
import math
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "generated"

PALETTE = {
    "bg": "#070b13",
    "panel": "#0d1522",
    "panel_2": "#111d2d",
    "line": "#23364d",
    "soft": "#8fa1ba",
    "text": "#f4f7fb",
    "cyan": "#00d9ff",
    "blue": "#4db8ff",
    "purple": "#9b7cff",
    "amber": "#f6a623",
    "green": "#00e6a8",
}

SHORT_LABELS = {
    "visual-taste-lab": "Visual Taste",
    "wechat-to-obsidian": "Obsidian",
    "ai-coding-knowledge-framework": "AI Discipline",
    "wechat-daily-report-skill": "Daily Report",
    "daily-card-public": "Daily Cards",
    "content-creator-toolkit": "Creator Toolkit",
    "opc-policy": "OPC Policy",
    "x-md-composer": "X Composer",
}

LEGACY_FILES = [
    "intro-lab.svg",
    "skill-radar.svg",
    "project-map.svg",
    "now-shipping.svg",
    "learner-map.svg",
    "capability-radar.svg",
    "project-constellation.svg",
    "now-building.svg",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap(text: str, limit: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        width = sum(2 if ord(c) > 127 else 1 for c in candidate)
        if width > limit and current:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def text_lines(lines: list[str], x: int, y: int, size: int, color: str, weight: int = 500) -> str:
    return "\n".join(
        f'<text x="{x}" y="{y + idx * int(size * 1.38)}" fill="{color}" '
        f'font-family="Avenir Next, Noto Sans SC, PingFang SC, sans-serif" '
        f'font-size="{size}" font-weight="{weight}">{esc(line)}</text>'
        for idx, line in enumerate(lines)
    )


def stars(width: int, height: int) -> str:
    points = [
        (35, 74, 1.8, PALETTE["cyan"]), (82, 208, 1.2, PALETTE["soft"]),
        (126, 118, 0.9, PALETTE["amber"]), (164, 246, 1.5, PALETTE["soft"]),
        (208, 48, 1.1, PALETTE["purple"]), (247, 179, 1.0, PALETTE["soft"]),
        (298, 96, 1.3, PALETTE["cyan"]), (344, 255, 1.1, PALETTE["amber"]),
        (387, 137, 1.5, PALETTE["soft"]), (428, 64, 1.0, PALETTE["purple"]),
        (475, 221, 1.2, PALETTE["soft"]), (519, 87, 1.3, PALETTE["cyan"]),
        (562, 152, 1.0, PALETTE["soft"]), (606, 42, 1.5, PALETTE["purple"]),
        (648, 236, 1.1, PALETTE["soft"]), (690, 111, 1.8, PALETTE["cyan"]),
        (734, 203, 1.1, PALETTE["amber"]), (781, 71, 1.2, PALETTE["soft"]),
        (816, 252, 1.7, PALETTE["purple"]),
    ]
    return "\n".join(
        f'<circle cx="{x}" cy="{min(y, height - 18)}" r="{r}" fill="{color}" opacity="0.8"/>'
        for x, y, r, color in points
        if x < width and y < height
    )


def svg_frame(width: int, height: int, title: str, body: str, accent: str) -> str:
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">Custom GitHub profile SVG for siuserxiaowei.</desc>
  <defs>
    <radialGradient id="core" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.36"/>
      <stop offset="0.42" stop-color="#10233b" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#070b13" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="panel" x1="0" y1="0" x2="{width}" y2="{height}">
      <stop offset="0" stop-color="#0d1522"/>
      <stop offset="0.58" stop-color="#09101b"/>
      <stop offset="1" stop-color="#11192a"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="{width}" height="{height}" rx="18" fill="url(#panel)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="17" stroke="#273a52"/>
  <rect width="{width}" height="{height}" rx="18" fill="url(#core)"/>
  <g opacity="0.72">{stars(width, height)}</g>
  {body}
</svg>
"""


def orbit(cx: int, cy: int, rx: int, ry: int, color: str, rotate: int = 0, opacity: float = 0.72) -> str:
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rotate} {cx} {cy})" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-opacity="{opacity}"/>'
    )


def orbit_node(cx: int, cy: int, rx: int, ry: int, angle: int, color: str, rotate: int = 0) -> tuple[float, float, str]:
    rad = math.radians(angle)
    x = rx * math.cos(rad)
    y = ry * math.sin(rad)
    rot = math.radians(rotate)
    px = cx + x * math.cos(rot) - y * math.sin(rot)
    py = cy + x * math.sin(rot) + y * math.cos(rot)
    return px, py, f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{color}" filter="url(#glow)"/>'


def render_galaxy_header(data: dict) -> str:
    profile = data["profile"]
    body = f"""
  <text x="425" y="42" fill="{PALETTE['text']}" text-anchor="middle" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="24" font-weight="800">siuserxiaowei</text>
  <text x="425" y="66" fill="{PALETTE['soft']}" text-anchor="middle" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="15">Beginner to Builder · AI Tools · Knowledge Systems · Visual Design</text>
  <g transform="translate(0 12)">
    {orbit(425, 148, 290, 34, PALETTE["cyan"], -4, 0.58)}
    {orbit(425, 148, 224, 30, PALETTE["amber"], 13, 0.52)}
    {orbit(425, 148, 170, 34, PALETTE["purple"], -17, 0.58)}
    <circle cx="425" cy="148" r="26" fill="#0b1525" stroke="{PALETTE['cyan']}" stroke-width="2"/>
    <circle cx="425" cy="148" r="14" fill="#102744" stroke="{PALETTE['cyan']}" stroke-opacity="0.7"/>
    <text x="425" y="155" fill="{PALETTE['cyan']}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="18" font-weight="800">S</text>
    {orbit_node(425, 148, 290, 34, 18, PALETTE["cyan"], -4)[2]}
    {orbit_node(425, 148, 290, 34, 202, PALETTE["cyan"], -4)[2]}
    {orbit_node(425, 148, 224, 30, 42, PALETTE["amber"], 13)[2]}
    {orbit_node(425, 148, 224, 30, 190, PALETTE["amber"], 13)[2]}
    {orbit_node(425, 148, 170, 34, 96, PALETTE["purple"], -17)[2]}
    {orbit_node(425, 148, 170, 34, 246, PALETTE["purple"], -17)[2]}
    <text x="196" y="126" fill="{PALETTE['purple']}" font-family="Menlo, Consolas, monospace" font-size="13">Codex</text>
    <text x="260" y="169" fill="{PALETTE['blue']}" font-family="Menlo, Consolas, monospace" font-size="13">Python</text>
    <text x="288" y="226" fill="{PALETTE['amber']}" font-family="Menlo, Consolas, monospace" font-size="13">GitHub Pages</text>
    <text x="523" y="110" fill="{PALETTE['cyan']}" font-family="Menlo, Consolas, monospace" font-size="13">Obsidian</text>
    <text x="558" y="169" fill="{PALETTE['amber']}" font-family="Menlo, Consolas, monospace" font-size="13">Automation</text>
    <text x="662" y="152" fill="{PALETTE['cyan']}" font-family="Menlo, Consolas, monospace" font-size="13">Visual Taste</text>
  </g>
  <text x="425" y="282" fill="{PALETTE['soft']}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="14" font-style="italic">"{esc(profile['philosophy'])}"</text>
"""
    return svg_frame(850, 310, "Galaxy Header", body, PALETTE["cyan"])


def render_mission_telemetry(data: dict) -> str:
    metrics = data["metrics"]
    icon_colors = [PALETTE["cyan"], PALETTE["amber"], PALETTE["purple"], PALETTE["cyan"], PALETTE["purple"]]
    columns = []
    for idx, item in enumerate(metrics[:5]):
        x = 60 + idx * 146
        color = icon_colors[idx % len(icon_colors)]
        divider = "" if idx == 0 else f'<path d="M{x - 32} 72V162" stroke="#23364d" stroke-opacity="0.75"/>'
        columns.append(f"""
    {divider}
    <g transform="translate({x} 0)">
      <circle cx="18" cy="69" r="8" fill="none" stroke="{color}" stroke-width="3"/>
      <circle cx="18" cy="69" r="3" fill="{color}"/>
      <text x="18" y="112" fill="{PALETTE['text']}" text-anchor="middle" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="36" font-weight="900">{esc(item['value'])}</text>
      <text x="18" y="142" fill="{PALETTE['soft']}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="3">{esc(item['label'])}</text>
    </g>""")
    body = f"""
  <text x="42" y="55" fill="{PALETTE['soft']}" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="7">MISSION TELEMETRY</text>
  <g>{''.join(columns)}</g>
"""
    return svg_frame(850, 200, "Mission Telemetry", body, PALETTE["purple"])


def render_tech_stack(data: dict) -> str:
    tracks = data["tracks"]
    lanes = []
    for idx, track in enumerate(tracks):
        x = 46 + idx * 262
        color = track["color"]
        tags = track.get("tags", [])[:4]
        chips = []
        for chip_idx, tag in enumerate(tags):
            cx = 22 + (chip_idx % 2) * 108
            cy = 112 + (chip_idx // 2) * 42
            chips.append(f"""
        <rect x="{cx}" y="{cy}" width="96" height="28" rx="14" fill="#0a1320" stroke="{color}" stroke-opacity="0.56"/>
        <text x="{cx + 48}" y="{cy + 19}" fill="{PALETTE['text']}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="10">{esc(tag)}</text>""")
        lanes.append(f"""
    <g transform="translate({x} 72)">
      <rect width="234" height="150" rx="18" fill="#0d1522" stroke="#263951"/>
      <text x="22" y="36" fill="{color}" font-family="Menlo, Consolas, monospace" font-size="12" letter-spacing="3">TRACK 0{idx + 1}</text>
      <text x="22" y="66" fill="{PALETTE['text']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="22" font-weight="850">{esc(track['name'])}</text>
      {''.join(chips)}
    </g>""")
    body = f"""
  <text x="42" y="52" fill="{PALETTE['soft']}" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="7">TECH STACK / LEARNING LANES</text>
  {''.join(lanes)}
"""
    return svg_frame(850, 260, "Tech Stack", body, PALETTE["green"])


def render_projects_constellation(data: dict) -> str:
    projects = data["projects"][:8]
    coords = [(94, 112), (250, 78), (408, 120), (618, 88), (692, 204), (510, 242), (304, 236), (122, 214)]
    colors = [PALETTE["cyan"], PALETTE["blue"], PALETTE["amber"], PALETTE["purple"], PALETTE["green"]]
    paths = []
    nodes = []
    for idx, project in enumerate(projects):
        x, y = coords[idx]
        color = colors[idx % len(colors)]
        if idx:
            px, py = coords[idx - 1]
            paths.append(
                f'<path d="M{px} {py}C{(px + x) / 2:.1f} {py - 52},{(px + x) / 2:.1f} {y + 48},{x} {y}" '
                f'stroke="{color}" stroke-width="1.5" stroke-opacity="0.33"/>'
            )
        nodes.append(f"""
    <g transform="translate({x} {y})">
      <circle r="7.5" fill="{color}" filter="url(#glow)"/>
      <text x="18" y="-4" fill="{PALETTE['text']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="14" font-weight="800">{esc(SHORT_LABELS.get(project['name'], project['name']))}</text>
      <text x="18" y="15" fill="{color}" font-family="Menlo, Consolas, monospace" font-size="10">{esc(project['track'])}</text>
    </g>""")
    body = f"""
  <text x="42" y="52" fill="{PALETTE['soft']}" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="7">PROJECT CONSTELLATION</text>
  <text x="42" y="84" fill="{PALETTE['text']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="22" font-weight="850">From notes to running tools</text>
  <g transform="translate(18 34)">
    {''.join(paths)}
    {''.join(nodes)}
  </g>
  <text x="42" y="304" fill="{PALETTE['soft']}" font-family="Menlo, Consolas, monospace" font-size="13">visual-taste-lab · ai-coding-knowledge-framework · wechat-to-obsidian</text>
"""
    return svg_frame(850, 330, "Project Constellation", body, PALETTE["amber"])


def main() -> None:
    data = yaml.safe_load((ROOT / "profile.yml").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    for legacy in LEGACY_FILES:
        path = OUT / legacy
        if path.exists():
            path.unlink()
    files = {
        "galaxy-header.svg": render_galaxy_header(data),
        "mission-telemetry.svg": render_mission_telemetry(data),
        "tech-stack.svg": render_tech_stack(data),
        "projects-constellation.svg": render_projects_constellation(data),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"generated assets/generated/{name}")


if __name__ == "__main__":
    main()
