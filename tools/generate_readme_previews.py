from __future__ import annotations

import re
import textwrap
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_OUTPUTS = ROOT / "sample_outputs"
IMAGE_DIR = ROOT / "docs" / "images"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_height(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    width: int,
    font: ImageFont.ImageFont,
    fill: str,
    *,
    line_gap: int = 7,
    bullet: bool = False,
) -> int:
    x, y = xy
    prefix = "- " if bullet else ""
    wrapped = wrap_by_pixels(draw, text, font, width - int(draw.textlength(prefix, font=font))) or [""]
    for index, line in enumerate(wrapped):
        line_prefix = prefix if index == 0 else "  " if bullet else ""
        draw.text((x, y), f"{line_prefix}{line}", font=font, fill=fill)
        y += text_height(draw, line, font) + line_gap
    return y


def wrap_by_pixels(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue

        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if draw.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def markdown_sections(path: Path) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title = ""
    current_lines: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            current_title = line.removeprefix("# ").strip()
            continue
        if line.startswith("## "):
            if current_title and current_lines:
                sections.append((current_title, current_lines))
            current_title = line.removeprefix("## ").strip()
            current_lines = []
            continue
        current_lines.append(line)
    if current_title and current_lines:
        sections.append((current_title, current_lines))
    return sections


def render_markdown_card(source: Path, target: Path, subtitle: str) -> None:
    width = 1280
    padding = 56
    title_font = load_font(FONT_BOLD, 42)
    section_font = load_font(FONT_BOLD, 25)
    body_font = load_font(FONT_REGULAR, 22)
    small_font = load_font(FONT_REGULAR, 18)

    sections = markdown_sections(source)
    canvas = Image.new("RGB", (width, 1600), "#f5f7fb")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((30, 30, width - 30, 1560), radius=22, fill="#ffffff", outline="#d7dde8", width=2)
    draw.rectangle((30, 30, width - 30, 142), fill="#172033")
    draw.text((padding, 63), source.stem.replace("_", " ").title(), font=title_font, fill="#ffffff")
    draw.text((padding, 118), subtitle, font=small_font, fill="#b8c3d8")

    y = 190
    max_content_width = width - (padding * 2)
    for title, lines in sections[:7]:
        draw.text((padding, y), title, font=section_font, fill="#172033")
        y += 38
        for line in lines[:5]:
            bullet = line.startswith("- ")
            clean = re.sub(r"^- ", "", line)
            color = "#354052" if not title.lower().startswith("metadata") else "#596579"
            y = draw_wrapped(draw, clean, (padding, y), max_content_width, body_font, color, bullet=bullet)
        y += 22

    final = canvas.crop((0, 0, width, min(y + 70, 1600)))
    final.save(target)


def read_xlsx_rows(path: Path) -> list[list[str]]:
    namespace = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall("m:si", namespace):
                shared_strings.append("".join(text.text or "" for text in item.findall(".//m:t", namespace)))

        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows: list[list[str]] = []
        for row in sheet.findall(".//m:sheetData/m:row", namespace):
            values: list[str] = []
            for cell in row.findall("m:c", namespace):
                value = cell.find("m:v", namespace)
                if value is None:
                    values.append("")
                elif cell.attrib.get("t") == "s":
                    values.append(shared_strings[int(value.text or "0")])
                else:
                    values.append(value.text or "")
            rows.append(values)
        return rows


def render_table_card(source: Path, target: Path, title: str) -> None:
    rows = read_xlsx_rows(source)
    headers = rows[0]
    data_rows = rows[1:]
    width = 1640
    padding = 48
    title_font = load_font(FONT_BOLD, 42)
    header_font = load_font(FONT_BOLD, 19)
    body_font = load_font(FONT_REGULAR, 18)
    small_font = load_font(FONT_REGULAR, 18)

    canvas = Image.new("RGB", (width, 780), "#f5f7fb")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((30, 30, width - 30, 720), radius=22, fill="#ffffff", outline="#d7dde8", width=2)
    draw.rectangle((30, 30, width - 30, 142), fill="#172033")
    draw.text((padding, 63), title, font=title_font, fill="#ffffff")
    draw.text((padding, 118), "Sample Excel output rendered for README preview", font=small_font, fill="#b8c3d8")

    table_x = padding
    table_y = 190
    table_width = width - (padding * 2)
    if len(headers) == 6 and headers[0].startswith("Requirement"):
        ratios = [0.14, 0.12, 0.28, 0.16, 0.15, 0.15]
    else:
        ratios = [0.13, 0.26, 0.20, 0.14, 0.20, 0.07]
    col_widths = [int(table_width * ratio) for ratio in ratios]
    col_widths[-1] += table_width - sum(col_widths)
    row_height = 86

    x = table_x
    for index, header in enumerate(headers):
        col_width = col_widths[index]
        draw.rectangle((x, table_y, x + col_width, table_y + row_height), fill="#eaf0f8", outline="#cfd8e6")
        draw_wrapped(draw, header, (x + 14, table_y + 20), col_width - 28, header_font, "#172033", line_gap=3)
        x += col_width

    for row_index, row in enumerate(data_rows[:4], start=1):
        y = table_y + row_index * row_height
        fill = "#ffffff" if row_index % 2 else "#f8fafc"
        x = table_x
        for col_index, value in enumerate(row):
            col_width = col_widths[col_index]
            draw.rectangle((x, y, x + col_width, y + row_height), fill=fill, outline="#d7dde8")
            draw_wrapped(draw, value, (x + 14, y + 18), col_width - 28, body_font, "#354052", line_gap=3)
            x += col_width

    final = canvas.crop((0, 0, width, table_y + row_height * (len(data_rows[:4]) + 1) + 60))
    final.save(target)


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    render_markdown_card(
        SAMPLE_OUTPUTS / "01_executive_summary.md",
        IMAGE_DIR / "executive-summary.png",
        "Markdown output for leadership review",
    )
    render_table_card(
        SAMPLE_OUTPUTS / "02_requirements_matrix.xlsx",
        IMAGE_DIR / "requirements-matrix.png",
        "Requirements Matrix",
    )
    render_table_card(
        SAMPLE_OUTPUTS / "03_risk_register.xlsx",
        IMAGE_DIR / "risk-register.png",
        "Risk Register",
    )
    render_markdown_card(
        SAMPLE_OUTPUTS / "05_go_no_go.md",
        IMAGE_DIR / "go-no-go.png",
        "Decision support output for pre-sales qualification",
    )


if __name__ == "__main__":
    main()
