# CodSoft Data Analytics Internship — Tasks 1, 2 & 3

## Project Overview

This repository contains the three completed Data Analytics internship tasks:

### Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| **Task 1** | Data Cleaning & Preprocessing | ✓ Complete |
| **Task 2** | Exploratory Data Analysis (EDA) | ✓ Complete |
| **Task 3** | Data Visualization Dashboard | ✓ Complete |

## Technology Stack

- **Python** 3.x
- **Pandas** — data loading, cleaning, manipulation, and analysis
- **NumPy** — numerical operations
- **Matplotlib** — static visualizations
- **Seaborn** — statistical visualizations
- **Plotly** — interactive visualizations
- **Jupyter Notebook** — interactive development environment

## Dataset

This project uses the **Superstore Sales Dataset**, a publicly available dataset containing retail sales data. 

- **Dataset name:** Superstore Sales Dataset
- **Source:** Kaggle / GitHub (raw GitHub URL used for download)
- **Purpose:** Retail sales analysis across multiple categories, regions, and time periods
- **Main columns:** OrderID, OrderDate, ShipDate, ShipMode, CustomerID, CustomerName, Segment, Country, City, State, Postal Code, Region, ProductID, Category, Sub-Category, ProductName, Sales, Quantity, Discount, Profit
- **Rows:** 9,993 records (after cleaning)
- **File format:** CSV

## Results

### Task 1 — Data Cleaning & Preprocessing
- Imported and inspected 9,994-row raw dataset
- Identified and removed 1 duplicate record (2 rows marking, 1 to keep)
- Identified 11 missing values in "Postal Code" column
- Filled missing Postal Code values with the mode
- Converted OrderDate and ShipDate from strings to datetime64
- Converted Postal Code to nullable Int64 type
- Verified OrderYear consistency with parsed dates
- Exported cleaned dataset: `cleaned_dataset.csv` (9,993 rows)
- Generated missing data comparison visualization

### Task 2 — Exploratory Data Analysis
- Calculated descriptive statistics for Sales, Quantity, Discount, and Profit
- Analyzed distributions across 3 product categories, 3 customer segments, and 4 regions
- Identified trends: Year-over-year growth from $484K (2016) to $733K (2019)
- Found strong Sales-Profit correlation (0.479), negative Profit-Discount correlation (-0.220)
- Detected 1,167 high-sales outliers and 1,277 extreme profit outliers
- Identified 1,870 loss-making orders (18.7%), primarily due to high discounting
- Answered 7 key business questions:
  - Top revenue category: **Technology** ($836K, 36.4% of total)
  - Most profitable segment: **Consumer** ($134K)
  - Highest sales region: **West** ($725K)
  - Overall profit margin: **12.47%**
  - Discounts ≥50% result in negative average profit (-$105/order)
- Generated comprehensive findings report (markdown)

### Task 3 — Data Visualization Dashboard
- Created 5 static charts (Matplotlib/Seaborn):
  1. **Bar chart** — Total sales by category
  2. **Line chart** — Monthly sales trend
  3. **Pie chart** — Sales composition by category
  4. **Histogram** — Distribution of sales values
  5. **Scatter plot** — Sales vs Profit (colored by discount)
- Created 3 bonus charts:
  - Box plot: Profit by category
  - Stacked bar: Yearly sales by category
  - Heatmap: Correlation matrix
- Created 5 interactive HTML dashboards using Plotly
- All charts include: descriptive titles, axis labels, legends, readable color schemes

## Repository Structure

```
CODSOFT_TASKSNO/
├── README.md
├── requirements.txt
├── Task-1-Data-Cleaning/
│   ├── data/
│   │   ├── raw/
│   │   │   └── superstore.csv (raw original dataset)
│   │   └── processed/
│   │       └── cleaned_dataset.csv (cleaned output)
│   ├── notebooks/
│   │   └── data_cleaning.ipynb (generated)
│   ├── visuals/
│   │   └── missing_data_comparison.png
│   └── README.md
│
├── Task-2-EDA/
│   ├── data/
│   ├── notebooks/
│   │   └── eda.ipynb (generated)
│   ├── reports/
│   │   └── findings.md (EDA findings report)
│   └── README.md
│
├── Task-3-Data-Visualization/
│   ├── data/
│   ├── notebooks/
│   │   └── visualization.ipynb (generated)
│   ├── visualizations/
│   │   ├── bar_chart.png
│   │   ├── line_chart.png
│   │   ├── pie_chart.png
│   │   ├── histogram.png
│   │   ├── scatter_plot.png
│   │   ├── box_plot.png
│   │   ├── stacked_bar.png
│   │   └── correlation_heatmap.png
│   ├── interactive_dashboards/
│   │   ├── interactive_sales_by_category.html
│   │   ├── interactive_monthly_sales.html
│   │   ├── interactive_profit_by_category.html
│   │   ├── interactive_sales_vs_profit.html
│   │   └── interactive_sales_distribution.html
│   └── README.md
│
└── requirements.txt
```

