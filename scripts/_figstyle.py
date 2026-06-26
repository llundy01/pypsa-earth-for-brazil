"""
Shared figure style for the Brazil dissertation.
Import this in every plotting script so all figures look the same.

    from _figstyle import apply_style, CARRIER_COLORS, VOLTAGE_COLORS, save_fig
    apply_style()
    ...
    save_fig(fig, "my_figure")          # -> results/figures/my_figure.{png,pdf,svg}

Font matches the LaTeX thesis (Helvetica sans-serif, 11 pt).
"""
import os
import matplotlib.pyplot as plt

# --- colour palettes (theme "Aguas": Brazil + hydro) ------------------------
CARRIER_COLORS = {
    "hydro":         "#1B6CA8",
    "ror":           "#1B6CA8",   # run-of-river = hydro
    "wind":          "#43AA8B",
    "onwind":        "#43AA8B",
    "offwind":       "#2A9D8F",
    "offwind-ac":    "#2A9D8F",
    "offwind-dc":    "#21867A",
    "solar":         "#F2C14E",
    "biomass":       "#6A994E",
    "gas":           "#E07A5F",
    "OCGT":          "#E07A5F",
    "CCGT":          "#C85C42",
    "coal":          "#3D405B",
    "lignite":       "#5A5D7A",
    "nuclear":       "#C44536",
    "oil":           "#7D5BA6",
    "load_shedding": "#BBBBBB",
}

# voltage ramp for network maps (low -> high)
VOLTAGE_COLORS = {
    765: "#d62728", 525: "#ff7f0e", 500: "#ffae5e", 440: "#9467bd",
    345: "#2ca02c", 230: "#1f77b4", 138: "#17becf", 88: "#8c8c8c", 69: "#c7c7c7",
}
VOLTAGE_LEVELS = [765, 525, 500, 440, 345, 230, 138, 88, 69]


def apply_style():
    """Apply the shared rcParams. Call once at the top of every figure script."""
    plt.rcParams.update({
        "font.family":      "sans-serif",
        "font.sans-serif":  ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size":        11,
        "axes.titlesize":   13,
        "axes.titleweight": "bold",
        "axes.labelsize":   11,
        "axes.linewidth":   0.6,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":        True,
        "grid.linestyle":   ":",
        "grid.alpha":       0.35,
        "grid.linewidth":   0.5,
        "legend.fontsize":  9,
        "legend.frameon":   False,
        "legend.title_fontsize": 10,
        "xtick.labelsize":  9,
        "ytick.labelsize":  9,
        "figure.dpi":       120,
        "savefig.dpi":      300,
        "savefig.bbox":     "tight",
    })


def voltage_bin(kv):
    """Snap an arbitrary kV value to the nearest standard level (for colouring)."""
    return min(VOLTAGE_LEVELS, key=lambda o: abs(o - kv))


def save_fig(fig, name, outdir="results/figures", formats=("png", "pdf", "svg")):
    """Save a figure to results/figures/ in several formats (PNG preview, PDF/SVG vector)."""
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for fmt in formats:
        p = os.path.join(outdir, f"{name}.{fmt}")
        fig.savefig(p, format=fmt)
        paths.append(p)
    return paths
