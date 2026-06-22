# CLAUDE.md — Genomics Viz with Python (Quarto reveal.js deck)

> Auto-loaded by Claude Code. Read `README.md` next for the authoring cheatsheet.

## What this is
A Quarto **reveal.js** slide theme + template for a 3-day course, "Genomics Viz
with Python." The visual system is a warm "Carbon-cream" data-viz look. Treat
`style.scss` as the single source of truth for all visual decisions.

## Files
- `style.scss` — the theme. ALL colors, type, and component styles live here.
- `slides.qmd` — the deck. One `##` (or `#`) heading per slide.
- `README.md` — authoring cheatsheet + token table (read this).
- `Genomics Viz with Python.html` (in the parent folder) — a static HTML
  **reference render** of the target look. It is NOT the source; it's the visual
  spec. Match it; don't port it.

## Build / preview
```bash
quarto preview slides.qmd     # live reload
quarto render  slides.qmd     # -> slides.html
```
Needs Quarto ≥ 1.4 and a Python env with `numpy matplotlib seaborn`
(figures render from synthetic data in the chunks).

## Hard rules — do not violate
1. **No new colors.** Use only the SCSS tokens / CSS vars: `--gv-green`
   (#208462, primary), `--gv-purple` (#7754bf), `--gv-red` (#c0473a),
   `--gv-blue`, `--gv-amber`, `--gv-ink`, `--gv-cream`, and `--base-a/c/g/t`.
   Green carries the story; red/purple highlight one thing at a time.
2. **No new fonts.** JetBrains Mono (labels/code) · Space Grotesk (titles) ·
   Asap (body). They're imported at the top of `style.scss`.
3. **Use the existing classes, don't reinvent them:**
   `[label]{.eyebrow}` · `[up]{.up}` `[down]{.down}` `[alt]{.alt}` ·
   `::: {.keybox}` · `::: {.card}` · `::: {.browser}` ·
   `# Title {.divider}` · `::: {.columns .agenda}` · `[A]{.b-a}` etc.
4. **Eyebrow-above-title pattern:** blank-ish `##` slide title, then the
   `[…]{.eyebrow}` span, then a `###` as the visible heading. (See existing
   slides.)
5. **Code+plot / step-build = `::: {.panel-tabset}`** with `###` sub-headings as
   tab labels. Already styled — don't hand-roll tabs.
6. **Figures stay on-system:** reuse the palette constants from the `setup`
   chunk (`GREEN PURPLE RED BLUE GREY`) and the matplotlib `rcParams` already
   set there. Prefer perceptually-uniform colormaps (`mako`, `viridis`, scico).
7. **Slide size is 1280×720** (set in the YAML). Keep it.

## When adding lecture content
Each new plot type = one slide following an existing pattern. The course topics
(by day) are listed in the agenda slide of `slides.qmd`. Add real data loading
where you have it; otherwise keep the synthetic-data chunks so the deck renders.

## Don't
- Don't edit the HTML reference render to change the theme — change `style.scss`.
- Don't add gradients, emoji, drop-shadows beyond what's in `style.scss`, or
  rounded-corner+left-border "callout" clichés other than the defined `.keybox`.
