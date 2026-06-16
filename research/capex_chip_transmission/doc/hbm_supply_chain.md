# Memory & HBM Supply Chain Map

This document maps the High Bandwidth Memory (HBM) supply chain, identifying key manufacturers, upstream equipment/materials suppliers, and their transmission dynamics.

---

## 1. Key HBM Manufacturers
HBM stacks DRAM chips vertically using TSVs (Through-Silicon Vias), achieving high bandwidth for AI accelerators.

*   **SK Hynix (Korea):**
    *   **Market Share (2024E):** ~52% (TrendForce data).
    *   **Role:** Pioneer in HBM; primary supplier of HBM3/HBM3E to NVIDIA (H100, H200, Blackwell).
    *   **Packaging Tech:** MR-MUF (Mass Reflow Molded Underfill).
*   **Samsung Electronics (Korea):**
    *   **Market Share (2024E):** ~42%.
    *   **Role:** Major volume supplier; supplying both HBM3 and working on Blackwell qualifications.
    *   **Packaging Tech:** TC-NCF (Thermal Compression Non-Conductive Film).
*   **Micron Technology (US - Ticker: `MU`):**
    *   **Market Share (2024E):** ~5-6%.
    *   **Role:** Ramping up HBM3E production for NVIDIA H200/Blackwell; high-efficiency design (24GB/36GB stacks).
    *   **Packaging Tech:** TC-NCF/MR-MUF hybrid.

---

## 2. Upstream Advanced Packaging & Bonding Equipment
Vertical stacking of DRAM dies requires ultra-precise bonding equipment.

*   **Hanmi Semiconductor (Korea - Ticker: `042700.KS`):**
    *   **Role:** Monopolizes the supply of **Dual TC Bonders** (Thermal Compression Bonders) to SK Hynix and Micron for HBM3E.
*   **ASMPT (Hong Kong - Ticker: `0522.HK`):**
    *   **Role:** Key supplier of TC Bonders and hybrid bonding equipment (for next-gen HBM4).
*   **Shibaura Mechatronics / Toray (Japan):**
    *   **Role:** Specialized bonding and washing equipment for memory stacking.

---

## 3. Upstream TSV & Wafer Processing Equipment
Creating vertical vias (TSVs) requires deep silicon etching and metal deposition.

*   **Lam Research (US - Ticker: `LRCX`):**
    *   **Role:** Dominates deep silicon etching (via-middle process) for TSV creation.
*   **Applied Materials (US - Ticker: `AMAT`):**
    *   **Role:** Leader in TSV barrier/seed layer deposition (PVD/CVD).
*   **Tokyo Electron (Japan - Ticker: `TOELY`):**
    *   **Role:** Coating/developing, wafer cleaning, and TSV etching equipment.

---

## 4. Advanced Testing Equipment
HBM requires rigorous testing of individual dies (KGD - Known Good Die) and final stacks due to high thermal/mechanical risk.

*   **Advantest (Japan - Ticker: `ATEYY` / `6857.T`):**
    *   **Role:** Dominates the HBM testing market (V93000 SoC and T5800 memory test systems) for Samsung, SK Hynix, and Micron.
*   **Teradyne (US - Ticker: `TER`):**
    *   **Role:** Provides memory test systems competing with Advantest.

---

## 5. Specialty Materials
*   **Resonac (formerly Showa Denko, Japan):**
    *   **Role:** Market leader in thermal Epoxy Molding Compound (EMC) and underfills for advanced packaging.
*   **Namics (Japan):**
    *   **Role:** Key supplier of underfill materials used in SK Hynix's MR-MUF packaging.

---

## 6. Transmission & Lag Implications
1.  **Lead Times:** Memory/HBM has longer lead times (typically 6-9 months) compared to standard DRAM, making it highly sensitive to double-ordering and supply shocks.
2.  **Transmission Sequence:**
    $$\text{Hyperscaler Capex} \rightarrow \text{AI Accelerator Orders (NVIDIA)} \rightarrow \text{HBM Orders (SK Hynix, Micron)} \rightarrow \text{Packaging/Testing Equipment (Hanmi, Advantest)}$$
3.  **Cyclicality:** HBM capacity is booked out 12-18 months in advance, meaning equipment suppliers (Hanmi, Advantest) see their revenue cycles spike ahead of actual memory shipments, showing a front-running characteristic relative to generic memory cycles.
