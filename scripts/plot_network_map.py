"""
Plot the transmission network with precise line geometries coloured by voltage.

Two ways to run:
  * as a Snakemake script (a `snakemake` object is injected) -> uses its input/output
  * standalone:  python scripts/plot_network_map.py LINES.geojson [SUBSTATIONS.geojson]

Reads a GeoJSON of LineStrings with a `voltage` (or `v_nom`) property; optionally a
GeoJSON of substation Points. Uses the shared style in _figstyle.py.
"""
import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _figstyle import apply_style, VOLTAGE_COLORS, VOLTAGE_LEVELS, voltage_bin, save_fig


def _features(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["features"]


def plot_network(lines_path, subs_path=None, out_name="network_map",
                 outdir="results/figures",
                 title="Brazilian transmission network — lines by voltage"):
    apply_style()

    groups = {o: [] for o in VOLTAGE_LEVELS}
    for ft in _features(lines_path):
        p = ft["properties"]
        v = p.get("voltage") or p.get("v_nom") or 0
        kv = v / 1000 if v > 1000 else v
        geom = ft.get("geometry") or {}
        if not kv or geom.get("type") != "LineString":
            continue
        groups[voltage_bin(round(kv))].append(np.array(geom["coordinates"]))

    fig, ax = plt.subplots(figsize=(9, 9))
    for o in sorted(VOLTAGE_LEVELS):                 # low voltage first (background)
        if groups[o]:
            lw = 0.3 + (o / 765.0) * 1.6
            ax.add_collection(LineCollection(groups[o], colors=VOLTAGE_COLORS[o], linewidths=lw))

    if subs_path:
        xs, ys = [], []
        for ft in _features(subs_path):
            p, geom = ft["properties"], ft.get("geometry") or {}
            if "lon" in p and "lat" in p:
                xs.append(p["lon"]); ys.append(p["lat"])
            elif geom.get("type") == "Point":
                xs.append(geom["coordinates"][0]); ys.append(geom["coordinates"][1])
        ax.scatter(xs, ys, s=1.2, c="k", alpha=0.3, linewidths=0, zorder=5)

    ax.set_xlim(-75, -32)
    ax.set_ylim(-35, 7)
    ax.set_aspect(1 / math.cos(math.radians(-12)))
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    handles = [Line2D([0], [0], color=VOLTAGE_COLORS[o], lw=2.5, label=f"{o} kV")
               for o in VOLTAGE_LEVELS if groups[o]]
    ax.legend(handles=handles, title="Voltage (kV)", loc="lower left")
    fig.tight_layout()

    paths = save_fig(fig, out_name, outdir=outdir)
    print("saved:", *paths, sep="\n  ")
    return paths


if "snakemake" in globals():
    smk = globals()["snakemake"]
    subs = smk.input.get("substations") if hasattr(smk.input, "get") else None
    plot_network(smk.input.lines, subs,
                 out_name="base_network_map",
                 outdir=os.path.dirname(smk.output[0]))
elif __name__ == "__main__":
    lines = sys.argv[1] if len(sys.argv) > 1 else "data/custom_lines.geojson"
    subs = sys.argv[2] if len(sys.argv) > 2 else None
    plot_network(lines, subs)
