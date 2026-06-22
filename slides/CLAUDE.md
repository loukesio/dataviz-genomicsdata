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
1. **No off-system colours.** The palette is the **Economist colour system** —
   the five categorical "story" colours plus the named base ramps. Nothing from
   outside this system; no ad-hoc hexes outside the Day-1 `setup` chunk.
   - **Primary five** (SCSS vars / `setup` constants):
     `--gv-green`/`GREEN` `#379A8B` (green-teal — carries the story) ·
     `--gv-blue`/`BLUE` `#006BA2` · `--gv-amber`/`AMBER` `#EBB434` ·
     `--gv-red`/`RED` `#B4405F` · `--gv-purple`/`PURPLE` `#9A607F`.
     Green-teal carries the story; red/purple highlight one thing at a time.
   - **Neutrals:** `--gv-ink`/`INK` · `--gv-cream`/`CREAM` · `--gv-muted`/`MUTED`
     · `GREY` `#B3B3B3`; plus the DNA bases `--base-a/c/g/t`.
   - **Economist base ramps** for many-category & continuous needs — the `ECON`
     dict in `setup`: Chicago (blue), Hong Kong (teal), New York (amber),
     Shanghai (green), Singapore (orange), Tokyo (magenta), Econ Red, London
     (greyscale), Canvas. Source: the marber.economist.com colour system.
   - **Helpers in `setup`:** `COURSE_PAL` (the five) · `ECON_QUAL` (~6
     maximally-distinct hues, one strong tint per ramp, for qualitative
     categories) · `econ_cmap("ramp")` (continuous sequential from one ramp —
     use for stacked areas/heatmaps, **never** a rainbow) · `econ_diverging`
     (blue–cream–red for signed values, e.g. log2 fold-change).
2. **No new fonts.** Slide UI: JetBrains Mono (labels/code) · Space Grotesk
   (titles) · Asap (body), imported in `style.scss`. Matplotlib figures:
   **IBM Plex Mono**, registered in the Day-1 `setup` chunk via
   `matplotlib.font_manager` and set as `rcParams["font.family"]`, so it is the
   font for **all** matplotlib figures (not just pipeline/flow diagrams).
   - The `.ttf` files live in **`fonts/IBM_Plex_Mono/`** at the repo root
     (sibling of `slides/`). The `setup` chunk resolves them with path fallbacks
     (`../fonts/IBM_Plex_Mono`, then `fonts/IBM_Plex_Mono`, …) and falls back to
     `DejaVu Sans Mono` if the folder ever moves — a render never hard-fails on a
     missing font.
   - Never set the slide UI fonts (Asap / Space Grotesk / JetBrains) inside a
     matplotlib figure, and never set IBM Plex Mono in the SCSS.
3. **Use the existing classes, don't reinvent them:**
   `[label]{.eyebrow}` · `[up]{.up}` `[down]{.down}` `[alt]{.alt}` ·
   `::: {.keybox}` · `::: {.takeaway}` (end-of-slide main message, `.alt` = purple) ·
   `::: {.card}` · `::: {.browser}` ·
   `# Title {.divider}` · `::: {.columns .agenda}` · `[A]{.b-a}` etc.
4. **Eyebrow-above-title pattern:** blank-ish `##` slide title, then the
   `[…]{.eyebrow}` span, then a `###` as the visible heading. (See existing
   slides.)
5. **Code+plot / step-build = two-column, code always visible.** Left column
   (~44–46%): the **full, commented build code**, shown in full (never a teaser
   stub), growing **one step per slide** (canvas → data → style → message). Right
   column (~54–56%): the rendered plot. **Every line of code carries a short
   comment** so a student can learn from it. Do NOT hide code behind a
   `panel-tabset` "Code" tab — the code stays on screen next to its result.
   (This supersedes the earlier panel-tabset rule.)
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
   - **Inserting a new slide:** use a decimal between the neighbours, never
     renumber. New slide between 7 and 8 → `7.5`. Between 7 and 7.5 → `7.3`.
     Between 7.5 and 8 → `7.7`. Existing markers stay fixed so git diffs stay
     small and "fix slide 33" never silently points at a different slide.
   - **Only renumber on explicit request** ("clean up the markers"). Renumbering
     is its own commit, separate from content edits.

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
