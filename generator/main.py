from __future__ import annotations

import html
import math
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "generated"


PALETTE = {
    "ink": "#07130f",
    "panel": "#0b211a",
    "paper": "#f7f5ea",
    "muted": "#b8cec5",
    "green": "#00e6a8",
    "blue": "#63d8ff",
    "lime": "#d8ff6a",
    "line": "#245145",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap(text: str, limit: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        next_value = current + char
        weight = sum(2 if ord(c) > 127 else 1 for c in next_value)
        if weight > limit and current:
            lines.append(current)
            current = char
        else:
            current = next_value
    if current:
        lines.append(current)
    return lines


def svg_frame(width: int, height: int, title: str, body: str) -> str:
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">Generated profile visual for siuserxiaowei.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{width}" y2="{height}">
      <stop offset="0" stop-color="#08261d"/>
      <stop offset="0.58" stop-color="#07130f"/>
      <stop offset="1" stop-color="#092f3a"/>
    </linearGradient>
    <radialGradient id="pulse" cx="50%" cy="36%" r="70%">
      <stop offset="0" stop-color="#00e6a8" stop-opacity="0.28"/>
      <stop offset="0.45" stop-color="#63d8ff" stop-opacity="0.09"/>
      <stop offset="1" stop-color="#07130f" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="{width}" height="{height}" rx="28" fill="url(#bg)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="27" stroke="#2e6b5a" stroke-opacity="0.72"/>
  <rect width="{width}" height="{height}" rx="28" fill="url(#pulse)"/>
  <g opacity="0.24">
    {grid(width, height)}
  </g>
  {body}
</svg>
"""


def grid(width: int, height: int) -> str:
    lines = []
    for x in range(40, width, 40):
        lines.append(f'<path d="M{x} 0V{height}" stroke="#6bdcc6" stroke-width="0.6"/>')
    for y in range(40, height, 40):
        lines.append(f'<path d="M0 {y}H{width}" stroke="#6bdcc6" stroke-width="0.6"/>')
    return "\n    ".join(lines)


def text_lines(lines: list[str], x: int, y: int, size: int, color: str, weight: int = 500, gap: int = 1) -> str:
    items = []
    for idx, line in enumerate(lines):
        items.append(
            f'<text x="{x}" y="{y + idx * int(size * (1.35 + gap * 0.05))}" fill="{color}" '
            f'font-family="Avenir Next, Noto Sans SC, PingFang SC, sans-serif" '
            f'font-size="{size}" font-weight="{weight}">{esc(line)}</text>'
        )
    return "\n".join(items)


def render_header(data: dict) -> str:
    p = data["profile"]
    body = f"""
  <g transform="translate(52 48)">
    <text x="0" y="0" fill="{PALETTE['green']}" font-family="Menlo, Consolas, monospace" font-size="15" letter-spacing="4">LEARNING SYSTEM / AI BEGINNER BUILD LOG</text>
    <text x="0" y="78" fill="{PALETTE['paper']}" font-family="Georgia, STSong, serif" font-size="50" font-weight="700">小白学 AI，也能搭出</text>
    <text x="0" y="134" fill="{PALETTE['paper']}" font-family="Georgia, STSong, serif" font-size="50" font-weight="700">自己的工具系统。</text>
    {text_lines(wrap(p["story"], 54), 2, 178, 20, PALETTE["muted"], 500)}
    <rect x="0" y="236" width="304" height="46" rx="23" fill="#0d3027" stroke="#3b7a68"/>
    <text x="22" y="266" fill="{PALETTE['lime']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="17" font-weight="700">{esc(p['subtitle'])}</text>
    <text x="0" y="342" fill="{PALETTE['blue']}" font-family="Menlo, Consolas, monospace" font-size="15">{esc(p['website'])}</text>
  </g>
  <g transform="translate(610 70)">
    <circle cx="128" cy="128" r="108" stroke="#63d8ff" stroke-opacity="0.35"/>
    <circle cx="128" cy="128" r="70" stroke="#00e6a8" stroke-opacity="0.36"/>
    <path d="M128 22C200 52 236 92 235 156C184 146 154 174 128 236C102 174 72 146 21 156C20 92 56 52 128 22Z" fill="#0e342a" stroke="#00e6a8" stroke-width="2"/>
    <circle cx="128" cy="128" r="10" fill="#d8ff6a" filter="url(#glow)"/>
    <circle cx="62" cy="90" r="5" fill="#63d8ff"/>
    <circle cx="204" cy="96" r="5" fill="#00e6a8"/>
    <circle cx="92" cy="194" r="5" fill="#d8ff6a"/>
    <circle cx="196" cy="192" r="5" fill="#63d8ff"/>
    <path d="M62 90L128 128L204 96M128 128L92 194M128 128L196 192" stroke="#79f5db" stroke-opacity="0.56"/>
    <text x="16" y="292" fill="{PALETTE['paper']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="17" font-weight="800">Learning notes -> working tools</text>
  </g>
"""
    return svg_frame(920, 430, "学习者星图", body)


def render_radar(data: dict) -> str:
    tracks = data["tracks"]
    cx, cy = 210, 176
    radius = 116
    angles = [-90, 30, 150]
    rings = []
    for scale in [0.33, 0.66, 1.0]:
        pts = []
        for angle in angles:
            rad = math.radians(angle)
            pts.append((cx + math.cos(rad) * radius * scale, cy + math.sin(rad) * radius * scale))
        rings.append('<polygon points="{}" fill="none" stroke="#4d9582" stroke-opacity="0.5"/>'.format(" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    values = []
    for track, angle in zip(tracks, angles):
        rad = math.radians(angle)
        value = radius * int(track["score"]) / 100
        values.append((cx + math.cos(rad) * value, cy + math.sin(rad) * value))
    track_rows = []
    for idx, track in enumerate(tracks):
        y = 88 + idx * 92
        track_rows.append(f"""
    <g transform="translate(472 {y})">
      <rect x="0" y="0" width="370" height="68" rx="16" fill="#0c2a23" stroke="#2e6b5a"/>
      <circle cx="24" cy="34" r="8" fill="{esc(track['color'])}"/>
      <text x="44" y="26" fill="{PALETTE['paper']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="19" font-weight="800">{esc(track['name'])}</text>
      <text x="44" y="50" fill="{PALETTE['muted']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="13">{esc(track['summary'])}</text>
    </g>""")
    body = f"""
  <text x="48" y="54" fill="{PALETTE['green']}" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="4">CAPABILITY RADAR</text>
  <text x="48" y="91" fill="{PALETTE['paper']}" font-family="Georgia, STSong, serif" font-size="36" font-weight="700">三条能力主线</text>
  <g>
    {' '.join(rings)}
    <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - radius}" stroke="#63d8ff" stroke-opacity="0.45"/>
    <line x1="{cx}" y1="{cy}" x2="{cx + radius * 0.866:.1f}" y2="{cy + radius * 0.5:.1f}" stroke="#63d8ff" stroke-opacity="0.45"/>
    <line x1="{cx}" y1="{cy}" x2="{cx - radius * 0.866:.1f}" y2="{cy + radius * 0.5:.1f}" stroke="#63d8ff" stroke-opacity="0.45"/>
    <polygon points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in values)}" fill="#00e6a8" fill-opacity="0.22" stroke="#00e6a8" stroke-width="3"/>
    <circle cx="{cx}" cy="{cy}" r="5" fill="#d8ff6a"/>
    <text x="156" y="38" fill="{PALETTE['paper']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="15" font-weight="700">AI 工具实验</text>
    <text x="274" y="267" fill="{PALETTE['paper']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="15" font-weight="700">内容系统</text>
    <text x="34" y="267" fill="{PALETTE['paper']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="15" font-weight="700">视觉设计</text>
  </g>
  {''.join(track_rows)}
"""
    return svg_frame(920, 390, "能力雷达", body)


def render_projects(data: dict) -> str:
    projects = data["projects"][:8]
    coords = [(92, 116), (252, 82), (440, 132), (642, 92), (638, 226), (456, 258), (260, 260), (112, 230)]
    palette = [PALETTE["green"], PALETTE["blue"], PALETTE["lime"], "#8df7d0"]
    labels = {
        "visual-taste-lab": "visual-taste-lab",
        "wechat-to-obsidian": "wechat-to-obsidian",
        "ai-coding-knowledge-framework": "AI 工程纪律",
        "wechat-daily-report-skill": "群日报 Skill",
        "daily-card-public": "daily-card",
        "content-creator-toolkit": "content toolkit",
        "opc-policy": "OPC policy",
        "x-md-composer": "x-md-composer",
    }
    lines = []
    nodes = []
    for idx, project in enumerate(projects):
        x, y = coords[idx]
        if idx:
            px, py = coords[idx - 1]
            lines.append(f'<path d="M{px} {py}C{(px + x) / 2:.1f} {py - 40},{(px + x) / 2:.1f} {y + 40},{x} {y}" stroke="#63d8ff" stroke-opacity="0.25"/>')
        color = palette[idx % len(palette)]
        nodes.append(f"""
    <g transform="translate({x} {y})">
      <circle r="10" fill="{color}" filter="url(#glow)"/>
      <rect x="18" y="-20" width="178" height="42" rx="12" fill="#0c2a23" stroke="#2e6b5a"/>
      <text x="32" y="-2" fill="{PALETTE['paper']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="13" font-weight="800">{esc(labels.get(project['name'], project['name']))}</text>
      <text x="32" y="16" fill="{color}" font-family="Menlo, Consolas, monospace" font-size="11">{esc(project['track'])}</text>
    </g>""")
    body = f"""
  <text x="48" y="54" fill="{PALETTE['green']}" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="4">PROJECT CONSTELLATION</text>
  <text x="48" y="92" fill="{PALETTE['paper']}" font-family="Georgia, STSong, serif" font-size="36" font-weight="700">把学习变成公开作品</text>
  <g transform="translate(28 38)">
    {''.join(lines)}
    {''.join(nodes)}
  </g>
"""
    return svg_frame(920, 370, "项目星座", body)


def render_now(data: dict) -> str:
    metrics = data["metrics"]
    now = data["now"]
    p = data["profile"]
    metric_cards = []
    for idx, item in enumerate(metrics):
        x = 48 + idx * 202
        metric_cards.append(f"""
    <g transform="translate({x} 88)">
      <rect width="178" height="88" rx="18" fill="#0c2a23" stroke="#2e6b5a"/>
      <text x="18" y="36" fill="{PALETTE['lime']}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="28" font-weight="900">{esc(item['value'])}</text>
      <text x="18" y="64" fill="{PALETTE['muted']}" font-family="Menlo, Consolas, monospace" font-size="12">{esc(item['label'])}</text>
    </g>""")
    now_lines = []
    for idx, item in enumerate(now):
        y = 232 + idx * 40
        now_lines.append(f'<text x="86" y="{y}" fill="{PALETTE["paper"]}" font-family="Avenir Next, Noto Sans SC, sans-serif" font-size="20">{esc(item)}</text><circle cx="58" cy="{y - 7}" r="6" fill="{[PALETTE["green"], PALETTE["blue"], PALETTE["lime"]][idx % 3]}"/>')
    body = f"""
  <text x="48" y="54" fill="{PALETTE['green']}" font-family="Menlo, Consolas, monospace" font-size="14" letter-spacing="4">NOW BUILDING</text>
  {''.join(metric_cards)}
  {''.join(now_lines)}
  <text x="48" y="364" fill="{PALETTE['blue']}" font-family="Menlo, Consolas, monospace" font-size="14">{esc(p['philosophy'])}</text>
"""
    return svg_frame(920, 410, "正在构建", body)


def main() -> None:
    data = yaml.safe_load((ROOT / "profile.yml").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "learner-map.svg": render_header(data),
        "capability-radar.svg": render_radar(data),
        "project-constellation.svg": render_projects(data),
        "now-building.svg": render_now(data),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"generated assets/generated/{name}")


if __name__ == "__main__":
    main()
