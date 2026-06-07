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
   `::: {.keybox}` · `::: {.takeaway}` (end-of-slide main message, `.alt` = purple) ·
   `::: {.card}` · `::: {.browser}` ·
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
8. **Every slide gets a `<!-- slide N -->` marker comment** on its own line
   directly above the `##` (or `#`) heading. Numbering is flat and sequential:
   `1`, `2`, `3`, … starting from the YAML title slide as `1`.
   - When a single topic is split into multiple slides (e.g. theory + result,
     or code + plot), use dotted sub-numbers: `5.1`, `5.2`, `5.3` … Sub-numbers
     keep the parent intact, so renumbering only happens when a NEW topic is
     inserted, not when an existing topic gets another slide.
   - When you split a slide that already exists, re-mark both halves immediately
     and never re-use a marker.
   - Markers are the canonical way the user (and Claude) refer to a slide:
     "fix slide 14.2" is unambiguous; "fix the heatmap slide" is not.
   - The marker is a plain HTML comment — it does not render in the deck.

## Primary task: restyle the user's EXISTING slides
The user already has Day-1 slides written with real content. Your job is to apply
this theme to their `.qmd` — a **restyle, not a rewrite**:
- Wire `style.scss` + the `setup` chunk into their YAML (theme, 1280×720, palette).
- Map each existing slide to the closest pattern (Title / Agenda / Divider /
  Two-column / Code+Plot tabset / Step-build / Takeaway / Full-bleed / Browser /
  Closing) and wrap its content in the matching classes above.
- Recolor hard-coded figure colors to `GREEN PURPLE RED BLUE GREY`.
- **Preserve their text, code, data, and topic order.** Don't invent slides or
  rephrase lecture copy unless asked.
- `slides.qmd` is a pattern reference to copy from — not content to merge in.

## Don't
- Don't edit the HTML reference render to change the theme — change `style.scss`.
- Don't add gradients, emoji, drop-shadows beyond what's in `style.scss`, or
  rounded-corner+left-border "callout" clichés other than the defined `.keybox`.
