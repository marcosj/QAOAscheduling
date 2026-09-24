# QI26-20 preprint source

The manuscript lives here; do not move the repository root. The arXiv ZIP is generated separately with `main.tex` and `main.bbl` at its top level.

From the repository root:

```bash
python3 tools/build_arxiv.py
```

On Windows: `py -3 tools/build_arxiv.py`.

This requires Python >= 3.9, pdfLaTeX and BibTeX. It regenerates `main.bbl`, updates `paper/QI26_20_preprint.pdf`, builds a minimal archive with used figures and ancillary data, and tests the extracted ZIP in an independent directory. Logs, SHA-256 values and the ZIP are written to `build/arxiv/`.

For a local typesetting-only build from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Edit `references.bib`, not `main.bbl`, when changing citations. The `.bbl` is tracked intentionally. The repository PDF and arXiv package must be rebuilt after source changes.

The corresponding author reports that the preprint dissemination approvals have been received by email. The final author-approval sentence and funding statement are active in `main.tex`. Keep the approval emails private. Read [the preparation guide](../../docs/ARXIV_PREPARATION_ES.md) for record-keeping and submission steps.

The `Data/` directory preserves the complete decoded hardware distributions and metric audit. The arXiv builder copies these unchanged into `anc/Data/`. No scientific results are recomputed by the build script.

## Licenses

The original manuscript content is licensed under **CC BY 4.0**; original accompanying software is licensed under **Apache 2.0**. See [LICENSING.md](../../LICENSING.md), [LICENSE-CONTENT](../../LICENSE-CONTENT), [LICENSE](../../LICENSE), and [NOTICE](../../NOTICE). Third-party materials retain their respective terms.

The builder includes both license texts, scope, and attribution in `anc/` so the arXiv source archive is self-contained. Select **CC BY 4.0** in the arXiv submission form.
