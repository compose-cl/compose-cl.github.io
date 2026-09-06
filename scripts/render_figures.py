"""Render the published figure PDFs for the web without changing their design.

Run from the repository root: python3 scripts/render_figures.py
Dependency: PyMuPDF. PDFs are kept alongside their web renderings for download.
"""

from pathlib import Path

import fitz


def main():
    root = Path(__file__).resolve().parents[1]
    for name in ("survival", "anchors-allocation", "factorial", "sho-results"):
        with fitz.open(root / "static" / "figures" / f"{name}.pdf") as document:
            page = document[0]
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2400 / page.rect.width, 2400 / page.rect.width), alpha=False)
            output = root / "static" / "images" / f"{name}.png"
            pixmap.save(output)
            print(f"{output.name}: {pixmap.width} x {pixmap.height}")


if __name__ == "__main__":
    main()
