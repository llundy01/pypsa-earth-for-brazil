# Custom figure rules for the Brazil dissertation.
# Enabled via config.yaml:  custom_rules: ["custom_figures.smk"]
# Run with:                 snakemake -j1 plot_base_network
# Output:                   results/<run>/figures/base_network_map.{png,pdf,svg}

rule plot_base_network:
    input:
        lines="resources/" + RDIR + "base_network/all_lines_build_network.geojson",
        substations="resources/" + RDIR + "base_network/all_buses_build_network.geojson",
    output:
        "results/" + RDIR + "figures/base_network_map.png",
        "results/" + RDIR + "figures/base_network_map.pdf",
    script:
        "scripts/plot_network_map.py"
