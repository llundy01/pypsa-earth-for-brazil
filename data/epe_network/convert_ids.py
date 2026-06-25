"""
Convert EPE custom network IDs (strings -> integers) for PyPSA-Earth.

PyPSA-Earth's clean_osm_data casts line_id (L338) and bus_id (L270) to int.
Our EPE export uses string IDs (ml_line_0, ml_st_0_525) -> crash.
This script rewrites the IDs as integers and writes a mapping table so we can
trace each integer ID back to the original EPE object later (needed to target
named lines in the wildfire scenario).

Geometry, voltages and all other attributes are left untouched.
Outputs go next to the source files, in data code/converted/.
"""
import json
import csv
import re
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "converted")


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def dump(obj, name):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)


def write_csv(rows, header, name):
    with open(os.path.join(BASE, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ---- LINES: line_id -> sequential int (0..N-1) ------------------------------
lines = load("all_clean_lines.geojson")
map_lines = []
for i, ft in enumerate(lines["features"]):
    p = ft["properties"]
    orig = p.get("line_id")
    p["line_id"] = i  # integer
    map_lines.append([i, orig, p.get("voltage"), p.get("length")])
dump(lines, "custom_lines.geojson")
write_csv(map_lines, ["new_line_id", "epe_line_id", "voltage_V", "length_km"],
          "mapping_lines.csv")

# ---- SUBSTATIONS: bus_id -> seq int; station_id -> int parsed from ml_st_K --
subs = load("all_clean_substations.geojson")
map_subs = []
for i, ft in enumerate(subs["features"]):
    p = ft["properties"]
    orig_bus = p.get("bus_id")
    orig_st = p.get("station_id")
    m = re.search(r"(\d+)", str(orig_st))
    st_int = int(m.group(1)) if m else i  # keeps stations grouped
    p["bus_id"] = i  # integer, unique
    p["station_id"] = st_int
    map_subs.append([i, orig_bus, st_int, orig_st,
                     p.get("voltage"), p.get("lon"), p.get("lat")])
dump(subs, "custom_substations.geojson")
write_csv(map_subs,
          ["new_bus_id", "epe_bus_id", "new_station_id", "epe_station_id",
           "voltage_V", "lon", "lat"],
          "mapping_substations.csv")

# ---- summary ----------------------------------------------------------------
print("LINES:", len(lines["features"]), "-> custom_lines.geojson")
print("   line_id sample:", [f["properties"]["line_id"] for f in lines["features"][:3]])
print("SUBSTATIONS:", len(subs["features"]), "-> custom_substations.geojson")
print("   bus_id sample:", [f["properties"]["bus_id"] for f in subs["features"][:3]])
print("   station_id sample:", [f["properties"]["station_id"] for f in subs["features"][:3]])
n_stations = len(set(r[2] for r in map_subs))
print("   distinct stations:", n_stations, "(buses:", len(map_subs), ")")
print("Mapping tables: mapping_lines.csv, mapping_substations.csv")
