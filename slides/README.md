# Handoff: Genomics Viz with Python — Quarto reveal.js deck

A working package for continuing this slide deck in **Claude Code** (or by hand).
Everything Claude Code needs is in this folder.

> **Your situation:** you already have Day-1 slides written with real content. The
> job for Claude Code is to **restyle your existing `.qmd` to this theme** — keep
> your text, code, and figures; apply the look, the components, and the layout
> patterns. It is a refactor, **not** a rewrite. See §0.

```
design_handoff_genomics_deck/
├── README.md      ← you are here (start Claude Code with this open)
├── CLAUDE.md      ← auto-loaded guardrails — DO NOT delete, move with the project
├── style.scss     ← the reveal.js theme (single source of truth for visuals)
├── slides.qmd     ← pattern reference — every layout demonstrated
└── reference/
    ├── reference-render.html   ← static HTML render of the TARGET look (visual spec)
    ├── deck-stage.js           ← support file for the reference render only
    └── slides/                 ← per-slide PNG screenshots (01–11, see §6)
```

---

## 0. The task: restyle the existing Day-1 slides

You (the developer / Claude Code) are given the user's **existing Day-1 `.qmd`**
that already contains the real lecture content. Apply this design system to it.

**Do**
- Point the deck at the theme: in the YAML front matter set
  `format: revealjs: theme: [default, style.scss]`, `width: 1280`, `height: 720`.
- Copy the `setup` chunk and `execute`/`format` options from `slides.qmd` so
  figures inherit the cream `rcParams` and the `GREEN PURPLE RED BLUE GREY` palette.
- Map each existing slide onto the **closest layout pattern** (table in §6) and wrap
  its content in the matching classes/components from §5 — e.g. turn a code+figure
  slide into a `::: {.panel-tabset}` Code/Plot, add an `[eyebrow]{.eyebrow}` above
  titles, end key slides with a `::: {.takeaway}`.
- Recolor any hard-coded figure colors to the palette constants.
- Keep the user's wording, data, and code logic intact.

**Don't**
- Don't rewrite or “improve” the lecture copy, reorder topics, or invent new slides
  unless asked.
- Don't introduce colors, fonts, or components outside `style.scss`.
- Don't touch the cream default to make something dark (ask first).

**Suggested first prompt to Claude Code**
> *"Read CLAUDE.md, README, and skim reference/reference-render.html. My Day-1
> deck is `day1.qmd`. Restyle it to this theme: wire `style.scss` + the setup
> chunk into the YAML, then go slide by slide mapping each to the closest layout
> in §6 and wrapping content in the right classes. Preserve all my text, code, and
> data — this is a restyle, not a rewrite. Show me a `quarto preview` when done."*

**Slide-by-slide migration checklist (per existing slide)**
1. Add the eyebrow + `###` title (eyebrow-above-title pattern).
2. Pick the layout from §6; wrap in `.columns` / `.panel-tabset` / `.card` etc.
3. Replace ad-hoc emphasis with `[.up]/[.down]/[.alt]` or `==highlight==`.
4. Point figure colors at `GREEN/PURPLE/RED/BLUE/GREY`; drop top/right spines.
5. If the slide has a single message, end it with `::: {.takeaway}`.
6. Preview; check nothing overflows at 1280×720.

---

## 1. How to communicate with Claude Code (the important part)

Claude Code has **no "skills file."** Its persistent-instruction channel is a file
literally named **`CLAUDE.md`**, which it loads automatically from the directory it
is launched in (plus parent dirs, plus any `CLAUDE.md` in a subfolder it starts
editing). `CLAUDE.md` is already written for this project — keep it next to the
`.scss`/`.qmd`.

**Workflow**
1. Put `style.scss`, `slides.qmd` (as a pattern reference), and `CLAUDE.md` next to
   your existing Day-1 `.qmd` in your course repo.
2. Launch Claude Code from that folder. It ingests `CLAUDE.md` on its own — you do
   **not** need to paste the rules each session.
3. Then ask in plain language. Because your content already exists, the prompts are
   about **restyling**, e.g.:
   - *"Restyle `day1.qmd` to this theme — wire in style.scss + the setup chunk, then
     map each slide to a layout in README §6. Keep my text and code. Preview when done."*
   - *"Slide 4 of mine is a code block + a figure. Convert it to a Code/Plot
     `.panel-tabset` like the volcano slide and end it with a `.takeaway`."*
   - *"Recolor every figure in `day1.qmd` to the palette constants from the setup chunk."*
   - *"Add eyebrow labels above each slide title using the `[…]{.eyebrow}` pattern."*

**Two rules to tell Claude Code up front** (they're also in `CLAUDE.md`):
- The visual spec is `reference/reference-render.html` — **match it, don't port it.**
  The `.html` is a static mock; the deliverable is the Quarto `.qmd` + `.scss`.
- All visual changes go in `style.scss`. Never hard-code colors/fonts in a slide.

---

## 2. What these files are

- **`style.scss` and `slides.qmd` are production files**, not throwaway mocks — they
  render the real deck with `quarto render slides.qmd`. Extend them.
- **`reference/reference-render.html` is a design reference only** — a high-fidelity
  static render showing the intended look, interactions (Code↔Plot tabs), and the
  data-viz placeholders. Use it as the pixel/comp target.

**Fidelity: high.** Final colors, type, spacing, and component styles are decided.
Recreate/extend faithfully; don't redesign.

---

## 3. Build & preview

```bash
quarto preview slides.qmd     # live reload
quarto render  slides.qmd     # -> slides.html
```
Requires **Quarto ≥ 1.4** and a Python env with **`numpy matplotlib seaborn`**
(the template renders real figures from synthetic data in its chunks).

Fonts (**JetBrains Mono · Space Grotesk · Asap**) load from Google Fonts at the top
of `style.scss` — no install needed online. Download the `.ttf`s only for offline
presenting or to render matplotlib text in those fonts (plots use DejaVu Sans now).

---

## 4. Design tokens (defined in `style.scss`, exposed as CSS vars)

| Token         | Hex       | Role                                          |
|---------------|-----------|-----------------------------------------------|
| `--gv-cream`  | `#f6f4ee` | slide background                              |
| `--gv-surface`| `#fdfcf8` | cards / figure wraps                          |
| `--gv-ink`    | `#211f1a` | body text                                     |
| `--gv-muted`  | `#807b6d` | secondary text                                |
| `--gv-faint`  | `#a8a395` | micro-labels, axis ticks                      |
| `--gv-line`   | `#e2ddcf` | hairlines, borders                            |
| `--gv-green`  | `#208462` | **primary** — links, eyebrows, "down"         |
| `--gv-purple` | `#7754bf` | secondary highlight / "alt"                   |
| `--gv-red`    | `#c0473a` | emphasis / "up-regulated"                     |
| `--gv-blue`   | `#2b6fb0` | kwargs / tertiary                             |
| `--gv-amber`  | `#c98a1a` | quaternary                                    |
| `--base-a/c/g/t` | —      | DNA-base chip colors                          |

Type: JetBrains Mono (labels/code) · Space Grotesk 600 (titles) · Asap (body).
Slide size **1280×720**. Harmony rule: **green carries the story; red/purple
highlight one thing at a time.**

---

## 5. Components / classes (all styled in `style.scss`)

| Pattern                | Markup                                            |
|------------------------|---------------------------------------------------|
| Eyebrow label          | `[Differential expression]{.eyebrow}`             |
| Inline highlights      | `[up]{.up}` `[down]{.down}` `[alt]{.alt}` · `==hi==` |
| DNA base chips         | `[A]{.b-a} [T]{.b-t} [G]{.b-g} [C]{.b-c}`         |
| Key-point callout      | `::: {.keybox}` + `[label]{.keylabel}`            |
| **Main message / bottom line** | `::: {.takeaway}` + `[The bottom line]{.tl}` (add `.alt` for purple) |
| Card / figure wrap     | `::: {.card}`                                     |
| Section divider (dark) | `# Day 01 — Foundations & *DE* {.divider}`        |
| Agenda (numbered, ruled)| `::: {.columns .agenda}` + `.column` blocks      |
| Code ↔ Plot / step build| `::: {.panel-tabset}` + `###` tab headings       |
| App / browser frame    | `::: {.browser}` + `::: {.bbar}`                  |

**Eyebrow-above-title pattern:** blank-ish `##` slide title → `[…]{.eyebrow}` →
`###` as the visible heading. (See any content slide in `slides.qmd`.)

---

## 6. Slide layouts in the template (`slides.qmd`)

| # | Layout              | Topic shown            | Reference shot                    |
|---|---------------------|------------------------|-----------------------------------|
| 1 | Title / cover       | course front matter    | `reference/slides/01-slide.png`   |
| 2 | Agenda / bullets    | 3-day schedule         | `02-slide.png`                    |
| 3 | Section divider     | Day 01                 | `03-slide.png`                    |
| 4 | Two-column concept  | the Python viz stack   | `04-slide.png` (+ `.takeaway`)    |
| 5 | Code ↔ Plot tabs    | volcano — Code tab      | `05-slide.png`                    |
| 5 | Code ↔ Plot tabs    | volcano — Plot tab      | `06-slide.png`                    |
| 6 | Step-by-step build  | heatmap — final tab     | `07-slide.png`                    |
| 7 | Big takeaway / quote| design principle       | `08-slide.png`                    |
| 8 | Full-bleed figure   | Manhattan plot         | `09-slide.png`                    |
| 9 | Live-demo frame     | UMAP explorer          | `10-slide.png`                    |
|10 | Closing             | thank-you + resources  | `11-slide.png`                    |

Screenshots are 2× PNG renders of `reference-render.html` at 1280×720 — use them as
the exact visual target for each layout.

---

## 7. After Day 1 is restyled

- Apply the same pass to **Day 2/3** content as you write it.
- `slides.qmd` stays as the canonical **pattern reference** — point Claude Code at
  any slide in it ("do it like the heatmap step-build slide").
- Add a `{.dark}` theme variant for live coding (ask first).
- Add speaker notes (`::: {.notes}`) per slide.

---

*Per-slide screenshots are in `reference/slides/` (01–11) — see the §6 table for
what each one shows.*
