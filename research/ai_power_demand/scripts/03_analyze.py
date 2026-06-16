"""03_analyze.py — calculate AI bottom-up demand and net grid deficits.

Consumes clean parquet files and outputs comparison tables and charts.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(PROJECT / "scripts"))

from utils import io, plotting  # noqa: E402
import config  # noqa: E402

# Conversion factor
GW_TO_TWH_FACTOR = 8.76


def calculate_bottom_up_demand(country: str, scenario: str) -> tuple[float, float]:
    """Calculate 2030 bottom-up power demand (in GW and TWh)."""
    # Active GPUs in millions
    n_gpus = config.GPU_DEPLOYMENT_SCENARIOS_2030[country][scenario] * 1e6
    gpu_tdp = config.GPU_TDP_KW["H100"]  # Blended average GPU TDP in kW
    pue = config.AVERAGE_PUE
    
    # Power demand in GW
    gw = (n_gpus * gpu_tdp * pue) / 1e6
    twh = gw * GW_TO_TWH_FACTOR
    return round(gw, 2), round(twh, 2)


def main() -> None:
    paths = io.project_paths(PROJECT)
    
    # Load processed data
    projections = pd.read_parquet(paths["processed"] / "projections_clean.parquet")
    grid = pd.read_parquet(paths["processed"] / "grid_parameters_clean.parquet")
    ppas = pd.read_parquet(paths["processed"] / "hyperscaler_ppas_clean.parquet")
    
    # Calculate bottom-up scenarios for 2030
    bu_results = {}
    for country in ["US", "China"]:
        bu_results[country] = {}
        for scenario in ["low", "medium", "high"]:
            gw, twh = calculate_bottom_up_demand(country, scenario)
            bu_results[country][scenario] = {"gw": gw, "twh": twh}
            
    # Calculate total PPA capacity (US only, as Chinese firms rely on grid-allocated green bases)
    total_ppa_mw = ppas["capacity_mw"].sum()
    total_ppa_gw = total_ppa_mw / 1000.0
    
    # Get grid parameters
    us_wait = grid[(grid["country"] == "US") & (grid["metric"] == "average_wait_time_years")]["value"].values[0]
    us_queue = grid[(grid["country"] == "US") & (grid["metric"] == "active_queue_capacity")]["value"].values[0]
    china_uhv = grid[(grid["country"] == "China") & (grid["metric"] == "uhv_transmission_capacity")]["value"].values[0]
    
    # Calculate grid deficit
    # For US: bottom-up medium demand (7.0 GW) - secured PPAs (2.45 GW) = 4.55 GW net grid demand.
    # Given the 5-year queue wait time, this creates a temporary grid capacity deficit.
    us_net_grid_gw = bu_results["US"]["medium"]["gw"] - total_ppa_gw
    
    # Compile comparison table
    comparison_data = [
        {
            "parameter": "AI GPU Blended Power TDP",
            "us_value": f"{config.GPU_TDP_KW['H100']} kW",
            "china_value": f"{config.GPU_TDP_KW['H100']} kW",
            "unit": "kW",
            "description": "Blended average TDP per active GPU node"
        },
        {
            "parameter": "Projected Active GPUs (Medium, 2030)",
            "us_value": f"{config.GPU_DEPLOYMENT_SCENARIOS_2030['US']['medium']} million",
            "china_value": f"{config.GPU_DEPLOYMENT_SCENARIOS_2030['China']['medium']} million",
            "unit": "million",
            "description": "Projected active equivalent GPU footprint"
        },
        {
            "parameter": "Bottom-up AI Power Demand (Low, 2030)",
            "us_value": f"{bu_results['US']['low']['gw']} GW",
            "china_value": f"{bu_results['China']['low']['gw']} GW",
            "unit": "GW",
            "description": "Estimated power load in Low deployment scenario"
        },
        {
            "parameter": "Bottom-up AI Power Demand (Medium, 2030)",
            "us_value": f"{bu_results['US']['medium']['gw']} GW",
            "china_value": f"{bu_results['China']['medium']['gw']} GW",
            "unit": "GW",
            "description": "Estimated power load in Medium deployment scenario"
        },
        {
            "parameter": "Bottom-up AI Power Demand (High, 2030)",
            "us_value": f"{bu_results['US']['high']['gw']} GW",
            "china_value": f"{bu_results['China']['high']['gw']} GW",
            "unit": "GW",
            "description": "Estimated power load in High deployment scenario"
        },
        {
            "parameter": "Top-down Projected Consumption (2030)",
            "us_value": "330.0 TWh (37.67 GW)",
            "china_value": "380.0 TWh (43.38 GW)",
            "unit": "TWh (GW)",
            "description": "Top-down projections from EPRI (US Medium) and CAICT (China)"
        },
        {
            "parameter": "Bilateral Secured PPAs (Nuclear/Geothermal)",
            "us_value": f"{total_ppa_gw:.3f} GW",
            "china_value": "0.0 GW",
            "unit": "GW",
            "description": "Secured bilateral clean energy contracts by hyperscalers"
        },
        {
            "parameter": "Net Grid Power Required (2030 Medium)",
            "us_value": f"{us_net_grid_gw:.2f} GW",
            "china_value": f"{bu_results['China']['medium']['gw']} GW",
            "unit": "GW",
            "description": "Projected demand that must go through standard grid"
        },
        {
            "parameter": "Grid Interconnection Queue Wait Time",
            "us_value": f"{us_wait} years",
            "china_value": "N/A (Centralized planning)",
            "unit": "years",
            "description": "Average wait time in grid interconnection queue"
        },
        {
            "parameter": "Grid Capacity Metric",
            "us_value": f"Queue: {us_queue} GW",
            "china_value": f"UHV Line Capacity: {china_uhv} GW",
            "unit": "GW",
            "description": "US active interconnection queue capacity vs China UHV line capacity"
        }
    ]
    
    df_comp = pd.DataFrame(comparison_data)
    io.write_processed(df_comp, paths["tables"] / "us_china_comparison.csv")
    
    # 4. Generate comparison charts
    plotting.apply_default_style()
    
    # Chart 1: Datacenter Electricity Consumption Projections (TWh)
    # Prepare historical and forecast points
    years = [2022, 2026, 2030]
    us_points = [200.0, 330.0, 390.0]  # EPRI Medium
    china_points = [130.0, 270.0, 380.0] # CAICT
    
    # Create figure
    fig1 = plotting.line_chart(
        years, us_points,
        title="Projected Datacenter Power Demand (TWh/year)",
        xlabel="Year", ylabel="TWh / year",
        label="US (EPRI Medium)"
    )
    ax1 = fig1.axes[0]
    ax1.plot(years, china_points, label="China (CAICT/IEA)", marker='o')
    # Add bottom-up projections as markers at 2030
    ax1.scatter([2030], [bu_results["US"]["medium"]["twh"]], color='red', label="US Bottom-up (Medium)", zorder=5)
    ax1.scatter([2030], [bu_results["China"]["medium"]["twh"]], color='orange', label="China Bottom-up (Medium)", zorder=5)
    ax1.legend()
    plotting.save_figure(fig1, paths["figures"] / "demand_scenarios.png")
    
    # Chart 2: Bottleneck comparison
    # Plot US Interconnection queue vs China UHV Capacity
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    categories = ["US Interconnection Queue", "China UHV Grid Capacity"]
    values = [us_queue, china_uhv]
    ax2.bar(categories, values, color=["#1f77b4", "#2ca02c"])
    ax2.set_ylabel("Capacity (GW)")
    ax2.set_title("Grid Infrastructure Bottleneck Metrics")
    plotting.save_figure(fig2, paths["figures"] / "bottlenecks.png")
    
    print("\nanalysis complete. Wrote:")
    print("  output/tables/us_china_comparison.csv")
    print("  output/figures/demand_scenarios.png")
    print("  output/figures/bottlenecks.png")
    
    print("\nUS vs. China Power Deficit Comparison Table:")
    print(df_comp.to_string(index=False))


if __name__ == "__main__":
    main()
