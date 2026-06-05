import matplotlib.pyplot as plt

BRAND       = '#28A87D'
BRAND_LIGHT = '#79DFBD'
BRAND_BG    = '#E8F5F1'
ACCENT_YLW  = '#FFD166'
ACCENT_PURP = '#7754BF'
GRAY_DARK   = '#606060'
RED         = '#E74C3C'

COURSE_PAL = [
    '#28A87D', '#E8A838', '#7754BF', '#E74C3C', '#3498DB',
    '#F39C12', '#16A085', '#8E44AD', '#C0392B', '#2980B9',
]


def apply_course_theme():
    """Apply the publication-ready matplotlib style used across all course slides."""
    plt.rcParams.update({
        'figure.facecolor' : 'white',
        'axes.facecolor'   : 'white',
        'axes.grid'        : True,
        'grid.color'       : '#e8e8e8',
        'grid.linestyle'   : '--',
        'grid.linewidth'   : 0.5,
        'axes.spines.top'  : False,
        'axes.spines.right': False,
        'font.size'        : 11,
        'axes.titlesize'   : 14,
        'axes.titleweight' : 'bold',
        'axes.labelsize'   : 12,
        'xtick.labelsize'  : 10,
        'ytick.labelsize'  : 10,
        'legend.fontsize'  : 10,
        'figure.titlesize' : 16,
        'figure.dpi'       : 150,
    })


def get_palette(n: int = 10) -> list[str]:
    """Return up to n colours from the course palette, cycling if necessary."""
    if n <= len(COURSE_PAL):
        return COURSE_PAL[:n]
    cycles = (n // len(COURSE_PAL)) + 1
    return (COURSE_PAL * cycles)[:n]
