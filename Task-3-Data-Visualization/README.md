# Task 3 — Data Visualization Dashboard

## Objective

Create meaningful data visualizations using Matplotlib, Seaborn, and Plotly to present analytical findings through clear and understandable charts.

## Deliverables

| Deliverable | Status |
|-------------|--------|
| Python/Jupyter Notebook | ✓ Complete |
| Bar chart | ✓ Complete |
| Line chart | ✓ Complete |
| Pie chart | ✓ Complete |
| Histogram | ✓ Complete |
| Scatter plot | ✓ Complete |
| Proper chart titles and labels | ✓ Complete |
| Legends where necessary | ✓ Complete |
| Clear presentation of insights | ✓ Complete |
| **Bonus**: Interactive Plotly dashboards | ✓ Complete |
| **Bonus**: Box plot, Stacked bar, Heatmap | ✓ Complete |

## Files

- `visualization.py` — Main visualization script
- `notebooks/visualization.ipynb` — Interactive Jupyter notebook version
- `visualizations/` — All chart output files:
  - `bar_chart.png` — Total sales by product category
  - `line_chart.png` — Monthly sales trend (2016-2019)
  - `pie_chart.png` — Sales composition by category
  - `histogram.png` — Distribution of sales values
  - `scatter_plot.png` — Sales vs Profit (colored by discount)
  - `box_plot.png` — Profit distribution by category
  - `stacked_bar.png` — Yearly sales by category
  - `correlation_heatmap.png` — Correlation matrix heatmap
  - `interactive_sales_by_category.html` — Interactive Plotly bar chart
  - `interactive_monthly_sales.html` — Interactive Plotly line chart
  - `interactive_profit_by_category.html` — Interactive Plotly pie chart
  - `interactive_sales_vs_profit.html` — Interactive Plotly scatter plot
  - `interactive_sales_distribution.html` — Interactive Plotly histogram
- `README.md` — This file

## Chart List

### Required Visualizations

| Chart | File | Description |
|-------|------|-------------|
| **Bar Chart** | `bar_chart.png` | Compares total sales across categories (Office Supplies, Furniture, Technology) |
| **Line Chart** | `line_chart.png` | Shows monthly sales trend from 2016-2019, revealing seasonal patterns |
| **Pie Chart** | `pie_chart.png` | Displays sales composition: Office Supplies (50.7%), Furniture (23.1%), Technology (26.2%) |
| **Histogram** | `histogram.png` | Shows distribution of sales values with mean and median markers |
| **Scatter Plot** | `scatter_plot.png` | Examines Sales vs Profit relationship, colored by discount rate |

### Bonus Visualizations

| Chart | File | Description |
|-------|------|-------------|
| **Box Plot** | `box_plot.png` | Profit distribution by category showing outliers |
| **Stacked Bar** | `stacked_bar.png` | Yearly sales breakdown by category |
| **Heatmap** | `correlation_heatmap.png` | Correlation matrix for Sales, Quantity, Discount, Profit |

### Interactive Dashboards

All interactive Plotly charts include hover details, zoom, pan, and export features.

## Insights from Visualizations

1. **Sales Distribution**: Most orders are small-value; a few large orders dominate total revenue
2. **Category Leader**: Technology generates the most revenue despite lower volume
3. **Seasonal Pattern**: Clear Q4 peak (Nov-Dec) in sales — holiday season effect
4. **Profit-Outlier Relationship**: High discount orders cluster in the negative profit zone
5. **Category Profitability**: Technology has highest profit ($145K), followed by Furniture ($18K)
6. **Outlier Concentration**: High-value orders are spread across categories but concentrate in Technology

## How to Run

```bash
# Using Python script
python visualization.py

# Using Jupyter notebook
jupyter notebook notebooks/visualization.ipynb
```

Outputs include:
- 8 static PNG charts saved to `visualizations/`
- 5 interactive HTML dashboards saved to `visualizations/`

---

*Task completed: September 2026*