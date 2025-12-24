# Data Visualization for Genomics - Day 1 Presentation

This Quarto presentation is inspired by Cédric Scherer's elegant style, adapted for genomics education.

## Files Included

- `genomics-viz-day1.qmd` - Main presentation file
- `slides.scss` - Custom styling with genomics-themed colors

## Color Scheme

- **Primary Blue** (#0077BE) - DNA/Science theme
- **Secondary Green** (#00A651) - Biology/Life
- **Tertiary Amber** (#E8A627) - Discovery/Energy
- **Accent Purple** (#C75DAB) - Bioinformatics

## What You Need

### Required R Packages
```r
install.packages(c(
  "quarto",
  "rmarkdown", 
  "ggplot2",
  "dplyr",
  "patchwork",
  "pheatmap",
  "gdtools"
))
```

### Required Directory Structure
```
your-project/
├── genomics-viz-day1.qmd
├── slides.scss
└── img/                    # Create this folder
    └── (add your images here)
```

## Images Needed

Based on your slides, you'll need to add these images to the `img/` folder:

1. `bg-dna-pattern.png` - Background for title slide (can be any DNA helix pattern)
2. `data-comic.png` - Comic about data analysis (from your slide 2)

**Tip:** You can create a simple DNA pattern background using online tools or leave it as a solid color initially.

## How to Render

### In RStudio:
1. Open `genomics-viz-day1.qmd`
2. Click the "Render" button
3. Or run: `quarto::quarto_render("genomics-viz-day1.qmd")`

### From Terminal:
```bash
quarto render genomics-viz-day1.qmd
```

## Customization Tips

### Change Colors
Edit the color variables in `slides.scss`:
```scss
$color-primary:    #0077BE;  // Your main color
$color-secondary:  #00A651;  // Your accent color
```

### Add More Slides
Use the existing structure:

```markdown
## New Slide Title

Content here...
```

### Add Code Examples
```markdown
## Code Example

```{r}
#| echo: true
#| eval: true
library(ggplot2)
ggplot(data, aes(x, y)) + geom_point()
```
```

### Create Section Dividers
```markdown
# Section Title {background-color="#0077BE"}
```

## Current Slides Included

1. ✅ Title Slide
2. ✅ Why data visualizations? (Anscombe's Quartet)
3. ✅ Big data in biology
4. ✅ How we're going to work
5. ✅ What else you need (PollEv)
6. ✅ Section: Common types of visualizations
7. ✅ Learning objectives
8. ✅ Scatter plots
9. ✅ Bar charts (with examples)
10. ✅ Box plots and violin plots
11. ✅ Heatmaps
12. ✅ Closing slide

## Next Steps

1. **Add your actual data** - Replace the simulated data with your real genomics examples
2. **Add images** - Place your images in the `img/` folder
3. **Customize content** - Adjust text to match your teaching style
4. **Add more examples** - Include real genomics case studies from your research

## Features from Cédric's Style

- ✨ Professional typography
- 🎨 Custom color schemes
- 📊 Integrated R code and plots
- 🎯 Progressive disclosure with fragments
- 🖼️ Clean, modern layout
- 📱 Responsive design

## Questions or Issues?

Contact: loukas.theodosiou@bio.auth.gr

---

**License:** Feel free to adapt and share with appropriate credit
**Based on:** Cédric Scherer's ggiraph workshop style (useR 2025)
