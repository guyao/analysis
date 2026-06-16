# AI Power Demand & Grid Deficit: US vs. China

This project analyzes the projected electricity demand of AI datacenters in the United States and China through 2030, evaluates the capacity of each country's power grid to fulfill this demand, and quantifies the grid deficits and comparative structural bottlenecks.

## Research Question (Falsifiable)
Can the electricity grids of the United States and China generate and transmit enough power to fulfill projected AI datacenter demand through 2030, what is the calculated deficit (in GW/TWh), and which country possesses a structural advantage in overcoming grid capacity constraints?

## Hypotheses
*   **H1 (structural deficit bottleneck):** Both countries will experience localized power deficits for AI datacenters. However, the bottleneck in the US is institutional and regulatory (grid interconnection queues, permitting delays, fragmented ISO/RTO regions), whereas the bottleneck in China is geopolitical and geographical (chip technology constraints, regional mismatch between western power generation bases and eastern demand centers).
*   **H2 (renewable deployment speed):** China's state-directed grid planning and centralized investment will allow it to deploy and connect new renewable capacity (solar, wind) and transmission (UHV lines) to datacenters faster than the US market-driven, fragmented grid system.
*   **H3 (private nuclear power contribution):** US hyperscalers will rely heavily on bilateral, off-grid power purchase agreements (PPAs)—particularly co-located nuclear power plants—to bypass grid connection queues, contributing over 5 GW of dedicated capacity by 2030, whereas Chinese hyperscalers will rely on state-allocated capacity from massive national wind/solar bases.

## Methodology & Metrics
1.  **AI Power Demand Projections (US vs. China):**
    *   Estimated from GPU shipment numbers, average power consumption per node (e.g. NVIDIA H100/H200, Blackwell B200), and projected datacenter Power Usage Effectiveness (PUE) ratios.
    *   Compare industry projections (IEA, EPRI, Boston Consulting Group, McKinsey) for datacenter electricity share of total load.
2.  **Grid Interconnection & Transmission Capacity:**
    *   US: Analyze PJM, ERCOT, MISO, CAISO interconnection queues and average wait times.
    *   China: Analyze the "East-West Data Center Computing" (东数西算) project, UHV transmission capacity, and State Grid additions.
3.  **Big Tech PPA Contribution Analysis:**
    *   Log and analyze tech hyperscaler nuclear/clean energy deals (e.g. Microsoft/Constellation, Amazon/Talen, Google/Fervo) and calculate their capacity contribution.
4.  **Calculated Deficits:**
    *   Grid deficit = Projected AI Datacenter Power Demand (GW) - (Secured Off-Grid Capacity + State-Planned Datacenter Allocation).
    *   Load growth impact = AI load addition as a percentage of total grid additions.

## Data Sources (Logged in sources.md)
*   International Energy Agency (IEA) Electricity Reports.
*   US Department of Energy (DOE) and Federal Energy Regulatory Commission (FERC) queue databases.
*   China National Energy Administration (NEA) grid stats and State Grid Corporation annual reports.
*   Company press releases and financial filings (MSFT, AMZN, GOOGL, META) regarding energy PPAs.

## Structure
```
ai_power_demand/
├── README.md          # this file
├── data/
│   ├── raw/           # immutable reports, SEC filings, power statistics
│   └── processed/     # cleaned and unified demand/supply tables
├── scripts/           # collection, cleaning, and model projections
│   ├── config.py
│   ├── 01_collect.py
│   ├── 02_clean.py
│   └── 03_analyze.py
└── output/
    ├── tables/        # deficit projections table
    ├── figures/       # US vs China power deficit chart
    └── report.en.ipynb   # final report and model execution
```

## Conclusions
Our comparative quantitative analysis of the US and China AI power demand and deficits yields the following core conclusions:

1. **Strategic Bottleneck Mismatch (H1 Supported):**
   * **US Bottleneck:** Institutional and regulatory. The US grid has an active interconnection queue of **2,600 GW**, but projects face an average **5.0-year wait time** with only a **20% completion rate**. 
   * **China Bottleneck:** Geopolitical and technological. China has constructed a massive UHV grid with **150 GW of transmission capacity** for its **"East-West Data Center Computing" (东数西算)** project, but is limited by chip availability.

2. **Chinese Infrastructure Lead (H2 Supported):**
   * China's centralized state grid planning allows immediate allocation of UHV-linked renewable capacity to computing hubs. In contrast, the US market is fragmented, leading to severe localized deficits due to permitting delays.

3. **US Private Off-Grid Pivot (H3 Supported):**
   * US hyperscalers are actively bypassing the grid using bilateral clean energy PPAs (e.g., nuclear and geothermal). Secured contracts stand at **2.448 GW** (including Microsoft's 835 MW Crane Center/Three Mile Island deal and AWS's 960 MW Susquehanna deal). This private capacity covers **35%** of the projected 7.0 GW US bottom-up medium AI demand by 2030.

All tables, figures, and models are fully reproducible. See `output/report.en.ipynb` for the full model execution and discussion.


