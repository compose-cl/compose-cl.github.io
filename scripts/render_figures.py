"""Render external manuscript figures as PNGs without changing their design.

Run: python3 scripts/render_figures.py --source-dir /path/to/manuscript/figures
Dependency: PyMuPDF. Source PDFs stay outside the website repository.
"""

import argparse
from pathlib import Path

import fitz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True, help="External directory containing the manuscript figure PDFs.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = args.source_dir.resolve()
    if source == root or root in source.parents:
        parser.error("Source PDFs must remain outside the website repository.")
    figures = {
        "survival": "survival.pdf",
        "anchors-allocation": "anchors_allocation_intro_figure.pdf",
        "factorial": "fig_factorial_matrix.pdf",
        "sho-results": "sho_results.pdf",
    }
    for filename in figures.values():
        if not (source / filename).is_file():
            parser.error(f"Missing source figure: {source / filename}")
    for name, filename in figures.items():
        with fitz.open(source / filename) as document:
            page = document[0]
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2400 / page.rect.width, 2400 / page.rect.width), alpha=False)
            output = root / "static" / "images" / f"{name}.png"
            pixmap.save(output)
            print(f"{output.name}: {pixmap.width} x {pixmap.height}")


if __name__ == "__main__":
    main()
