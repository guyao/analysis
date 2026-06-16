"""Shared configuration and parameters for the AI power demand study.
"""

from __future__ import annotations
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

# Tickers of interest for hyperscaler analysis
HYPERSCALERS = ("MSFT", "AMZN", "GOOGL", "META")

# GPU parameters (Thermal Design Power in kW)
GPU_TDP_KW = {
    "H100": 0.7,
    "B200": 1.2,
    "H200": 0.85,
}

# Average AI datacenter PUE range
AVERAGE_PUE = 1.25

# Scenarios for cumulative active GPUs deployed by 2030 (in millions)
# US is expected to have a much larger share of leading-edge GPUs due to export restrictions.
GPU_DEPLOYMENT_SCENARIOS_2030 = {
    "US": {
        "low": 5.0,     # 5 million active H100 equivalents
        "medium": 8.0,  # 8 million active H100 equivalents
        "high": 12.0    # 12 million active H100 equivalents
    },
    "China": {
        "low": 1.0,     # 1 million active equivalent GPUs (mostly localized/lower TDP)
        "medium": 2.0,  # 2 million active equivalent GPUs
        "high": 3.5     # 3.5 million active equivalent GPUs
    }
}
