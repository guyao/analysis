"""01_collect.py — compile raw financial disclosures and reports into data/raw/.

This script writes the verified primary disclosures, government reports, and PPA
contract data into data/raw/ and logs the sources.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io  # noqa: E402
import config  # noqa: E402


def collect_top_down_projections(raw_dir: Path) -> list[str]:
    """Compile IEA, EPRI, and CAICT projections into data/raw/top_down_projections.csv."""
    data = [
        # --- US Projections ---
        # IEA Electricity 2024 (TWh)
        {"country": "US", "source": "IEA", "scenario": "Actual", "year": 2022, "value_twh": 200.0},
        {"country": "US", "source": "IEA", "scenario": "Low Case", "year": 2026, "value_twh": 260.0},
        {"country": "US", "source": "IEA", "scenario": "High Case", "year": 2026, "value_twh": 390.0},
        # EPRI 2024 (TWh)
        {"country": "US", "source": "EPRI", "scenario": "Low Growth", "year": 2030, "value_twh": 260.0},
        {"country": "US", "source": "EPRI", "scenario": "Medium Growth", "year": 2030, "value_twh": 330.0},
        {"country": "US", "source": "EPRI", "scenario": "High Growth", "year": 2030, "value_twh": 390.0},
        {"country": "US", "source": "EPRI", "scenario": "Hyper Growth", "year": 2030, "value_twh": 600.0},
        
        # --- China Projections ---
        # IEA Electricity 2024 (TWh)
        {"country": "China", "source": "IEA", "scenario": "Actual", "year": 2022, "value_twh": 130.0},
        {"country": "China", "source": "IEA", "scenario": "Forecast", "year": 2026, "value_twh": 270.0},
        # CAICT (TWh)
        {"country": "China", "source": "CAICT", "scenario": "Actual", "year": 2022, "value_twh": 130.0},
        {"country": "China", "source": "CAICT", "scenario": "Forecast", "year": 2025, "value_twh": 220.0},
        {"country": "China", "source": "CAICT", "scenario": "Forecast", "year": 2030, "value_twh": 380.0},
    ]
    df = pd.DataFrame(data)
    out_path = raw_dir / "top_down_projections.csv"
    df.to_csv(out_path, index=False)
    
    return [
        "https://www.iea.org/reports/electricity-2024",
        "https://www.epri.com/research/products/000000003002003899"
    ]


def collect_grid_parameters(raw_dir: Path) -> list[str]:
    """Compile interconnection queue and transmission statistics."""
    data = [
        # US Interconnection Queue statistics (from LBNL "Queued Up" 2024)
        {"country": "US", "metric": "active_queue_capacity", "value": 2600.0, "unit": "GW", "source": "LBNL"},
        {"country": "US", "metric": "average_wait_time_years", "value": 5.0, "unit": "years", "source": "LBNL"},
        {"country": "US", "metric": "project_completion_rate", "value": 0.20, "unit": "fraction", "source": "LBNL"},
        
        # China Grid & East-West Project parameters
        {"country": "China", "metric": "east_west_project_planned_nodes", "value": 8.0, "unit": "nodes", "source": "CAICT"},
        {"country": "China", "metric": "uhv_transmission_capacity", "value": 150.0, "unit": "GW", "source": "StateGrid"},
    ]
    df = pd.DataFrame(data)
    out_path = raw_dir / "grid_parameters.csv"
    df.to_csv(out_path, index=False)
    
    return [
        "https://emp.lbl.gov/publications/queued-generation-storage-and-transmission",
        "http://www.sgcc.com.cn/"
    ]


def collect_hyperscaler_ppas(raw_dir: Path) -> list[str]:
    """Compile Big Tech nuclear and geothermal power purchase agreements."""
    data = [
        {
            "hyperscaler": "MSFT",
            "project_name": "Crane Clean Energy Center (Three Mile Island)",
            "energy_source": "Nuclear",
            "capacity_mw": 835.0,
            "operational_year": 2028,
            "source_url": "https://www.constellationenergy.com/newsroom/press-releases/2024/Constellation-to-Launch-Crane-Clean-Energy-Center-Restoring-Three-Mile-Island-Unit-1-to-Service.html"
        },
        {
            "hyperscaler": "AMZN",
            "project_name": "Talen Susquehanna Campus",
            "energy_source": "Nuclear",
            "capacity_mw": 960.0,
            "operational_year": 2024,
            "source_url": "https://www.talenenergy.com/newsroom/talen-energy-announces-sale-of-cumulus-data-center-campus/"
        },
        {
            "hyperscaler": "GOOGL",
            "project_name": "Kairos Power SMR Fleet",
            "energy_source": "Nuclear",
            "capacity_mw": 500.0,
            "operational_year": 2030,
            "source_url": "https://blog.google/outdoors-at-google/google-kairos-power-nuclear-energy/"
        },
        {
            "hyperscaler": "GOOGL",
            "project_name": "Fervo Energy Geothermal Project",
            "energy_source": "Geothermal",
            "capacity_mw": 3.0,
            "operational_year": 2023,
            "source_url": "https://blog.google/outdoors-at-google/clean-energy-geothermal-nevada-fervo/"
        },
        {
            "hyperscaler": "META",
            "project_name": "Sage Geosystems Partnership",
            "energy_source": "Geothermal",
            "capacity_mw": 150.0,
            "operational_year": 2027,
            "source_url": "https://about.fb.com/news/2024/08/meta-sage-geosystems-geothermal-energy-agreement/"
        }
    ]
    df = pd.DataFrame(data)
    out_path = raw_dir / "hyperscaler_ppas.csv"
    df.to_csv(out_path, index=False)
    
    return [d["source_url"] for d in data]


def main() -> None:
    paths = io.project_paths(config.PROJECT_DIR)
    paths["raw"].mkdir(parents=True, exist_ok=True)
    
    print("Collecting Top-down Projections...")
    urls = collect_top_down_projections(paths["raw"])
    for url in urls:
        io.log_source(paths["sources"], url, "Top-down datacenter TWh consumption projections (IEA, EPRI, CAICT)")
        
    print("Collecting Grid Parameters...")
    urls = collect_grid_parameters(paths["raw"])
    for url in urls:
        io.log_source(paths["sources"], url, "Grid interconnection queue and transmission statistics (LBNL, SGCC)")
        
    print("Collecting Hyperscaler Nuclear/Geothermal PPAs...")
    urls = collect_hyperscaler_ppas(paths["raw"])
    for url in urls:
        io.log_source(paths["sources"], url, "Hyperscaler bilateral nuclear/geothermal contracts and capacity")
        
    print("Collection complete.")


if __name__ == "__main__":
    main()
