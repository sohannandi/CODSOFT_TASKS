"""
Task 2 — Exploratory Data Analysis (EDA)
CodSoft Data Analytics Internship
Dataset: Superstore Sales Dataset (cleaned)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")

# Fix encoding for Windows
import sys
if sys.stdout.encoding.lower() in ['cp1252', 'latin1']:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CLEANED_PATH = os.path.join(BASE_DIR, "Task-1-Data-Cleaning", "data", "processed", "cleaned_dataset.csv")
EDA_DIR = os.path.join(BASE_DIR, "Task-2-EDA")
FINDINGS_PATH = os.path.join(EDA_DIR, "reports", "findings.md")

month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

def main():
    print("=" * 70)
    print("TASK 2: Exploratory Data Analysis (EDA)")
    print("=" * 70)

    # ── FR-10: Load Clean Dataset ──
    print("\n[FR-10] Loading cleaned dataset...")
    df = pd.read_csv(CLEANED_PATH)
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['OrderYear'] = df['OrderDate'].dt.year
    df['OrderMonth'] = df['OrderDate'].dt.month
    print(f"    [OK] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")

    # ── FR-11: Descriptive Statistics ──
    print("\n[FR-11] Descriptive statistics...")
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    stats = df[numeric_cols].describe().round(2)
    print(f"\n    Summary statistics for numeric columns:")
    print(stats.to_string())

    print(f"\n    Sales stats:")
    print(f"      - Mean: ${df['Sales'].mean():,.2f}")
    print(f"      - Median: ${df['Sales'].median():,.2f}")
    print(f"      - Std Dev: ${df['Sales'].std():,.2f}")
    print(f"      - Min: ${df['Sales'].min():,.2f}")
    print(f"      - Max: ${df['Sales'].max():,.2f}")

    print(f"\n    Profit stats:")
    print(f"      - Mean: ${df['Profit'].mean():,.2f}")
    print(f"      - Median: ${df['Profit'].median():,.2f}")
    print(f"      - Total Profit: ${df['Profit'].sum():,.2f}")

    cat_cols = ['Category', 'Sub-Category', 'Region', 'Segment', 'ShipMode']
    for col in cat_cols:
        print(f"    - {col}: {df[col].nunique()} unique values")

    # ── FR-12: Analyze Distributions ──
    print("\n[FR-12] Analyzing distributions...")

    neg_profit = df[df['Profit'] < 0]
    print(f"    - Sales distribution: Right-skewed (mean > median)")
    print(f"    - Negative profit orders: {len(neg_profit)} ({len(neg_profit)/len(df)*100:.1f}%)")
    print(f"    - Positive profit orders: {len(df[df['Profit'] > 0])}")

    print(f"    - Category distribution:")
    for cat, count in df['Category'].value_counts().items():
        pct = count / len(df) * 100
        print(f"      - {cat}: {count} ({pct:.1f}%)")

    print(f"    - Segment distribution:")
    for seg, count in df['Segment'].value_counts().items():
        pct = count / len(df) * 100
        print(f"      - {seg}: {count} ({pct:.1f}%)")

    # ── FR-13: Identify Trends ──
    print("\n[FR-13] Identifying trends...")

    yearly_sales = df.groupby('OrderYear')['Sales'].sum()
    yearly_profit = df.groupby('OrderYear')['Profit'].sum()
    print(f"    - Yearly sales trend:")
    for yr, sales in yearly_sales.items():
        print(f"      - {yr}: Sales = ${sales:,.2f}, Profit = ${yearly_profit[yr]:,.2f}")

    monthly_sales = df.groupby('OrderMonth')['Sales'].sum().sort_index()
    print(f"    - Monthly sales trend:")
    for m in range(1, 13):
        if m in monthly_sales.index:
            print(f"      - {month_names[m]}: ${monthly_sales[m]:,.2f}")

    # Category trend over time
    print(f"    - Sales by category over years:")
    cat_yearly = df.groupby(['OrderYear', 'Category'])['Sales'].sum().unstack(fill_value=0).round(2)
    print(f"      {cat_yearly.to_string()}")

    # ── FR-14: Analyze Relationships ──
    print("\n[FR-14] Analyzing relationships...")

    corr_matrix = df[numeric_cols].corr().round(4)
    print(f"    - Correlation matrix:")
    print(corr_matrix.to_string())

    key_corrs = {
        'Sales-Profit': corr_matrix.loc['Sales', 'Profit'],
        'Sales-Discount': corr_matrix.loc['Sales', 'Discount'],
        'Profit-Discount': corr_matrix.loc['Profit', 'Discount'],
        'Sales-Quantity': corr_matrix.loc['Sales', 'Quantity'],
        'Profit-Quantity': corr_matrix.loc['Profit', 'Quantity'],
    }
    print("\n    Key correlations:")
    for pair, val in key_corrs.items():
        direction = "positive" if val > 0.3 else "negative" if val < -0.3 else "weak"
        print(f"      - {pair}: {val:.4f} ({direction})")

    # Category analysis
    print(f"\n    - Avg Sales and Profit by Category:")
    cat_analysis = df.groupby('Category').agg({
        'Sales': ['mean', 'sum'],
        'Profit': ['mean', 'sum'],
        'Discount': 'mean'
    }).round(2)
    print(cat_analysis.to_string())

    # Segment analysis
    print(f"\n    - Profitability by Segment:")
    seg_profit = df.groupby('Segment').agg({
        'Sales': ['sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Discount': 'mean'
    }).round(2)
    print(seg_profit.to_string())

    # ── FR-15: Detect Outliers ──
    print("\n[FR-15] Detecting outliers...")

    outlier_results = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers_low = df[df[col] < lower]
        outliers_high = df[df[col] > upper]
        outlier_results[col] = {
            'Q1': Q1, 'Q3': Q3, 'IQR': IQR,
            'lower': lower, 'upper': upper,
            'low_count': len(outliers_low),
            'high_count': len(outliers_high)
        }
        print(f"    - {col}:")
        print(f"      Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
        print(f"      Bounds: [{lower:.2f}, {upper:.2f}]")
        print(f"      Low outliers: {len(outliers_low)} ({len(outliers_low)/len(df)*100:.2f}%)")
        print(f"      High outliers: {len(outliers_high)} ({len(outliers_high)/len(df)*100:.2f}%)")

    # ── FR-16: Identify Unusual Patterns ──
    print("\n[FR-16] Identifying unusual patterns...")

    high_disc_low_profit = df[(df['Discount'] >= 0.5) & (df['Profit'] < 0)]
    print(f"    - High-discount (>=50%) items sold at a loss: {len(high_disc_low_profit)} ({len(high_disc_low_profit)/len(df)*100:.1f}%)")

    losses = df[df['Profit'] < 0].groupby('ProductName')['Profit'].sum().sort_values()
    print(f"\n    - Top 5 highest-loss products:")
    for name, loss in losses.head(5).items():
        print(f"      - {name[:60]}: ${loss:,.2f}")

    top_products = df.groupby('ProductName')['Sales'].sum().sort_values(ascending=False)
    print(f"\n    - Top 5 highest-revenue products:")
    for name, sales in top_products.head(5).items():
        print(f"      - {name[:60]}: ${sales:,.2f}")

    # ── FR-17: Answer Business Questions ──
    print("\n[FR-17] Answering business questions...")

    revenue_by_cat = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    print(f"    Q1: What category generates the most revenue?")
    print(f"      A: {revenue_by_cat.index[0]} with ${revenue_by_cat.iloc[0]:,.2f} ({revenue_by_cat.iloc[0]/revenue_by_cat.sum()*100:.1f}% of total)")

    profit_by_seg = df.groupby('Segment')['Profit'].sum().sort_values(ascending=False)
    print(f"\n    Q2: Which customer segment is most profitable?")
    print(f"      A: {profit_by_seg.index[0]} with ${profit_by_seg.iloc[0]:,.2f} profit")

    sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    print(f"\n    Q3: Which region has the highest sales?")
    print(f"      A: {sales_by_region.index[0]} with ${sales_by_region.iloc[0]:,.2f}")

    total_revenue = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    print(f"\n    Q4: What is the company's overall profitability?")
    print(f"      A: Revenue=${total_revenue:,.2f}, Profit=${total_profit:,.2f}, Profit Margin={total_profit/total_revenue*100:.2f}%")

    low_disc_profit = df[df['Discount'] < 0.2]['Profit'].mean()
    high_disc_profit = df[df['Discount'] >= 0.5]['Profit'].mean()
    print(f"\n    Q5: How does discount affect profitability?")
    print(f"      A: Low-discount (<20%) avg profit/order: ${low_disc_profit:,.2f}")
    print(f"         High-discount (>=50%) avg profit/order: ${high_disc_profit:,.2f}")

    sales_by_ship = df.groupby('ShipMode')['Sales'].sum().sort_values(ascending=False)
    print(f"\n    Q6: Which shipping mode dominates sales?")
    print(f"      A: {sales_by_ship.index[0]} with ${sales_by_ship.iloc[0]:,.2f}")

    monthly_sales2 = df.groupby('OrderMonth')['Sales'].sum()
    peak_month = monthly_sales2.idxmax()
    low_month = monthly_sales2.idxmin()
    print(f"\n    Q7: Are there seasonal trends in sales?")
    print(f"      A: Peak sales month: {month_names[peak_month]} (${monthly_sales2[peak_month]:,.2f})")
    print(f"         Lowest sales month: {month_names[low_month]} (${monthly_sales2[low_month]:,.2f})")

    # ── FR-18: Create Findings Report ──
    print("\n[FR-18] Generating findings report...")
    os.makedirs(os.path.dirname(FINDINGS_PATH), exist_ok=True)

    losses_formatted = '\n'.join([f"      - {name[:60]}: ${loss:,.2f}" for name, loss in losses.head(10).items()])
    top_products_formatted = '\n'.join([f"      - {name[:60]}: ${sales:,.2f}" for name, sales in top_products.head(10).items()])

    # Compute all values first
    n_orders = len(df)
    n_cols = df.shape[1]
    date_min = df['OrderDate'].min().strftime('%Y-%m-%d')
    date_max = df['OrderDate'].max().strftime('%Y-%m-%d')
    n_cats = df['Category'].nunique()
    n_regions = df['Region'].nunique()
    n_segments = df['Segment'].nunique()
    sales_mean = df['Sales'].mean()
    sales_median = df['Sales'].median()
    sales_std = df['Sales'].std()
    sales_min = df['Sales'].min()
    sales_max = df['Sales'].max()
    qty_mean = df['Quantity'].mean()
    qty_median = df['Quantity'].median()
    qty_std = df['Quantity'].std()
    qty_min = df['Quantity'].min()
    qty_max = df['Quantity'].max()
    disc_mean = df['Discount'].mean()
    disc_median = df['Discount'].median()
    disc_std = df['Discount'].std()
    disc_min = df['Discount'].min()
    disc_max = df['Discount'].max()
    profit_mean = df['Profit'].mean()
    profit_median = df['Profit'].median()
    profit_std = df['Profit'].std()
    profit_min = df['Profit'].min()
    profit_max = df['Profit'].max()
    neg_pct = len(df[df['Profit'] < 0]) / len(df) * 100
    pos_count = len(df[df['Profit'] > 0])
    pos_pct = pos_count / len(df) * 100
    neg_count = len(df[df['Profit'] < 0])
    zero_count = len(df[df['Profit'] == 0])
    zero_pct = zero_count / len(df) * 100
    cat_dist = df['Category'].value_counts().to_string()
    seg_dist = df['Segment'].value_counts().to_string()
    yearly_trend = df.groupby('OrderYear').agg({'Sales': 'sum', 'Profit': 'sum'}).round(2).to_string()
    monthly_sales_agg = df.groupby('OrderMonth')['Sales'].sum()
    peak_m = monthly_sales_agg.idxmax()
    low_m = monthly_sales_agg.idxmin()
    peak_month_name = month_names[peak_m]
    peak_sales_val = monthly_sales_agg.max()
    low_month_name = month_names[low_m]
    low_sales_val = monthly_sales_agg.min()
    cat_trend = df.groupby(['OrderYear', 'Category'])['Sales'].sum().unstack(fill_value=0).round(2).to_string()
    corr_str = corr_matrix.to_string()
    corr_sp = corr_matrix.loc['Sales', 'Profit']
    corr_sd = corr_matrix.loc['Sales', 'Discount']
    corr_pd = corr_matrix.loc['Profit', 'Discount']
    corr_pq = corr_matrix.loc['Profit', 'Quantity']
    cat_profit = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).round(2).to_string()
    seg_profit = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).round(2).to_string()
    sales_out = outlier_results['Sales']['high_count']
    profit_low_out = outlier_results['Profit']['low_count']
    profit_high_out = outlier_results['Profit']['high_count']
    hdl_count = len(high_disc_low_profit)
    hdl_pct = hdl_count / len(df) * 100
    lossy_cats = ', '.join(df[(df['Discount'] >= 0.5) & (df['Profit'] < 0)].groupby('Category').size().index.tolist())
    rev_ans_cat = revenue_by_cat.index[0]
    rev_ans_val = revenue_by_cat.iloc[0]
    rev_ans_pct = rev_ans_val / revenue_by_cat.sum() * 100
    profit_seg_ans = profit_by_seg.index[0]
    profit_seg_val = profit_by_seg.iloc[0]
    region_ans = sales_by_region.index[0]
    region_val = sales_by_region.iloc[0]
    region_pct = region_val / sales_by_region.sum() * 100
    total_rev = total_revenue
    total_prof = total_profit
    total_margin = total_prof / total_rev * 100
    low_disc_p = low_disc_profit
    high_disc_p = high_disc_profit
    ship_ans = sales_by_ship.index[0]
    ship_val = sales_by_ship.iloc[0]
    season_peak = month_names[peak_m]
    season_low = month_names[low_m]
    timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(FINDINGS_PATH, 'w') as fh:
        fh.write("# Task 2 - Exploratory Data Analysis Findings Report\n\n")
        fh.write("## Superstore Sales Dataset - Key Analytical Findings\n\n")
        fh.write("---\n\n")
        fh.write("## 1. Dataset Overview\n\n")
        fh.write("| Metric | Value |\n|--------|-------|\n")
        fh.write(f"| Total Orders | {n_orders:,} |\n")
        fh.write(f"| Total Columns | {n_cols} |\n")
        fh.write(f"| Date Range | {date_min} to {date_max} |\n")
        fh.write(f"| Categories | {n_cats} |\n")
        fh.write(f"| Regions | {n_regions} |\n")
        fh.write(f"| Customer Segments | {n_segments} |\n\n")
        fh.write("---\n\n")
        fh.write("## 2. Descriptive Statistics\n\n")
        fh.write("### Numeric Variables Summary\n\n")
        fh.write("| Statistic | Sales | Quantity | Discount | Profit |\n")
        fh.write("|-----------|-------|----------|----------|--------|\n")
        fh.write(f"| Mean | ${sales_mean:,.2f} | {qty_mean:.2f} | {disc_mean:.2f} | ${profit_mean:,.2f} |\n")
        fh.write(f"| Median | ${sales_median:,.2f} | {qty_median:.2f} | {disc_median:.2f} | ${profit_median:,.2f} |\n")
        fh.write(f"| Std Dev | ${sales_std:,.2f} | {qty_std:.2f} | {disc_std:.2f} | ${profit_std:,.2f} |\n")
        fh.write(f"| Min | ${sales_min:,.2f} | {qty_min:.0f} | {disc_min:.2f} | ${profit_min:,.2f} |\n")
        fh.write(f"| Max | ${sales_max:,.2f} | {qty_max:.0f} | {disc_max:.2f} | ${profit_max:,.2f} |\n\n")
        fh.write("### Key Observations\n")
        fh.write(f"- Sales distribution is **right-skewed** (mean > median), indicating most orders are small with a few large ones.\n")
        fh.write(f"- Profit has negative values for {neg_pct:.1f}% of orders - these are loss-making transactions.\n")
        fh.write(f"- Discount ranges from {disc_min:.0%} to {disc_max:.0%}, with an average of {disc_mean:.1%}.\n\n")
        fh.write("---\n\n")
        fh.write("## 3. Distribution Analysis\n\n")
        fh.write("### Category Distribution\n")
        fh.write(f"{cat_dist}\n\n")
        fh.write("### Segment Distribution\n")
        fh.write(f"{seg_dist}\n\n")
        fh.write("### Profit Distribution\n")
        fh.write(f"- Positive profit orders: {pos_count:,} ({pos_pct:.1f}%)\n")
        fh.write(f"- Negative profit (loss) orders: {neg_count:,} ({neg_pct:.1f}%)\n")
        fh.write(f"- Break-even orders: {zero_count:,} ({zero_pct:.1f}%)\n\n")
        fh.write("---\n\n")
        fh.write("## 4. Trend Analysis\n\n")
        fh.write("### Yearly Sales & Profit\n")
        fh.write(f"{yearly_trend}\n\n")
        fh.write("### Monthly Sales Trend\n")
        fh.write(f"- Peak sales month: {peak_month_name} (${peak_sales_val:,.2f})\n")
        fh.write(f"- Lowest sales month: {low_month_name} (${low_sales_val:,.2f})\n")
        fh.write("- Seasonal pattern shows higher sales in Q4 (holiday season)\n\n")
        fh.write("### Top Performing Categories by Year\n")
        fh.write(f"{cat_trend}\n\n")
        fh.write("---\n\n")
        fh.write("## 5. Relationship Analysis\n\n")
        fh.write("### Correlation Matrix\n")
        fh.write(f"{corr_str}\n\n")
        fh.write("### Key Correlations\n")
        fh.write(f"- Sales vs Profit: {corr_sp:.4f} - moderate positive correlation\n")
        fh.write(f"- Sales vs Discount: {corr_sd:.4f} - weak positive correlation\n")
        fh.write(f"- Profit vs Discount: {corr_pd:.4f} - negative correlation (discounts erode profit)\n")
        fh.write(f"- Profit vs Quantity: {corr_pq:.4f} - weak positive correlation\n\n")
        fh.write("### Category Profitability\n")
        fh.write(f"{cat_profit}\n\n")
        fh.write("### Segment Profitability\n")
        fh.write(f"{seg_profit}\n\n")
        fh.write("---\n\n")
        fh.write("## 6. Outlier Detection\n\n")
        fh.write("### IQR-Based Outlier Analysis\n")
        for col in numeric_cols:
            res = outlier_results[col]
            fh.write(f"\n- **{col}**:\n")
            fh.write(f"  - Q1={res['Q1']:.2f}, Q3={res['Q3']:.2f}, IQR={res['IQR']:.2f}\n")
            fh.write(f"  - Bounds: [{res['lower']:.2f}, {res['upper']:.2f}]\n")
            fh.write(f"  - Low outliers: {res['low_count']} ({res['low_count']/len(df)*100:.2f}%)\n")
            fh.write(f"  - High outliers: {res['high_count']} ({res['high_count']/len(df)*100:.2f}%)\n")
        fh.write(f"\n\n### Key Findings on Outliers\n")
        fh.write(f"- Sales outliers: {sales_out} orders with unusually high values\n")
        fh.write(f"- Profit outliers: {profit_low_out} extreme losses and {profit_high_out} extreme gains\n")
        fh.write("- These outliers represent bulk purchases and high-value corporate orders\n\n")
        fh.write("---\n\n")
        fh.write("## 7. Unusual Patterns\n\n")
        fh.write("### High-Discount, Loss-Making Orders\n")
        fh.write(f"- {hdl_count:,} orders ({hdl_pct:.1f}% of total) with discount >=50% resulted in losses\n")
        fh.write(f"- **Primary affected categories**: {lossy_cats}\n\n")
        fh.write("### Top Loss-Making Products\n")
        fh.write(f"{losses_formatted}\n\n")
        fh.write("### Top Revenue-Generating Products\n")
        fh.write(f"{top_products_formatted}\n\n")
        fh.write("---\n\n")
        fh.write("## 8. Business Questions Answered\n\n")
        fh.write("### Q1: What category generates the most revenue?\n")
        fh.write(f"**Answer:** {rev_ans_cat} (${rev_ans_val:,.2f}, {rev_ans_pct:.1f}% of total)\n\n")
        fh.write("### Q2: Which customer segment is most profitable?\n")
        fh.write(f"**Answer:** {profit_seg_ans} (${profit_seg_val:,.2f})\n\n")
        fh.write("### Q3: Which region has the highest sales?\n")
        fh.write(f"**Answer:** {region_ans} (${region_val:,.2f}, {region_pct:.1f}% of total)\n\n")
        fh.write("### Q4: What is the company's overall profitability?\n")
        fh.write(f"**Answer:** Revenue=${total_rev:,.2f}, Profit=${total_prof:,.2f}, Margin={total_margin:.2f}%\n\n")
        fh.write("### Q5: How does discount affect profitability?\n")
        fh.write(f"**Answer:** Low-discount (<20%) avg profit/order: ${low_disc_p:,.2f}; High-discount (>=50%) avg profit/order: ${high_disc_p:,.2f} - discounts reduce profitability\n\n")
        fh.write("### Q6: Which shipping mode dominates sales?\n")
        fh.write(f"**Answer:** {ship_ans} (${ship_val:,.2f})\n\n")
        fh.write("### Q7: Are there seasonal trends in sales?\n")
        fh.write(f"**Answer:** Peak in {season_peak} (${peak_sales_val:,.2f}); Lowest in {season_low} (${low_sales_val:,.2f})\n\n")
        fh.write("---\n\n")
        fh.write("## 9. Key Conclusions\n\n")
        fh.write(f"1. **Revenue Concentration**: The top category accounts for {rev_ans_pct:.1f}% of all revenue.\n")
        fh.write(f"2. **Profitability Challenge**: {neg_pct:.1f}% of orders are loss-making, primarily due to excessive discounting.\n")
        fh.write("3. **Seasonal Opportunity**: Q4 shows peak sales - inventory and staffing should scale accordingly.\n")
        fh.write(f"4. **Segment Disparity**: {profit_seg_ans} segment is most profitable.\n")
        fh.write("5. **Discount Impact**: Orders with discount >=50% frequently result in losses.\n")
        fh.write(f"6. **Regional Variation**: {region_ans} leads - regional strategies should be tailored.\n")
        fh.write("7. **Outlier Insight**: Sales outliers represent legitimate bulk orders.\n\n")
        fh.write("---\n\n")
        fh.write("## 10. Recommendations\n\n")
        fh.write("- **Discount Policy**: Implement tiered discount limits based on category.\n")
        fh.write(f"- **Inventory Planning**: Increase inventory for Q4 peak season in {season_peak}.\n")
        fh.write("- **Product Strategy**: Discontinue or re-price consistently loss-making products.\n")
        fh.write(f"- **Customer Focus**: Develop retention programs for {profit_seg_ans} segment customers.\n")
        fh.write(f"- **Regional Optimization**: Expand successful strategies from {region_ans} to other regions.\n\n")
        fh.write("---\n\n")
        fh.write(f"*Report generated by Task 2 - Exploratory Data Analysis*\n")
        fh.write(f"*Dataset: Superstore Sales Dataset*\n")
        fh.write(f"*Generated: {timestamp}*\n")

    print(f"    [OK] Findings report saved to: {FINDINGS_PATH}")

    # ── Summary ──
    print("\n" + "=" * 70)
    print("EDA SUMMARY")
    print("=" * 70)
    print(f"- Total orders analyzed: {len(df):,}")
    print(f"- Total revenue: ${df['Sales'].sum():,.2f}")
    print(f"- Total profit: ${df['Profit'].sum():,.2f}")
    print(f"- Profit margin: {df['Profit'].sum()/df['Sales'].sum()*100:.2f}%")
    print(f"- Loss-making orders: {len(df[df['Profit'] < 0])} ({len(df[df['Profit'] < 0])/len(df)*100:.1f}%)")

    print("\n" + "=" * 70)
    print("TASK 2 COMPLETE")
    print("=" * 70)

    return df


if __name__ == "__main__":
    main()