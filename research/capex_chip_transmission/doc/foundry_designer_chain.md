# Foundry & Designer Supply Chain Map

This document maps the advanced logic chip foundry (晶圆代工厂) and chip designer (设计商) layers, focusing on TSMC, Samsung, Intel, and AMD, and analyzes their advanced packaging capacities and transmission lags.

---

## 1. Advanced Logic Foundries (晶圆代工厂)

Leading-edge wafer manufacturing is consolidated among three global players with sub-5nm capabilities:

*   **TSMC (Taiwan Semiconductor Manufacturing Co. - Ticker: `TSM`):**
    *   **Market Share (Advanced Nodes < 7nm):** >85%.
    *   **Leading Nodes:** 3nm (N3B/N3E) in mass production; 2nm (N2) planned for 2025/2026.
    *   **Core Clients:** Apple, NVIDIA, AMD, Qualcomm, MediaTek, Intel.
    *   **Advanced Packaging:** CoWoS (Chip-on-Wafer-on-Substrate), SoIC (System on Integrated Chips).
*   **Samsung Foundry (Korea):**
    *   **Leading Nodes:** 3nm GAA (Gate-All-Around) in production; 2nm GAA planned for 2025.
    *   **Core Clients:** Qualcomm (some mobile chips), Samsung LSI, custom ASIC design firms.
    *   **Advanced Packaging:** I-Cube (2.5D), X-Cube (3D). Offering "turnkey" services combining HBM + Foundry + Packaging.
*   **Intel Foundry (US - Ticker: `INTC`):**
    *   **Leading Nodes:** Intel 4/Intel 3 in production; Intel 20A and Intel 18A (with backside power delivery PowerVia and GAA RibbonFET) planned for 2025.
    *   **Core Clients:** Internal (Intel client/server CPUs), Microsoft (custom chips on 18A), AWS, Cisco.
    *   **Advanced Packaging:** Foveros (3D stacking), EMIB (Embedded Multi-die Interconnect Bridge).

---

## 2. Advanced Packaging: The Ultimate AI Bottleneck

AI accelerators (such as NVIDIA Blackwell and AMD Instinct MI300) do not use single monolithic dies; they rely on **Multi-Chip Modules (MCM)** where logic dies and HBM stacks are integrated on a silicon interposer.

```
+-------------------------------------------------+
|                    GPU / ASIC                   |
|  +-------+  +-------+  +-------+  +-------+     |
|  |  HBM  |  | Logic |  | Logic |  |  HBM  |     |
|  +-------+  +-------+  +-------+  +-------+     |
|  +----------------------------------------+     |
|  |           Silicon Interposer           |     |  <-- CoWoS / I-Cube / Foveros
|  +----------------------------------------+     |
+-------------------------------------------------+
```

*   **TSMC CoWoS (Industry Standard):**
    *   **Capacity constraint:** The primary bottleneck for NVIDIA H100 and Blackwell shipments in 2023-2024.
    *   **Expansion:** Capacity doubled in 2024 (reaching ~30k-35k wafers/month) and is projected to double again in 2025.
*   **Intel Foveros:**
    *   Used extensively in Intel Gaudi 3 AI accelerators and client processors. Intel is actively selling Foveros as an open packaging service to external foundry customers.
*   **Samsung I-Cube:**
    *   Provides alternative packaging for clients who cannot secure enough TSMC CoWoS capacity.

---

## 3. Advanced Chip Designers (设计商)

*   **NVIDIA (Ticker: `NVDA`):**
    *   **AI Accelerator Market Share:** ~90%.
    *   **Manufacturing Dependency:** Exclusively relies on TSMC for wafer fabrication (4N/3nm) and CoWoS packaging. Secures HBM from SK Hynix, Micron, and Samsung.
*   **AMD (Ticker: `AMD`):**
    *   **Core Products:** Instinct MI300X/MI325X/MI350X AI accelerators, EPYC server CPUs, Ryzen client CPUs.
    *   **Manufacturing Dependency:** Relies almost entirely on TSMC for advanced logic dies (5nm/6nm chiplets for MI300, 3nm/4nm for next-gen) and CoWoS advanced packaging.
    *   **HBM Sourcing:** Multi-sources HBM from SK Hynix, Samsung, and Micron.

---

## 4. AMD's Structural Packaging & Sourcing Strategy

1.  **Chiplet Pioneer:** AMD pioneered the chiplet architecture (separating Core Complex Dies - CCDs from I/O dies). This allows AMD to use older, cheaper nodes (e.g. 6nm) for I/O and reserve expensive advanced nodes (3nm/5nm) only for compute logic.
2.  **TSMC Allocation Battle:** Because NVIDIA consumes the lion's share of TSMC's CoWoS capacity, AMD faces structural supply constraints. AMD's ability to take market share in AI accelerators is directly capped by the CoWoS allocation it can secure from TSMC.
3.  **Alternative Packaging Exploration:** AMD is actively exploring Samsung's foundry/packaging services or Intel's packaging services to diversify its supply chain and mitigate TSMC allocation risks.

---

## 5. Transmission & Lead Time Dynamics

1.  **Wafer Fab Lead Time:** Logic wafer fabrication at advanced nodes (3nm/5nm) takes **18 to 22 weeks** (4-5 months).
2.  **Advanced Packaging Lead Time:** CoWoS packaging adds another **4 to 6 weeks**.
3.  **Total Cycle:** From placing a silicon wafer order at TSMC to a finished packaged MI300X/Blackwell accelerator takes roughly **6 months**.
4.  **Forward-Looking Capital Expenditures:**
    *   Fabs require massive upfront capex (a modern 3nm fab costs ~$15-20 billion).
    *   This creates a long lead time for equipment orders: when TSMC announces a capex increase, equipment makers (ASML, AMAT, LRCX) see revenue spikes **9-12 months** before the fab begins producing wafers.
    *   Therefore, **Foundry Capex** is the earliest indicator of structural capacity expansion in the chain.
