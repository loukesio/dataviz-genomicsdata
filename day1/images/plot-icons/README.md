# Plot icons — Genomics Viz with Python

78 mini plot thumbnails in the course visual system. Each comes as a **scalable
`.svg`** (best for web + Quarto HTML) and a **transparent `.png`** at 528×312
(best for Quarto PDF/Beamer, PowerPoint, Word).

```
plot-icons/
├── 01-amounts/        bars, dots, grouped/stacked bars, heatmap
├── 02-distributions/  histogram, density, boxplot, violin, strip, sina, ridgeline, Q–Q
├── 03-proportions/    pie, donut, stacked/grouped bars, mosaic, treemap, parallel sets
├── 04-relationships/  scatter, bubble, line, smooth, contours, hex, correlogram, slopegraph
├── 05-uncertainty/    error bars, 2D/graded error, confidence strip, eyes, quantile dots
└── 06-genomics/       volcano, heatmap, waterfall, waffle, pathway, ideogram, gene model,
                       peak, coverage, manhattan, MSA, seq-logo, UMAP, phylogeny,
                       circos, synteny, venn, upset
└── 07-ml/             confusion matrix, ROC, PR, calibration, threshold, ROC-comparison,
                       residuals, loss, learning curve, CV folds, grid search, elbow,
                       silhouette, feature importance, SHAP, LIME, PDP, ICE, attention,
                       saliency, decision tree, decision boundary, embedding/t-SNE
```

Backgrounds are **transparent**, so the icons sit on any slide or page colour.
viewBox is `0 0 132 78` (≈1.69:1); scale freely.

## Use in Quarto

Inline in Markdown (sizes in px or %):
```markdown
![](plot-icons/06-genomics/01-volcano.svg){width=140}
```

Next to a heading / as a section motif:
```markdown
## Volcano plots ![](plot-icons/06-genomics/01-volcano.svg){height=1em}
```

For **PDF / Beamer** output use the PNG (LaTeX won't embed SVG without `rsvg`):
```markdown
![](plot-icons/06-genomics/01-volcano.png){width=140}
```

## Use on a website

```html
<img src="plot-icons/06-genomics/01-volcano.svg" alt="Volcano plot" width="140">
```
SVGs are tiny and crisp at any size — prefer them for the web. You can also paste
the SVG markup inline and recolour it with CSS if you want themed variants.

## Recolouring

Every icon uses the course palette: green `#208462` / `#2ea579`, purple `#7754bf`,
red `#c0473a`, blue `#2b6fb0`, amber `#c98a1a`, on warm neutrals. Open any `.svg`
in a text editor and swap the hex values to retheme.

*Regenerated from `Plot Directory.html` — edit the gallery and re-export to refresh.*
