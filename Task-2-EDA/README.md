# Task 2 — Exploratory Data Analysis (EDA)

## Objective

Perform descriptive and exploratory analysis on the cleaned dataset to identify trends, distributions, relationships, outliers, and unusual patterns.

## Deliverables

| Deliverable | Status |
|-------------|--------|
| Python/Jupyter Notebook | ✓ Complete |
| Descriptive statistics | ✓ Complete |
| Trend analysis | ✓ Complete |
| Distribution analysis | ✓ Complete |
| Relationship analysis | ✓ Complete |
| Outlier analysis | ✓ Complete |
| Business-question analysis | ✓ Complete |
| **Bonus**: Findings report | ✓ Complete |

## Files

- `eda.py` — Main EDA script
- `notebooks/eda.ipynb` — Interactive Jupyter notebook version
- `reports/findings.md` — Comprehensive findings report (markdown)
- `README.md` — This file

## Process Overview

```mermaid
graph LR
    A[Cleaned Dataset] --> B[Descriptive Statistics]
    B --> C[Distribution Analysis]
    C --> D[Trend Analysis]
    D --> E[Relationship Analysis]
    E --> F[Outlier Detection]
    F --> G[Unusual Patterns]
    G --> H[Business Questions]
    H --> I[Findings Report]
```

## Analysis Summary

### Dataset Overview
- **Records analyzed**: 9,993 orders
- **Date range**: 2016-01-01 to 2019-12-31 (4 years)
- **Categories**: 3 (Office Supplies, Furniture, Technology)
- **Regions**: 4 (West, East, Central, South)
- **Segments**: 3 (Consumer, Corporate, Home Office)

### Descriptive Statistics

| Metric | Sales | Quantity | Discount | Profit |
|--------|-------|----------|----------|--------|
| Mean | $229.85 | 3.79 | 0.16 | $28.66 |
| Median | $54.48 | 3.00 | 0.20 | $8.67 |
| Std Dev | $623.28 | 2.23 | 0.21 | $234.27 |
| Min | $0.44 | 1 | 0.00 | -$6,599.98 |
| Max | $22,638.48 | 14 | 0.80 | $8,399.98 |

### Key Findings

1. **Revenue Growth**: Sales grew from $484K (2016) to $733K (2019)
2. **Profitability Challenge**: 18.7% of orders are loss-making (1,870 orders)
3. **Category Performance**: Technology leads revenue ($836K, 36.4%), Office Supplies leads volume (60.3%)
4. **Segment Profitability**: Consumer segment highest total profit ($134K), Home Office highest per-order profit ($33.84)
5. **Regional Leader**: West region ($725K, 31.6% of total)
6. **Seasonal Peak**: November ($272K), lowest in February ($133K)
7. **Discount Impact**: High discounts (≥50%) yield negative average profit (-$105/order)

### Correlation Matrix

| | Sales | Quantity | Discount | Profit |
|---|-------|----------|----------|--------|
| **Sales** | 1.000 | 0.201 | -0.028 | **0.479** |
| **Quantity** | 0.201 | 1.000 | 0.009 | 0.066 |
| **Discount** | -0.028 | 0.009 | 1.000 | **-0.220** |
| **Profit** | **0.479** | 0.066 | **-0.220** | 1.000 |

### Outlier Detection (IQR Method)

| Variable | Low Outliers | High Outliers |
|----------|-------------|--------------|
| Sales | 0 (0.0%) | 1,167 (11.7%) |
| Quantity | 0 (0.0%) | 170 (1.7%) |
| Discount | 0 (0.0%) | 856 (8.6%) |
| Profit | 604 (6.0%) | 1,277 (12.8%) |

### Business Questions Answered

| Question | Answer |
|----------|--------|
| What category generates the most revenue? | **Technology** ($836K, 36.4%) |
| Which customer segment is most profitable? | **Consumer** ($134K total) |
| Which region has the highest sales? | **West** ($725K) |
| What is overall profitability? | Revenue $2.3M, Profit $286K, Margin 12.47% |
| How does discount affect profitability? | High discounts (≥50%) = negative profit (-$105/order) |
| Which shipping mode dominates? | **Standard Class** ($1.36M) |
| Seasonal trends? | Peak: **November** ($272K), Low: **February** ($133K) |

## How to Run

```bash
# Using Python script
python eda.py

# Using Jupyter notebook
jupyter notebook notebooks/eda.ipynb
```

---

*Task completed: September 2026*