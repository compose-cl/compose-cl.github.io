# ComposeCL project website

Academic project page for **Continual Learning Mechanisms Compose for Long-Horizon Memorization**, by Zheyuan Zhang, Alvin Zhang, Daniel Khashabi, and Tianmin Shu, Johns Hopkins University.

Website: <https://compose-cl.github.io/>

## Local preview

No build step or runtime CDN dependencies are required.

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000>. JavaScript enhances the page with a 16-combination results explorer, an interactive Task-Level Successive Halving animation, and a BibTeX copy button. All research content and figures remain readable without JavaScript.

## Content and release links

- `index.html`: title, authors, abstract, captions, project citation, metadata, and release buttons.
- `static/css/project.css`: project-specific styles and responsive layouts.
- `static/js/project.js`: accessible results explorer and citation-copy behavior.
- `static/js/results-data.js`: final retention means and standard deviations for the 16 factorial combinations. Values are transcribed at the manuscript's one-decimal precision from the complete results tables for Symbol-QA, LLM-QA, and Real-QA.
- `static/js/tsh.js` and `static/css/tsh.css`: interactive pruning, dataset selection, task slider, and playback controls. Playback begins when visible, pauses offscreen, and stops at task 100. Reduced-motion preferences disable autoplay. Each candidate keeps its position, with elimination only at the recorded task boundaries.
- `static/js/tsh-data.js`: the 90 candidates and recorded survivor IDs for each dataset at tasks 10, 20, 50, and 100. `scripts/export_tsh_data.py --source-root /path/to/results/sho` regenerates this file from the three experiment traces. Add `--check` to validate the export without changing it. Training flags and local paths are not published.
- `static/images/`: web-rendered figures, favicon, and social preview.
- `scripts/render_figures.py`: reproducible PNG export from an external directory of manuscript figures. Requires PyMuPDF. Run `python3 scripts/render_figures.py --source-dir /path/to/manuscript/figures`. Source PDFs stay outside this repository and are never copied into it.
- `scripts/check_site.py` and `scripts/check_tsh.py`: Playwright browser checks for all 16 combinations, the actual surviving candidates at and between every pruning boundary on all three datasets, autoplay/pause/replay, scrubbing, reduced motion, keyboard controls, citation copying, local links, and five viewport widths. Pass `--render-social` to regenerate the social preview too.
- `scripts/social-preview.html`: source layout for the 1200 × 630 social preview, with the retention improvement above the two-design-dimensions diagram. Rendered with a browser screenshot. The versioned image URLs in the sharing metadata should be updated when the card changes.

The [paper](https://www.alphaxiv.org/pdf/2609.compose-cl) and [official code and datasets](https://github.com/cozheyuanzhangde/compose-cl) are available through the resource buttons at the top of the page.

The main result uses the same fixed composition on all datasets: SI + SD + generative replay + merged LoRA. Its final retention is 18.5%, 41.8%, and 44.3%, respectively, and it ranks among the top 3 of the 16 factorial methods on every dataset. Dataset-specific winners are separate comparisons.

The interactive factorial comparison is the first section below the title block. Only PNG figure assets are published. PDFs are excluded from the website and ignored by Git. The BibTeX entry uses `@article` without a URL field.

The TSH animation uses `full_0.5_0.5_0.5_top10/trace.json` from each dataset's recorded experiments. Decisions rank mean retention over seeds 41, 42, and 43. The pool shrinks from 90 to 45, 23, and 10 candidates after tasks 10, 20, and 50. Those same 10 complete task 100 without an additional cut. Eight anchor groups crossed with shared or merged LoRA form the 16 displayed categories. Dots represent individual method variants, not seed runs. Playback spends 5.5 seconds on each task interval for readability, not as a representation of training time. The original aggregated percentile-rank figure remains the no-JavaScript fallback.

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

The website template is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Bulma is MIT-licensed (notice in its CSS). Original, unmodified Lato and IBM Plex Mono fonts are bundled under the SIL Open Font License, with notices in `static/fonts/OFL.txt` and `static/fonts/ibm-plex-mono/OFL.txt`. Lato is used for the page and figures, with IBM Plex Mono for the citation block. The website's license does not set a license for the research code or datasets.
