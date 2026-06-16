"""02_clean.py — standardize raw tables and align metrics (TWh and GW).

Reads raw CSVs, standardizes names, converts between TWh and GW continuous power
(using TWh = GW * 8.76), and writes clean parquet files to data/processed/.
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

# Standard physical conversion: 1 GW continuous power for 1 year (8760 hours) = 8.76 TWh.
HOURS_PER_YEAR = 8760.0
GW_TO_TWH_FACTOR = 8.76


def twh_to_gw(twh: float) -> float:
    """Convert TWh annual consumption to average continuous GW load."""
    return twh / GW_TO_TWH_FACTOR


def gw_to_twh(gw: float) -> float:
    """Convert GW continuous capacity to annual TWh consumption."""
    return gw * GW_TO_TWH_FACTOR


def clean_projections(raw_path: Path, proc_path: Path) -> None:
    """Standardize top-down projections and add GW continuous equivalent columns."""
    df = pd.read_csv(raw_path)
    
    # Calculate GW continuous equivalent
    df["value_gw_eq"] = df["value_twh"].apply(twh_to_gw)
    
    # Round metrics for presentation
    df["value_twh"] = df["value_twh"].round(2)
    df["value_gw_eq"] = df["value_gw_eq"].round(2)
    
    io.write_processed(df, proc_path)
    print(f"  Cleaned projections: wrote {proc_path} ({len(df)} rows)")


def clean_grid_parameters(raw_path: Path, proc_path: Path) -> None:
    """Normalize grid parameters."""
    df = pd.read_csv(raw_path)
    io.write_processed(df, proc_path)
    print(f"  Cleaned grid parameters: wrote {proc_path} ({len(df)} rows)")


def clean_hyperscaler_ppas(raw_path: Path, proc_path: Path) -> None:
    """Standardize hyperscaler PPAs, adding TWh annual equivalent columns."""
    df = pd.read_csv(raw_path)
    
    # Calculate TWh annual generation potential (assuming 90% capacity factor for nuclear/geothermal)
    CAPACITY_FACTOR = 0.90
    df["capacity_gw"] = df["capacity_mw"] / 1000.0
    df["generation_twh_eq"] = df["capacity_gw"].apply(gw_to_twh) * CAPACITY_FACTOR
    
    # Round metrics
    df["capacity_gw"] = df["capacity_gw"].round(4)
    df["generation_twh_eq"] = df["generation_twh_eq"].round(4)
    
    io.write_processed(df, proc_path)
    print(f"  Cleaned hyperscaler PPAs: wrote {proc_path} ({len(df)} rows)")


def main() -> None:
    paths = io.project_paths(PROJECT)
    
    print("Cleaning projections data...")
    clean_projections(
        paths["raw"] / "top_down_projections.csv",
        paths["processed"] / "projections_clean.parquet"
    )
    
    print("Cleaning grid parameters...")
    clean_grid_parameters(
        paths["raw"] / "grid_parameters.csv",
        paths["processed"] / "grid_parameters_clean.parquet"
    )
    
    print("Cleaning hyperscaler PPAs...")
    clean_hyperscaler_ppas(
        paths["raw"] / "hyperscaler_ppas.csv",
        paths["processed"] / "hyperscaler_ppas_clean.parquet"
    )
    
    print("Cleaning complete.")


if __name__ == "__main__":
    main()
