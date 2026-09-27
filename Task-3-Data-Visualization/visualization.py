"""
Task 3 — Data Visualization Dashboard
CodSoft Data Analytics Internship
Dataset: Superstore Sales Dataset (cleaned)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
VIZ_DIR = os.path.join(BASE_DIR, "Task-3-Data-Visualization", "visualizations")
REPORT_DIR = os.path.join(BASE_DIR, "Task-2-EDA", "reports")

# Color palette
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4']
sns.set_palette(sns.color_palette(COLORS))

def main():
    print("=" * 70)
    print("TASK 3: Data Visualization Dashboard")
    print("=" * 70)

    # ── FR-19: Prepare Visualization Dataset ──
    print("\n[FR-19] Loading cleaned dataset...")
    df = pd.read_csv(CLEANED_PATH)
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['OrderYear'] = df['OrderDate'].dt.year
    df['OrderMonth'] = df['OrderDate'].dt.month
    df['OrderMonthName'] = df['OrderDate'].dt.strftime('%B')
    print(f"    [OK] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")

    # Monthly sales for line chart
    monthly_sales3 = df.groupby(df['OrderDate'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_sales3.columns = ['Period', 'Sales']
    monthly_sales3['Period'] = monthly_sales3['Period'].astype(str)

    os.makedirs(VIZ_DIR, exist_ok=True)

    # ═══════════════════════════════════════════════════════════
    # Chart 1: BAR CHART - Sales by Category
    # ═══════════════════════════════════════════════════════════
    print("\n[Chart 1] Creating bar chart - Sales by Category...")

    fig, ax = plt.subplots(figsize=(10, 6))
    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
    bars = ax.barh(cat_sales.index, cat_sales.values, color=COLORS[:3], edgecolor='white', linewidth=0.8)
    for bar, val in zip(bars, cat_sales.values):
        ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
                f'${val:,.0f}', va='center', fontsize=10, fontweight='bold')
    ax.set_title('Total Sales by Product Category', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Total Sales ($)', fontsize=11)
    ax.set_ylabel('Category', fontsize=11)
    ax.set_xlim(0, cat_sales.max() * 1.15)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.tight_layout()
    bar_path = os.path.join(VIZ_DIR, "bar_chart.png")
    fig.savefig(bar_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {bar_path}")

    # ═══════════════════════════════════════════════════════════
    # Chart 2: LINE CHART - Monthly Sales Trend
    # ═══════════════════════════════════════════════════════════
    print("\n[Chart 2] Creating line chart - Monthly Sales Trend...")

    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_sales3 = df.groupby(df['OrderDate'].dt.to_period('M'))['Sales'].sum()
    x_labels = [str(p) for p in monthly_sales3.index]
    y_values = monthly_sales3.values
    ax.plot(x_labels, y_values, marker='o', color=COLORS[0], linewidth=2, markersize=4)
    ax.fill_between(range(len(x_labels)), y_values, alpha=0.1, color=COLORS[0])
    ax.set_title('Monthly Sales Trend (2016-2019)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Total Sales ($)', fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.xticks(rotation=45, ha='right', fontsize=8)
    ax.legend(['Sales Trend'], loc='upper left', fontsize=10)
    plt.tight_layout()
    line_path = os.path.join(VIZ_DIR, "line_chart.png")
    fig.savefig(line_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {line_path}")

    # ═══════════════════════════════════════════════════════════
    # Chart 3: PIE CHART - Sales Composition by Category
    # ═══════════════════════════════════════════════════════════
    print("\n[Chart 3] Creating pie chart - Sales Composition by Category...")

    fig, ax = plt.subplots(figsize=(8, 8))
    cat_pie = df.groupby('Category')['Sales'].sum()
    wedges, texts, autotexts = ax.pie(
        cat_pie.values,
        labels=cat_pie.index,
        autopct='%1.1f%%',
        colors=COLORS[:len(cat_pie)],
        startangle=90,
        explode=(0.02, 0.02, 0.02),
        textprops={'fontsize': 11}
    )
    for at in autotexts:
        at.set_fontweight('bold')
    ax.set_title('Sales Distribution by Category', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    pie_path = os.path.join(VIZ_DIR, "pie_chart.png")
    fig.savefig(pie_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {pie_path}")

    # ═══════════════════════════════════════════════════════════
    # Chart 4: HISTOGRAM - Distribution of Sales
    # ═══════════════════════════════════════════════════════════
    print("\n[Chart 4] Creating histogram - Distribution of Sales...")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['Sales'], bins=50, color=COLORS[0], edgecolor='white', alpha=0.85)
    ax.axvline(df['Sales'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["Sales"].mean():,.0f}')
    ax.axvline(df['Sales'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${df["Sales"].median():,.0f}')
    ax.set_title('Distribution of Sales', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Sales ($)', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.legend(fontsize=10)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.tight_layout()
    hist_path = os.path.join(VIZ_DIR, "histogram.png")
    fig.savefig(hist_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {hist_path}")

    # ═══════════════════════════════════════════════════════════
    # Chart 5: SCATTER PLOT - Sales vs Profit
    # ═══════════════════════════════════════════════════════════
    print("\n[Chart 5] Creating scatter plot - Sales vs Profit...")

    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(
        df['Sales'], df['Profit'],
        c=df['Discount'], cmap='RdYlGn_r',
        alpha=0.6, edgecolors='white', linewidth=0.3, s=30
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Discount Rate', fontsize=10)
    ax.set_title('Sales vs Profit (colored by Discount)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Sales ($)', fontsize=11)
    ax.set_ylabel('Profit ($)', fontsize=11)
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.tight_layout()
    scatter_path = os.path.join(VIZ_DIR, "scatter_plot.png")
    fig.savefig(scatter_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {scatter_path}")

    # ═══════════════════════════════════════════════════════════
    # Bonus: Additional Chart - Profit by Category (Box Plot)
    # ═══════════════════════════════════════════════════════════
    print("\n[Bonus] Creating box plot - Profit by Category...")

    fig, ax = plt.subplots(figsize=(10, 6))
    df.boxplot(column='Profit', by='Category', ax=ax, patch_artist=True,
               boxprops=dict(facecolor=COLORS[1], alpha=0.6),
               medianprops=dict(color='black', linewidth=2))
    ax.set_title('Profit Distribution by Category', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Category', fontsize=11)
    ax.set_ylabel('Profit ($)', fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.suptitle('')  # Remove default title
    plt.tight_layout()
    box_path = os.path.join(VIZ_DIR, "box_plot.png")
    fig.savefig(box_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {box_path}")

    # ═══════════════════════════════════════════════════════════
    # Bonus: Stacked Bar - Yearly Sales by Category
    # ═══════════════════════════════════════════════════════════
    print("\n[Bonus] Creating stacked bar - Yearly Sales by Category...")

    fig, ax = plt.subplots(figsize=(10, 6))
    yearly_cat = df.groupby(['OrderYear', 'Category'])['Sales'].sum().unstack(fill_value=0)
    yearly_cat.plot(kind='bar', stacked=True, ax=ax, color=COLORS[:3], edgecolor='white')
    ax.set_title('Yearly Sales by Category', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Total Sales ($)', fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.xticks(rotation=0)
    ax.legend(title='Category', fontsize=9)
    plt.tight_layout()
    stacked_path = os.path.join(VIZ_DIR, "stacked_bar.png")
    fig.savefig(stacked_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {stacked_path}")

    # ═══════════════════════════════════════════════════════════
    # Bonus: Heatmap - Correlation Matrix
    # ═══════════════════════════════════════════════════════════
    print("\n[Bonus] Creating heatmap - Correlation Matrix...")

    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[['Sales', 'Quantity', 'Discount', 'Profit']].corr()
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='RdYlGn_r',
                vmin=-1, vmax=1, center=0, ax=ax,
                linewidths=1, linecolor='white', square=True)
    ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    heatmap_path = os.path.join(VIZ_DIR, "correlation_heatmap.png")
    fig.savefig(heatmap_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    [OK] Saved: {heatmap_path}")

    # ═══════════════════════════════════════════════════════════
    # Interactive Plotly Dashboard
    # ═══════════════════════════════════════════════════════════
    print("\n[Plotly] Creating interactive dashboard...")

    # Sales by Category (interactive bar)
    fig_cat = px.bar(
        df.groupby('Category')['Sales'].sum().reset_index(),
        x='Category', y='Sales',
        color='Category',
        title='Total Sales by Category',
        labels={'Sales': 'Total Sales ($)', 'Category': 'Product Category'},
        color_discrete_sequence=COLORS,
        text_auto='$,.0f'
    )
    fig_cat.update_layout(
        title_font_size=18,
        xaxis_title='Product Category',
        yaxis_title='Total Sales ($)',
        showlegend=False,
        template='plotly_white',
        height=500
    )
    fig_cat.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_cat_path = os.path.join(VIZ_DIR, "interactive_sales_by_category.html")
    fig_cat.write_html(fig_cat_path)
    print(f"    [OK] Saved: {fig_cat_path}")

    # Monthly Sales Trend (interactive line)
    monthly_sales_line = df.groupby(df['OrderDate'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_sales_line.columns = ['Period', 'Sales']
    monthly_sales_line['Period'] = monthly_sales_line['Period'].astype(str)
    fig_line = px.line(
        monthly_sales_line,
        x='Period', y='Sales',
        title='Monthly Sales Trend',
        labels={'Sales': 'Total Sales ($)', 'Period': 'Month'},
        template='plotly_white',
        height=500
    )
    fig_line.update_layout(
        title_font_size=18,
        xaxis_title='Month',
        yaxis_title='Total Sales ($)',
        yaxis_tickformat='$,.0f',
        height=500
    )
    fig_line_path = os.path.join(VIZ_DIR, "interactive_monthly_sales.html")
    fig_line.write_html(fig_line_path)
    print(f"    [OK] Saved: {fig_line_path}")

    # Profit by Category (interactive pie)
    fig_pie = px.pie(
        df.groupby('Category')['Profit'].sum().reset_index(),
        values='Profit', names='Category',
        title='Profit Composition by Category',
        color_discrete_sequence=COLORS,
        hole=0.4,
        height=500
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie_path = os.path.join(VIZ_DIR, "interactive_profit_by_category.html")
    fig_pie.write_html(fig_pie_path)
    print(f"    [OK] Saved: {fig_pie_path}")

    # Sales vs Profit scatter (interactive)
    fig_scatter = px.scatter(
        df.sample(min(2000, len(df))),
        x='Sales', y='Profit',
        color='Category',
        size='Quantity',
        hover_data=['Discount', 'ShipMode', 'Region'],
        title='Sales vs Profit by Category',
        labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)', 'Category': 'Product Category'},
        color_discrete_sequence=COLORS,
        height=500
    )
    fig_scatter.update_layout(template='plotly_white', height=500)
    fig_scatter_path = os.path.join(VIZ_DIR, "interactive_sales_vs_profit.html")
    fig_scatter.write_html(fig_scatter_path)
    print(f"    [OK] Saved: {fig_scatter_path}")

    # Distribution histogram (interactive)
    fig_hist = px.histogram(
        df, x='Sales', nbins=50,
        title='Distribution of Sales',
        labels={'Sales': 'Sales ($)'},
        color_discrete_sequence=[COLORS[0]],
        height=500
    )
    fig_hist.add_vline(x=df['Sales'].mean(), line_dash='dash', line_color='red',
                       annotation_text=f"Mean: ${df['Sales'].mean():,.0f}")
    fig_hist.add_vline(x=df['Sales'].median(), line_dash='dash', line_color='green',
                       annotation_text=f"Median: ${df['Sales'].median():,.0f}")
    fig_hist.update_layout(
        title_font_size=18,
        xaxis_title='Sales ($)',
        yaxis_title='Count',
        template='plotly_white',
        height=500
    )
    fig_hist_path = os.path.join(VIZ_DIR, "interactive_sales_distribution.html")
    fig_hist.write_html(fig_hist_path)
    print(f"    [OK] Saved: {fig_hist_path}")

    print("\n" + "=" * 70)
    print("VISUALIZATION SUMMARY")
    print("=" * 70)
    print(f"- Bar chart: {bar_path}")
    print(f"- Line chart: {line_path}")
    print(f"- Pie chart: {pie_path}")
    print(f"- Histogram: {hist_path}")
    print(f"- Scatter plot: {scatter_path}")
    print(f"- Bonus charts: box_plot, stacked_bar, correlation_heatmap")
    print(f"- Interactive plots: 5 HTML dashboards")
    print(f"\nAll visualizations saved to: {VIZ_DIR}")

    print("\n" + "=" * 70)
    print("TASK 3 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()