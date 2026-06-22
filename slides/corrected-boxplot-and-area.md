# Corrected pattern — boxplot step-by-step + stacked-area ramp

> Preview/verify file. Drop these slides into a scratch `.qmd` (with the Day-1
> `setup` chunk loaded) and `quarto preview` to check they FIT and look right.
> If good, I apply the same two patterns to violin / stacked-bar / small-multiples
> / ridgeline and the concept slides.
>
> Layout rule used here: **two columns, text left + plot right, plot sized to fit.**
> Step rule: **one sub-slide per build step**, left = theory + the step's code,
> right = the outcome of that step.
>
> One setup-chunk addition needed (add next to `econ_cmap`):
> ```python
> econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
>     [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1],
>      ECON["newyork"][0], ECON["red"][1]])   # blue→teal→green→amber→red
> ```

---

<!-- slide 23 -->
## When & Why a Boxplot {.smaller}

[Distributions · when to use]{.eyebrow}

### A boxplot summarises spread, pick the chart that fits your question

:::: {.columns}
::: {.column width="44%"}
Use a boxplot to compare the **distribution** of a continuous value across a few groups, its centre, spread, and outliers, without plotting every point.

**Spread is not precision.** Standard deviation describes how the data scatter around the mean. Standard error describes how precise your estimate of the mean is. A boxplot answers the first question, error bars on a mean answer the second.
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 5
r = np.random.default_rng(1)
groups = ["WT", "Mut A", "Mut B"]
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 5))
bp = ax.boxplot(data, widths=0.55, patch_artist=True, labels=groups)
for p in bp["boxes"]: p.set_facecolor(ECON["hongkong"][3]); p.set_edgecolor(GREEN)
for m in bp["medians"]: m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
for fl in bp["fliers"]: fl.set(marker="o", markerfacecolor=CREAM, markeredgecolor=RED, markersize=5)
ax.set_ylabel("Expression (TPM)")
ax.set_title("DISTRIBUTION ACROSS THREE GENOTYPES", fontsize=11, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::

::: {.takeaway}
SD vs SE: the spread of the data vs the precision of the estimate. Same numbers, different questions, different charts.
:::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Wilke (2019), Ch. 9.
:::


<!-- slide 24 -->
## Building a Boxplot · Step 1: the canvas {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Set up the figure, labels, and scale before any data

:::: {.columns}
::: {.column width="46%"}
Start with an empty, labelled canvas: the axes, the group positions, the y-scale. Decide the frame first, then fill it.

```python
groups = ["WT", "Mut A", "Mut B"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)")
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5)
ax.set_ylim(30, 85)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)")
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
ax.set_title("STEP 1: THE CANVAS", fontsize=12, fontweight="bold", color=MUTED, pad=10)
plt.show()
```
:::
::::


<!-- slide 25 -->
## Building a Boxplot · Step 2: the raw points {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Always look at the data first, with a little horizontal jitter

:::: {.columns}
::: {.column width="46%"}
Plot every observation, jittering the x-position so points don't stack on one line. This shows the sample size and shape that a summary will later hide.

```python
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70),
        r.normal(62, 10, 70),
        r.normal(58, 4, 70)]

rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    x = rj.normal(i, 0.06, len(d))
    ax.scatter(x, d, color=GREEN,
               s=18, alpha=0.5, edgecolors="none")
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.5, edgecolors="none")
ax.set_title("STEP 2: RAW POINTS", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide 26 -->
## Building a Boxplot · Step 3: add the box {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Overlay the five-number summary on top of the points

:::: {.columns}
::: {.column width="46%"}
The box draws Q1 to Q3, the median line, and whiskers to the most extreme points within 1.5× IQR. Matplotlib computes all of it for you.

```python
bp = ax.boxplot(
    data,
    positions=[1, 2, 3],
    widths=0.5,
    patch_artist=True,   # so we can colour it
)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.35, edgecolors="none")
ax.boxplot(data, positions=[1, 2, 3], widths=0.5, patch_artist=True)
ax.set_title("STEP 3: ADD THE BOX (DEFAULT)", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 27 -->
## Building a Boxplot · Step 4: style on-palette {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Economist green box, ink median, fade the points behind

:::: {.columns}
::: {.column width="46%"}
Style every element by hand: a soft teal fill, a green edge, a bold ink median, green whiskers. Drop the alpha on the points so the box reads on top.

```python
bp = ax.boxplot(data, positions=[1,2,3],
                widths=0.5, patch_artist=True)
for p in bp["boxes"]:
    p.set_facecolor(ECON["hongkong"][3])
    p.set_edgecolor(GREEN); p.set_alpha(0.75)
for m in bp["medians"]:
    m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]:
    w.set_color(GREEN)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.3, edgecolors="none")
bp = ax.boxplot(data, positions=[1, 2, 3], widths=0.5, patch_artist=True)
for p in bp["boxes"]: p.set_facecolor(ECON["hongkong"][3]); p.set_edgecolor(GREEN); p.set_alpha(0.75)
for m in bp["medians"]: m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
ax.set_title("STEP 4: STYLED ON-PALETTE", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 28 -->
## Building a Boxplot · Step 5: the message {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Hide duplicate outliers, add a title that states the finding

:::: {.columns}
::: {.column width="46%"}
The points already show every value, so turn off the default flier markers. Finish with a title that says what the reader should take away.

```python
bp = ax.boxplot(data, showfliers=False, ...)
ax.set_title(
    "MUT A SHOWS THE WIDEST SPREAD")
```

That is the whole recipe: **canvas → points → box → style → message.**
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.3, edgecolors="none")
bp = ax.boxplot(data, positions=[1, 2, 3], widths=0.5, patch_artist=True, showfliers=False)
for p in bp["boxes"]: p.set_facecolor(ECON["hongkong"][3]); p.set_edgecolor(GREEN); p.set_alpha(0.75)
for m in bp["medians"]: m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
ax.set_title("MUT A SHOWS THE WIDEST SPREAD", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Same recipe drives the violin: swap the box for a KDE body.
:::


<!-- slide 32 -->
## Stacked Area Over Time: Lineage Tracking {.smaller}

[Proportions · barcode lineages]{.eyebrow}

### Hundreds of lineages summing to one, every band on a continuous ramp

:::: {.columns}
::: {.column width="42%"}
Each column is one timepoint and sums to 1, so the whole height is the population. With hundreds of lineages, order them by abundance and colour them along **one continuous Economist ramp**, from blue through teal, green, and amber to red.

Position in the ramp encodes rank, so the eye can follow a band over time without a rainbow of unrelated hues.
:::
::: {.column width="58%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 7
#| fig-height: 5
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1],
     ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]          # largest first
colors = [econ_spectrum(i / (n_lin - 1)) for i in range(n_lin)]
fig, ax = plt.subplots(figsize=(7, 5))
ax.stackplot(days, freq, colors=colors, edgecolor="none")
ax.set_xlim(0, n_t - 1); ax.set_ylim(0, 1)
ax.set_xlabel("Time (days)"); ax.set_ylabel("Barcode frequency")
ax.set_title("BARCODE LINEAGE FREQUENCIES, REPLICATE 2",
             fontsize=11, fontweight="bold", color=INK, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::

::: {.takeaway}
Many components, one continuous ramp ordered by abundance, so every band is coloured and the eye can still track a lineage over time.
:::
