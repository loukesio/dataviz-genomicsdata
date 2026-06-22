# Rollout — violin build + stacked-bar build + stacked-area build

> Same pattern as the approved boxplot: two columns (theory + step code left,
> outcome right), one sub-slide per build step, plots sized to fit.
> Needs `econ_spectrum` in the setup chunk (see note in the boxplot file).
> Slide numbers are placeholders; the final renumber fixes them.

<!-- ════════════════════════════ VIOLIN ════════════════════════════ -->

<!-- slide V0 -->
## When & Why a Violin {.smaller}

[Distributions · when to use]{.eyebrow}

### Reach for a violin when the shape matters, not just the summary

:::: {.columns}
::: {.column width="44%"}
A boxplot hides shape: two very different distributions can share the same five-number summary. A violin draws a **mirrored density**, so a second hump or a long skew is visible at a glance.

Use it when the distribution might be **bimodal** or strongly skewed. Use a plain boxplot when a clean five-number summary is all you need.
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 5
r = np.random.default_rng(3)
bimodal = np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)])
fig, ax = plt.subplots(figsize=(6.4, 5))
vp = ax.violinplot([bimodal], positions=[1], widths=0.7, showextrema=False)
for b in vp["bodies"]: b.set_facecolor(ECON["hongkong"][3]); b.set_edgecolor(GREEN); b.set_alpha(0.85)
bx = ax.boxplot([bimodal], positions=[1], widths=0.12, patch_artist=True, showfliers=False)
for p in bx["boxes"]: p.set_facecolor(INK)
for m in bx["medians"]: m.set_color(CREAM)
ax.set_xticks([1]); ax.set_xticklabels(["one sample"]); ax.set_ylabel("Expression (TPM)")
ax.set_title("THE BOX MISSES THE TWO PEAKS", fontsize=11, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Wilke (2019), Ch. 7.
:::


<!-- slide V1 -->
## Building a Violin · Step 1: the canvas {.smaller}

[Distributions · violin build]{.eyebrow}

### Same canvas as the boxplot, three groups on the x-axis

:::: {.columns}
::: {.column width="46%"}
The recipe starts identically: an empty, labelled frame. One of the groups is deliberately **bimodal** so the violin has something a box would hide.

```python
r = np.random.default_rng(3)
groups = ["WT", "Mut A", "Mut B"]
data = [np.concatenate([r.normal(45,5,45),
                        r.normal(62,5,35)]),
        r.normal(62, 10, 80),
        r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1,2,3]); ax.set_xticklabels(groups)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
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
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
ax.set_title("STEP 1: THE CANVAS", fontsize=12, fontweight="bold", color=MUTED, pad=10)
plt.show()
```
:::
::::


<!-- slide V2 -->
## Building a Violin · Step 2: the raw points {.smaller}

[Distributions · violin build]{.eyebrow}

### Look at the points first, the left group has two clusters

:::: {.columns}
::: {.column width="46%"}
Jittered points already hint at the structure: the WT group sits in two clouds, not one. The violin will make that explicit.

```python
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d,
               color=GREEN, s=16, alpha=0.5,
               edgecolors="none")
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]),
        r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=16, alpha=0.5, edgecolors="none")
ax.set_title("STEP 2: RAW POINTS", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide V3 -->
## Building a Violin · Step 3: add the density {.smaller}

[Distributions · violin build]{.eyebrow}

### violinplot draws a kernel density and mirrors it about each axis

:::: {.columns}
::: {.column width="46%"}
The body width at any height is the point density there. The WT violin now shows two bulges, the bimodality a box would flatten away.

```python
vp = ax.violinplot(
    data,
    positions=[1, 2, 3],
    showextrema=False,
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
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]),
        r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=14, alpha=0.3, edgecolors="none")
ax.violinplot(data, positions=[1, 2, 3], showextrema=False)
ax.set_title("STEP 3: ADD THE DENSITY (DEFAULT)", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide V4 -->
## Building a Violin · Step 4: style on-palette {.smaller}

[Distributions · violin build]{.eyebrow}

### Teal body, green edge, fade the points behind

:::: {.columns}
::: {.column width="46%"}
Loop over the violin bodies and colour them on-brand, then drop the points' alpha so the density reads on top.

```python
vp = ax.violinplot(data, positions=[1,2,3],
                   showextrema=False)
for b in vp["bodies"]:
    b.set_facecolor(ECON["hongkong"][3])
    b.set_edgecolor(GREEN)
    b.set_alpha(0.75)
    b.set_linewidth(1.4)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]),
        r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=14, alpha=0.25, edgecolors="none")
vp = ax.violinplot(data, positions=[1, 2, 3], showextrema=False)
for b in vp["bodies"]:
    b.set_facecolor(ECON["hongkong"][3]); b.set_edgecolor(GREEN); b.set_alpha(0.75); b.set_linewidth(1.4)
ax.set_title("STEP 4: STYLED ON-PALETTE", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide V5 -->
## Building a Violin · Step 5: the message {.smaller}

[Distributions · violin build]{.eyebrow}

### Add a slim inner boxplot, then a title that states the finding

:::: {.columns}
::: {.column width="46%"}
A thin boxplot inside each violin gives the five-number summary and the shape together. Finish with the takeaway in the title.

```python
for i, d in enumerate(data, start=1):
    bx = ax.boxplot(d, positions=[i],
        widths=0.1, patch_artist=True,
        showfliers=False)
    bx["boxes"][0].set_facecolor(INK)
    bx["medians"][0].set_color(CREAM)
ax.set_title("WT IS BIMODAL")
```

Same recipe as the box: **canvas → points → density → style → message.**
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]),
        r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
vp = ax.violinplot(data, positions=[1, 2, 3], showextrema=False)
for b in vp["bodies"]:
    b.set_facecolor(ECON["hongkong"][3]); b.set_edgecolor(GREEN); b.set_alpha(0.6); b.set_linewidth(1.4)
for i, d in enumerate(data, start=1):
    bx = ax.boxplot(d, positions=[i], widths=0.1, patch_artist=True, showfliers=False)
    for p in bx["boxes"]: p.set_facecolor(INK)
    for m in bx["medians"]: m.set_color(CREAM); m.set_linewidth(1.4)
    for w in bx["whiskers"] + bx["caps"]: w.set_color(INK)
ax.set_title("WT IS BIMODAL", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::

::: {.takeaway}
Box vs violin: the box gives the summary, the violin reveals the shape. Show the violin when bimodality or skew is the story.
:::


<!-- ════════════════════════ STACKED BAR ════════════════════════ -->

<!-- slide SB1 -->
## Building a Stacked Bar · Step 1: the canvas {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Set up timepoints on x, abundance on y, and a distinct colour per taxon

:::: {.columns}
::: {.column width="46%"}
We track six taxa across six timepoints. Choose **distinct Economist hues**, one per taxon, with grey reserved for the catch-all "Other".

```python
taxa = ["Firmicutes","Bacteroidetes",
        "Proteobacteria","Actinobacteria",
        "Verrucomicrobia","Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0],
        ECON["hongkong"][0], ECON["tokyo"][1],
        ECON["newyork"][0], GREY]
tps = ["D0","D3","D7","D14","D21","D28"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks(range(len(tps))); ax.set_xticklabels(tps)
ax.set_ylabel("Read count"); ax.set_xlabel("Timepoint")
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cols]
ax.legend(handles, taxa, loc="upper right", fontsize=7, frameon=False)
ax.set_title("STEP 1: CANVAS + PALETTE", fontsize=12, fontweight="bold", color=MUTED, pad=10)
plt.show()
```
:::
::::


<!-- slide SB2 -->
## Building a Stacked Bar · Step 2: stack the counts {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Stack each taxon by carrying a running bottom

:::: {.columns}
::: {.column width="46%"}
Draw each taxon as a bar, then add its height to a running `bottom` so the next taxon sits on top. Raw counts let sample totals differ.

```python
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, counts[i], bottom=bottom,
           color=c, label=t, edgecolor=CREAM)
    bottom += counts[i]
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
rr = np.random.default_rng(5)
raw = rr.dirichlet(np.array([6, 5, 2, 2, 1, 1.0]), size=len(tps))
counts = (raw.T * rr.integers(8000, 12000, len(tps)))
fig, ax = plt.subplots(figsize=(6.4, 4.7))
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, counts[i], bottom=bottom, color=c, label=t, edgecolor=CREAM, width=0.8); bottom += counts[i]
ax.set_ylabel("Read count"); ax.set_xlabel("Timepoint")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_title("STEP 2: ABSOLUTE COUNTS", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide SB3 -->
## Building a Stacked Bar · Step 3: normalise to 100% {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Divide each column by its total so composition is comparable

:::: {.columns}
::: {.column width="46%"}
Absolute counts confound depth with composition. Divide every column by its sum so each bar reaches 100%, and only the **proportions** vary.

```python
comp = counts / counts.sum(axis=0,
                           keepdims=True) * 100
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, comp[i], bottom=bottom,
           color=c, label=t, edgecolor=CREAM)
    bottom += comp[i]
ax.set_ylim(0, 100)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
rr = np.random.default_rng(5)
raw = rr.dirichlet(np.array([6, 5, 2, 2, 1, 1.0]), size=len(tps))
counts = (raw.T * rr.integers(8000, 12000, len(tps)))
comp = counts / counts.sum(axis=0, keepdims=True) * 100
fig, ax = plt.subplots(figsize=(6.4, 4.7))
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, comp[i], bottom=bottom, color=c, label=t, edgecolor=CREAM, width=0.8); bottom += comp[i]
ax.set_ylim(0, 100); ax.set_ylabel("Relative abundance (%)"); ax.set_xlabel("Timepoint")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_title("STEP 3: NORMALISED TO 100%", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide SB4 -->
## Building a Stacked Bar · Step 4: legend & message {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Move the legend outside, title the trend

:::: {.columns}
::: {.column width="46%"}
Put the legend to the right so it never covers a bar, and write the finding into the title.

```python
ax.legend(loc="upper left",
          bbox_to_anchor=(1.01, 1.0),
          frameon=False)
ax.set_title(
    "FIRMICUTES RISE AS PROTEOBACTERIA FALL")
```

Recipe: **canvas → stack counts → normalise → label.**
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.8
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
rr = np.random.default_rng(5)
raw = rr.dirichlet(np.array([6, 5, 2, 2, 1, 1.0]), size=len(tps))
counts = (raw.T * rr.integers(8000, 12000, len(tps)))
comp = counts / counts.sum(axis=0, keepdims=True) * 100
fig, ax = plt.subplots(figsize=(6.8, 4.7))
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, comp[i], bottom=bottom, color=c, label=t, edgecolor=CREAM, width=0.8); bottom += comp[i]
ax.set_ylim(0, 100); ax.set_ylabel("Relative abundance (%)"); ax.set_xlabel("Timepoint")
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_title("MICROBIOME COMPOSITION OVER TIME", fontsize=11, fontweight="bold", color=INK, pad=10)
fig.subplots_adjust(right=0.74)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Cap categories (top taxa + "Other") so the palette stays distinct.
:::


<!-- ════════════════════════ STACKED AREA ════════════════════════ -->

<!-- slide SA1 -->
## Building a Stacked Area · Step 1: a few lineages {.smaller}

[Proportions · stacked-area build]{.eyebrow}

### Start with the handful of dominant lineages as stacked bands

:::: {.columns}
::: {.column width="46%"}
A stacked area is a stacked bar with a continuous x-axis. Begin with the top few lineages so the idea is clear: each band is one lineage, frequencies sum to 1 each day.

```python
econ_spectrum  # blue→teal→green→amber→red
top = freq[:6]
cols = [econ_spectrum(i/5) for i in range(6)]
ax.stackplot(days, top, colors=cols)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1], ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]
top = freq[:6]
cols = [econ_spectrum(i / 5) for i in range(6)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.stackplot(days, top, colors=cols, edgecolor=CREAM, lw=0.4)
ax.set_xlim(0, n_t - 1); ax.set_xlabel("Time (days)"); ax.set_ylabel("Frequency")
ax.set_title("STEP 1: TOP 6 LINEAGES", fontsize=12, fontweight="bold", color=INK, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::


<!-- slide SA2 -->
## Building a Stacked Area · Step 2: all of them, full spectrum {.smaller}

[Proportions · stacked-area build]{.eyebrow}

### Colour every band by its vertical position so the whole ramp shows

:::: {.columns}
::: {.column width="46%"}
Now add all 150 lineages. The trick: colour each band by **where it sits in the stack** (its cumulative height), not its rank. That spreads the full blue→red ramp across the whole height, so every band gets its own colour.

```python
mean_ab = freq.mean(axis=1)
cum = np.cumsum(mean_ab)
centre = (cum - mean_ab/2) / cum[-1]  # 0→1 up
colors = [econ_spectrum(c) for c in centre]
ax.stackplot(days, freq, colors=colors)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1], ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]
mean_ab = freq.mean(axis=1)
cum = np.cumsum(mean_ab)
centre = (cum - mean_ab / 2) / cum[-1]
colors = [econ_spectrum(c) for c in centre]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.stackplot(days, freq, colors=colors, edgecolor="none")
ax.set_xlim(0, n_t - 1); ax.set_ylim(0, 1); ax.set_xlabel("Time (days)"); ax.set_ylabel("Frequency")
ax.set_title("STEP 2: ALL 150, FULL SPECTRUM", fontsize=12, fontweight="bold", color=GREEN, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::


<!-- slide SA3 -->
## Building a Stacked Area · Step 3: the message {.smaller}

[Proportions · stacked-area build]{.eyebrow}

### Label the axes and title the dynamic

:::: {.columns}
::: {.column width="44%"}
The finished plot reads as a smooth blue-to-red gradient where each lineage keeps its own band, and you can follow any band as it widens or fades over time.

```python
ax.set_ylim(0, 1)
ax.set_xlabel("Time (days)")
ax.set_ylabel("Barcode frequency")
ax.set_title(
    "A FEW LINEAGES SWEEP TO FIXATION")
```

Recipe: **few bands → all bands by height → label.**
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 7
#| fig-height: 4.8
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1], ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]
mean_ab = freq.mean(axis=1); cum = np.cumsum(mean_ab)
centre = (cum - mean_ab / 2) / cum[-1]
colors = [econ_spectrum(c) for c in centre]
fig, ax = plt.subplots(figsize=(7, 4.8))
ax.stackplot(days, freq, colors=colors, edgecolor="none")
ax.set_xlim(0, n_t - 1); ax.set_ylim(0, 1)
ax.set_xlabel("Time (days)"); ax.set_ylabel("Barcode frequency")
ax.set_title("BARCODE LINEAGE FREQUENCIES, REPLICATE 2", fontsize=11, fontweight="bold", color=INK, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::

::: {.takeaway}
Many components, one continuous ramp keyed to vertical position, so every band is its own colour and you can still track a lineage over time.
:::
