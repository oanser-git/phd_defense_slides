#!/usr/bin/env python3

from __future__ import annotations

import html
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
DRAWIO_PATH = ROOT / "adaptation_families_workflow_modification.drawio"

CANVAS_W = 1600
CANVAS_H = 900

COLORS = {
    "D": "#3B82F6",
    "T": "#7C3AED",
    "M": "#C026D3",
    "O": "#0F766E",
    "A": "#D97706",
    "C": "#6B7280",
}

FILLS = {
    "D": "#e6f0ff",
    "T": "#f0e9ff",
    "M": "#fde7ff",
    "O": "#e5f7f5",
    "A": "#fff1df",
    "C": "#eef0f3",
}

LAYOUT = {
    "in": {"x": 40, "y": 320, "w": 240, "h": 96},
    "nids": {"x": 400, "y": 320, "w": 360, "h": 96},
    "thr": {"x": 900, "y": 320, "w": 210, "h": 96},
    "al": {"x": 1260, "y": 320, "w": 240, "h": 96},
    "d": {"x": 55, "y": 78, "w": 260, "h": 98},
    "t": {"x": 365, "y": 78, "w": 250, "h": 98},
    "m": {"x": 665, "y": 78, "w": 250, "h": 98},
    "o": {"x": 965, "y": 78, "w": 300, "h": 98},
    "c": {"x": 1305, "y": 78, "w": 250, "h": 98},
    "a": {"x": 1010, "y": 475, "w": 310, "h": 104},
}

LEGENDS = {
    "D": ("Drift detection", "monitor change in traffic or detector scores", "CADE, OWAD, TRANSCEND"),
    "T": ("Transfer / domain adap.", "reuse knowledge from another context", "ADA, NAEF, DI-NIDS"),
    "M": ("Meta-learning", "learn how to adapt quickly from prior tasks", "FC-Net, PTN-IDS, RETSINA"),
    "O": ("Online / continual learning", "update model weights over time", "AOC-IDS, ENIDrift, ReCDA"),
    "A": ("Active / semi-supervised", "use few labels or pseudo-labels", "Active-SVDD, HITL-IDS, METALS"),
    "C": ("Threshold calibration", "adjust alert cutoff after training", "Bridges, Hundman, MAGPIE"),
}

STAGES = [
    {"name": "stage1", "families": []},
    {"name": "stage2", "families": ["D"]},
    {"name": "stage3", "families": ["D", "T", "M", "O"]},
    {"name": "stage4", "families": ["D", "T", "M", "O", "A"]},
    {"name": "stage5", "families": ["D", "T", "M", "O", "A", "C"]},
]

NODE_MAP = {
    "in": "pipeline",
    "nids": "pipeline",
    "thr": "pipeline",
    "al": "pipeline",
    "d": "D",
    "t": "T",
    "m": "M",
    "o": "O",
    "a": "A",
    "c": "C",
}


def parse_drawio(path: Path) -> dict[str, dict[str, float | str]]:
    tree = ET.parse(path)
    root = tree.getroot()
    cells: dict[str, dict[str, float | str]] = {}
    for cell in root.iter("mxCell"):
        cell_id = cell.attrib.get("id")
        if cell_id not in NODE_MAP:
            continue
        geom = cell.find("mxGeometry")
        if geom is None:
            continue
        cells[cell_id] = {
            "x": float(LAYOUT[cell_id]["x"]),
            "y": float(LAYOUT[cell_id]["y"]),
            "w": float(LAYOUT[cell_id]["w"]),
            "h": float(LAYOUT[cell_id]["h"]),
            "value": html.unescape(cell.attrib.get("value", "")),
        }
    return cells


def badge_x(node: dict[str, float | str]) -> float:
    return float(node["x"]) + float(node["w"]) - 28


def badge_y(node: dict[str, float | str]) -> float:
    return float(node["y"]) - 18


def rounded_rect(x: float, y: float, w: float, h: float, *, stroke: str, fill: str, stroke_width: float = 2.2, radius: int = 18, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="8 7"' if dashed else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" ry="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dash}/>'
    )


def centered_text(x: float, y: float, lines: list[str], *, cls: str) -> str:
    line_gap_map = {
        "nodelabel": 34,
        "famlabel": 30,
        "small": 26,
    }
    line_gap = line_gap_map.get(cls, 24)
    start_y = y - ((len(lines) - 1) * line_gap) / 2
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_gap
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return f'<text x="{x}" y="{start_y}" text-anchor="middle" class="{cls}">{"".join(tspans)}</text>'


def left_text(x: float, y: float, line: str, *, cls: str, color: str | None = None) -> str:
    fill = f' fill="{color}"' if color else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{fill}>{escape(line)}</text>'


def circle(cx: float, cy: float, r: float, *, fill: str, text: str) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
        f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" class="family">{escape(text)}</text>'
    )


def polyline(points: list[tuple[float, float]], *, dashed: bool = False) -> str:
    coords = " ".join(f"{x},{y}" for x, y in points)
    cls = "arrowThin dashed" if dashed else "arrow"
    return f'<polyline points="{coords}" class="{cls}" marker-end="url(#arrowhead)"/>'


def line(x1: float, y1: float, x2: float, y2: float, *, dashed: bool = False) -> str:
    cls = "arrowThin dashed" if dashed else "arrow"
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#arrowhead)"/>'


def curve(start: tuple[float, float], control1: tuple[float, float], control2: tuple[float, float], end: tuple[float, float], *, dashed: bool = False) -> str:
    cls = "arrowThin dashed" if dashed else "arrow"
    return (
        f'<path d="M {start[0]},{start[1]} C {control1[0]},{control1[1]} {control2[0]},{control2[1]} {end[0]},{end[1]}" '
        f'class="{cls}" marker-end="url(#arrowhead)"/>'
    )


def draw_node(node: dict[str, float | str], *, stroke: str = "#5b6770", fill: str = "#ffffff") -> str:
    x = float(node["x"])
    y = float(node["y"])
    w = float(node["w"])
    h = float(node["h"])
    lines = str(node["value"]).splitlines()
    return (
        rounded_rect(x, y, w, h, stroke=stroke, fill=fill, stroke_width=2.8, radius=24) +
        centered_text(x + w / 2, y + h / 2 + 4, lines, cls="nodelabel")
    )


def draw_family(node: dict[str, float | str], letter: str) -> str:
    color = COLORS[letter]
    x = float(node["x"])
    y = float(node["y"])
    w = float(node["w"])
    h = float(node["h"])
    lines = str(node["value"]).splitlines()
    parts = [
        rounded_rect(x, y, w, h, stroke=color, fill=FILLS[letter], stroke_width=3.0, radius=22),
        centered_text(x + w / 2, y + h / 2 + 4, lines, cls="famlabel"),
        circle(badge_x(node), badge_y(node), 20, fill=color, text=letter),
    ]
    return "".join(parts)


def wrap_text(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width) or [text]


def legend_item(letter: str, x: float, y: float, opacity: float = 1.0) -> str:
    color = COLORS[letter]
    title, desc, refs = LEGENDS[letter]
    desc_lines = wrap_text(desc, 26 if letter in {"D", "T", "O", "A", "C"} else 29)
    refs_lines = wrap_text(refs, 30)
    parts = [circle(x, y, 16, fill=color, text=letter)]
    text_x = x + 34
    parts.append(left_text(text_x, y + 6, title, cls="legendtitle", color=color))
    line_y = y + 34
    for line_text in desc_lines:
        parts.append(left_text(text_x, line_y, line_text, cls="legenddesc"))
        line_y += 32
    for ref_line in refs_lines:
        parts.append(left_text(text_x, line_y, ref_line, cls="tiny"))
        line_y += 24
    return f'<g opacity="{opacity}">{"".join(parts)}</g>'


def draw_ad_box(thr: dict[str, float | str]) -> str:
    x = float(thr["x"]) - 40
    y = 250
    w = float(thr["w"]) + 120
    h = 210
    parts = [rounded_rect(x, y, w, h, stroke="#b8bfc5", fill="none", stroke_width=2.4, radius=26, dashed=True)]
    parts.append(f'<text x="{x + w/2}" y="{y + 36}" text-anchor="middle" class="small">Anomaly Detection NIDS</text>')
    return "".join(parts)


def stage_svg(cells: dict[str, dict[str, float | str]], visible: list[str]) -> str:
    node_in = cells["in"]
    node_nids = cells["nids"]
    node_thr = cells["thr"]
    node_al = cells["al"]

    elements: list[str] = []
    elements.append(draw_ad_box(node_thr))
    elements.extend([
        draw_node(node_in),
        draw_node(node_nids),
        draw_node(node_thr),
        draw_node(node_al),
        line(float(node_in["x"]) + float(node_in["w"]), float(node_in["y"]) + float(node_in["h"]) / 2, float(node_nids["x"]), float(node_nids["y"]) + float(node_nids["h"]) / 2),
        line(float(node_nids["x"]) + float(node_nids["w"]), float(node_nids["y"]) + float(node_nids["h"]) / 2, float(node_thr["x"]), float(node_thr["y"]) + float(node_thr["h"]) / 2),
        line(float(node_thr["x"]) + float(node_thr["w"]), float(node_thr["y"]) + float(node_thr["h"]) / 2, float(node_al["x"]), float(node_al["y"]) + float(node_al["h"]) / 2),
    ])

    if "D" in visible:
        d = cells["d"]
        elements.append(draw_family(d, "D"))
        elements.append(curve(
            (float(d["x"]) + float(d["w"]) / 2, float(d["y"]) + float(d["h"])),
            (float(d["x"]) + float(d["w"]) / 2 - 10, float(d["y"]) + float(d["h"]) + 70),
            (float(node_in["x"]) + float(node_in["w"]) / 2 - 10, float(node_in["y"]) - 60),
            (float(node_in["x"]) + float(node_in["w"]) / 2, float(node_in["y"])),
            dashed=True,
        ))
        elements.append(curve(
            (float(d["x"]) + float(d["w"]), float(d["y"]) + 38),
            (float(d["x"]) + float(d["w"]) + 85, float(d["y"]) + 88),
            (float(node_nids["x"]) + 30, float(node_nids["y"]) - 78),
            (float(node_nids["x"]) + 30, float(node_nids["y"])),
            dashed=True,
        ))

    if "T" in visible:
        t = cells["t"]
        elements.append(draw_family(t, "T"))
        elements.append(curve(
            (float(t["x"]) + float(t["w"]) / 2, float(t["y"]) + float(t["h"])),
            (float(t["x"]) + float(t["w"]) / 2 + 10, float(t["y"]) + float(t["h"]) + 70),
            (float(node_nids["x"]) + 80, float(node_nids["y"]) - 70),
            (float(node_nids["x"]) + 80, float(node_nids["y"])),
            dashed=True,
        ))

    if "M" in visible:
        m = cells["m"]
        elements.append(draw_family(m, "M"))
        elements.append(curve(
            (float(m["x"]) + float(m["w"]) / 2, float(m["y"]) + float(m["h"])),
            (float(m["x"]) + float(m["w"]) / 2, float(m["y"]) + float(m["h"]) + 80),
            (float(node_nids["x"]) + float(node_nids["w"]) / 2, float(node_nids["y"] - 70)),
            (float(node_nids["x"]) + float(node_nids["w"]) / 2, float(node_nids["y"])),
            dashed=True,
        ))

    if "O" in visible:
        o = cells["o"]
        elements.append(draw_family(o, "O"))
        elements.append(curve(
            (float(o["x"]) + float(o["w"]) / 2, float(o["y"]) + float(o["h"])),
            (float(o["x"]) + float(o["w"]) / 2 - 18, 242),
            (float(node_nids["x"]) + float(node_nids["w"]) - 40, 238),
            (float(node_nids["x"]) + float(node_nids["w"]) - 50, float(node_nids["y"])),
            dashed=True,
        ))

    if "A" in visible:
        a = cells["a"]
        elements.append(draw_family(a, "A"))
        elements.append(curve(
            (float(node_al["x"]) + float(node_al["w"]) / 2, float(node_al["y"] + float(node_al["h"]))),
            (float(node_al["x"]) + float(node_al["w"]) / 2 - 30, float(node_al["y"]) + float(node_al["h"]) + 26),
            (float(a["x"]) + float(a["w"]) * 0.82, float(a["y"]) - 30),
            (float(a["x"]) + float(a["w"]) * 0.72, float(a["y"])),
            dashed=True,
        ))
        elements.append(curve(
            (float(a["x"]), float(a["y"]) + float(a["h"]) / 2),
            (float(a["x"]) - 100, float(a["y"]) + float(a["h"]) / 2 + 20),
            (float(node_nids["x"]) + float(node_nids["w"]) / 2 + 40, float(node_nids["y"]) + float(node_nids["h"]) + 110),
            (float(node_nids["x"]) + float(node_nids["w"]) / 2, float(node_nids["y"]) + float(node_nids["h"])),
            dashed=True,
        ))

    if "C" in visible:
        c = cells["c"]
        elements.append(draw_family(c, "C"))
        elements.append(curve(
            (float(c["x"]) + float(c["w"]) / 2, float(c["y"]) + float(c["h"])),
            (float(c["x"]) + float(c["w"]) / 2 + 6, 246),
            (float(node_thr["x"]) + float(node_thr["w"]) + 120, 240),
            (float(node_thr["x"]) + float(node_thr["w"]) * 0.74, float(node_thr["y"])),
            dashed=True,
        ))

    legend_positions = {
        "D": (90, 620),
        "T": (570, 620),
        "M": (1050, 620),
        "O": (90, 780),
        "A": (570, 780),
        "C": (1050, 780),
    }
    for letter in visible:
        if letter in legend_positions:
            elements.append(legend_item(letter, *legend_positions[letter]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}">
  <defs>
    <style>
      .nodelabel {{ font: 700 28px 'DejaVu Sans', Arial, sans-serif; fill: #2c3e43; }}
      .famlabel {{ font: 700 24px 'DejaVu Sans', Arial, sans-serif; fill: #2c3e43; }}
      .small {{ font: 700 24px 'DejaVu Sans', Arial, sans-serif; fill: #5f6870; }}
      .tiny {{ font: 400 20px 'DejaVu Sans', Arial, sans-serif; fill: #314047; }}
      .legendtitle {{ font: 700 30px 'DejaVu Sans', Arial, sans-serif; }}
      .legenddesc {{ font: 400 30px 'DejaVu Sans', Arial, sans-serif; fill: #314047; }}
      .family {{ font: 700 22px 'DejaVu Sans', Arial, sans-serif; fill: white; }}
      .arrow {{ stroke: #55636c; stroke-width: 4.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
      .arrowThin {{ stroke: #55636c; stroke-width: 3.1; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
      .dashed {{ stroke-dasharray: 8 7; }}
    </style>
    <marker id="arrowhead" markerWidth="8" markerHeight="8" refX="6.8" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#55636c"/>
    </marker>
  </defs>
  {''.join(elements)}
</svg>
'''


def main() -> None:
    cells = parse_drawio(DRAWIO_PATH)
    for stage in STAGES:
        svg_path = ROOT / f"adaptation_families_workflow_{stage['name']}.svg"
        svg_path.write_text(stage_svg(cells, stage["families"]), encoding="utf-8")


if __name__ == "__main__":
    main()
