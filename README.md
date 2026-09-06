# ComposeCL project website

Academic project page for **Continual Learning Mechanisms Compose for Long-Horizon Memorization**, by Zheyuan Zhang, Alvin Zhang, Daniel Khashabi, and Tianmin Shu, Johns Hopkins University.

Website: <https://compose-cl.github.io/>

## Local preview

No build step or runtime CDN dependencies are required.

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000>. JavaScript enhances the page with a 16-combination results explorer and a BibTeX copy button. All research content and figures remain readable without JavaScript.

## Content and release links

- `index.html`: title, authors, abstract, captions, project citation, metadata, and release buttons.
- `static/css/project.css`: project-specific styles and responsive layouts.
- `static/js/project.js`: accessible results explorer and citation-copy behavior.
- `static/js/results-data.js`: final retention means and standard deviations for the 16 factorial combinations. Values are transcribed at the manuscript's one-decimal precision from the complete results tables for Symbol-QA, LLM-QA, and Real-QA.
- `static/images/`: web-rendered figures, favicon, and social preview.
- `scripts/render_figures.py`: reproducible PNG export from an external directory of manuscript figures. Requires PyMuPDF. Run `python3 scripts/render_figures.py --source-dir /path/to/manuscript/figures`. Source PDFs stay outside this repository and are never copied into it.
- `scripts/check_site.py`: Playwright browser checks for all 16 combinations, keyboard controls, citation copying, local links, and five viewport widths. Pass `--render-social` to regenerate the social preview too.
- `scripts/social-preview.html`: source layout for the 1200 × 630 social preview, rendered with a browser screenshot.

Paper and code are **not released yet**. Their buttons are intentionally disabled and labeled “Coming soon.” Upon release, replace each disabled button with an anchor to the actual public URL, remove the coming-soon label, and update the project citation if needed. Do not link a private development repository or an unverified manuscript PDF.

The main result uses the same fixed composition on all datasets: SI + SD + generative replay + merged LoRA. Its final retention is 18.5%, 41.8%, and 44.3%, respectively, and it ranks among the top 3 of the 16 factorial methods on every dataset. Dataset-specific winners are separate comparisons.

The interactive factorial comparison is the first section below the title block. Only PNG figure assets are published. PDFs are excluded from the website and ignored by Git. The BibTeX entry uses `@article` without a URL field.

## Deployment

This is a plain static GitHub Pages site. In the repository settings, choose **Pages → Deploy from a branch → main → / (root)** if Pages has not been enabled. Pushing `main` then updates <https://compose-cl.github.io/>. `.nojekyll` disables Jekyll processing. No package installation or secrets are needed to serve the website.

## Provenance and attribution

Built from [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template), upstream commit `d38af1c`, itself based on [Nerfies](https://nerfies.github.io/). The template's Bulma layout, academic title/author/resource blocks, figure/abstract sections, BibTeX component, and attribution footer are retained and adapted. The upstream `static/css/bulma.min.css` and `static/css/index.css` are vendored unchanged. Unused carousel, video, analytics, third-party viewer, and icon dependencies are omitted.

Figures and research text were synchronized with the authors' manuscript at revision `65990be`. The original figure names map as follows:

| Manuscript asset | Website asset |
| --- | --- |
| `survival.pdf` | `survival.png` |
| `anchors_allocation_intro_figure.pdf` | `anchors-allocation.png` |
| `fig_factorial_matrix.pdf` | `factorial.png` |
| `sho_results.pdf` | `sho-results.png` |

The website template is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Bulma is MIT-licensed (notice in its CSS). Original, unmodified Lato and IBM Plex Mono fonts are bundled under the SIL Open Font License, with notices in `static/fonts/OFL.txt` and `static/fonts/ibm-plex-mono/OFL.txt`. Lato is used for the page and figures, with IBM Plex Mono for the citation block. The website's license does not set a license for unreleased research code or datasets.
