"""Generate Jupyter notebooks for all three tasks."""
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
import os

BASE = os.path.dirname(__file__)

def make_notebook(cells, title, filename):
    nb = new_notebook()
    nb['metadata'] = {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.14.6'}
    }
    for cell_type, content in cells:
        if cell_type == 'md':
            nb['cells'].append(new_markdown_cell(content))
        else:
            nb['cells'].append(new_code_cell(content))
    with open(filename, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Created: {filename}")

# ── Task 1 Notebook ──
task1_cells = [
    ('md', '# Task 1: Data Cleaning & Preprocessing\n\n**CodSoft Internship** — Dataset: Superstore Sales Dataset'),
    ('md', '## 1. Import Dataset'),
    ('code', '''
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load the raw dataset
df = pd.read_csv('data/raw/superstore.csv')
print(f'Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns')
print(f'Columns: {list(df.columns)}')
'''),
    ('md', '## 2. Inspect Dataset Structure'),
    ('code', '''
print(f'Number of rows: {df.shape[0]}')
print(f'Number of columns: {df.shape[1]}')
print(f'Column names: {list(df.columns)}')
print('\\nData types:')
print(df.dtypes)
print('\\nSample records:')
print(df.head().to_string())
'''),
    ('md', '## 3. Identify Missing Values'),
    ('code', '''
missing_counts = df.isnull().sum()
missing_info = pd.DataFrame({
    'Missing Count': missing_counts,
    'Missing %': (missing_counts / len(df) * 100).round(2)
})
missing_info = missing_info[missing_info['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
print('Columns with missing values:')
print(missing_info.to_string())
print(f'\\nTotal missing cells: {missing_info["Missing Count"].sum()}')
'''),
    ('md', '## 4. Identify and Remove Duplicate Records'),
    ('code', '''
dup_mask = df.duplicated(keep=False)
n_dupes = dup_mask.sum()
print(f'Total duplicate rows (marked): {n_dupes}')

# Remove duplicates keeping first occurrence
df_clean = df.drop_duplicates(keep='first')
n_removed = len(df) - len(df_clean)
print(f'Duplicates removed: {n_removed}')
print(f'Remaining rows: {len(df_clean)}')
'''),
    ('md', '## 5. Identify Inconsistent Data'),
    ('code', '''
# Check ShipMode and Region consistency
print('ShipMode values:', df_clean['ShipMode'].nunique())
print(df_clean['ShipMode'].value_counts().to_string())
print('\\nRegion values:', df_clean['Region'].nunique())
print(df_clean['Region'].value_counts().to_string())
print('\\nCategory values:', df_clean['Category'].nunique())
print(df_clean['Category'].value_counts().to_string())
'''),
    ('md', '## 6. Handle Null Values & Correct Data Types'),
    ('code', '''
# Fill missing Postal Code with mode
postal_missing = df_clean['Postal Code'].isnull().sum()
if postal_missing > 0:
    mode_postal = df_clean['Postal Code'].mode()[0]
    df_clean['Postal Code'] = df_clean['Postal Code'].fillna(mode_postal)
    print(f'Filled {postal_missing} missing Postal Code with mode: {mode_postal}')

# Convert date columns to datetime
df_clean['OrderDate'] = pd.to_datetime(df_clean['OrderDate'], format='mixed')
df_clean['ShipDate'] = pd.to_datetime(df_clean['ShipDate'], format='mixed')

# Convert Postal Code to nullable integer
df_clean['Postal Code'] = df_clean['Postal Code'].astype('Int64')

# Ensure numeric columns are correct
for col in ['Sales', 'Quantity', 'Discount', 'Profit']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

print('Data types after cleaning:')
print(df_clean.dtypes)
'''),
    ('md', '## 7. Verify Final Dataset'),
    ('code', '''
print(f'Missing values: {df_clean.isnull().sum().sum()}')
print(f'Duplicate rows: {df_clean.duplicated().sum()}')
print(f'Final shape: {df_clean.shape}')
print('[OK] Dataset is clean and ready for EDA')
'''),
    ('md', '## 8. Export Cleaned Dataset'),
    ('code', '''
cleaned_path = 'data/processed/cleaned_dataset.csv'
df_clean.to_csv(cleaned_path, index=False)
print(f'Cleaned dataset exported: {cleaned_path}')
''')
]
make_notebook(task1_cells, 'Task 1', os.path.join(BASE, 'Task-1-Data-Cleaning/notebooks/data_cleaning.ipynb'))

# ── Task 2 Notebook ──
task2_cells = [
    ('md', '# Task 2: Exploratory Data Analysis (EDA)\n\n**CodSoft Internship** — Dataset: Superstore Sales (cleaned)'),
    ('md', '## 1. Load Cleaned Dataset'),
    ('code', '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set_style('whitegrid')

# Load the cleaned dataset from Task 1
df = pd.read_csv('../Task-1-Data-Cleaning/data/processed/cleaned_dataset.csv')
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
print(f'Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns')
print(f'Date range: {df["OrderDate"].min()} to {df["OrderDate"].max()}')
'''),
    ('md', '## 2. Descriptive Statistics'),
    ('code', '''
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
stats = df[numeric_cols].describe().round(2)
print(stats.to_string())
print(f'\\nTotal Revenue: ${df["Sales"].sum():,.2f}')
print(f'Total Profit: ${df["Profit"].sum():,.2f}')
print(f'Profit Margin: {df["Profit"].sum()/df["Sales"].sum()*100:.2f}%')
'''),
    ('md', '## 3. Distribution Analysis'),
    ('code', '''
print('Category distribution:')
print(df['Category'].value_counts().to_string())
print('\\nSegment distribution:')
print(df['Segment'].value_counts().to_string())
print('\\nProfit distribution:')
print(f'Positive profit: {len(df[df["Profit"] > 0])} ({len(df[df["Profit"] > 0])/len(df)*100:.1f}%)')
print(f'Negative profit: {len(df[df["Profit"] < 0])} ({len(df[df["Profit"] < 0])/len(df)*100:.1f}%)')
'''),
    ('md', '## 4. Trend Analysis'),
    ('code', '''
df['OrderYear'] = df['OrderDate'].dt.year
df['OrderMonth'] = df['OrderDate'].dt.month

# Yearly trends
yearly = df.groupby('OrderYear').agg({'Sales': 'sum', 'Profit': 'sum'})
print('Yearly sales and profit:')
print(yearly.round(2).to_string())

# Monthly seasonality
monthly = df.groupby('OrderMonth')['Sales'].sum()
print(f'\\nPeak month: {monthly.idxmax()} (${monthly.max():,.2f})')
print(f'Lowest month: {monthly.idxmin()} (${monthly.min():,.2f})')
'''),
    ('md', '## 5. Relationship Analysis (Correlation)'),
    ('code', '''
corr = df[numeric_cols].corr().round(4)
print('Correlation matrix:')
print(corr.to_string())

print(f'\\nSales-Profit correlation: {corr.loc["Sales","Profit"]:.4f}')
print(f'Profit-Discount correlation: {corr.loc["Profit","Discount"]:.4f}')

# Category analysis
print('\\nSales and profit by category:')
print(df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).round(2).to_string())
'''),
    ('md', '## 6. Outlier Detection (IQR Method)'),
    ('code', '''
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    low_out = df[df[col] < lower]
    high_out = df[df[col] > upper]
    print(f'{col}: Low={len(low_out)}, High={len(high_out)} outliers')
'''),
    ('md', '## 7. Unusual Patterns'),
    ('code', '''
# High discount, loss-making orders
hdl = df[(df['Discount'] >= 0.5) & (df['Profit'] < 0)]
print(f'High-discount loss-making orders: {len(hdl)} ({len(hdl)/len(df)*100:.1f}%)')
print('\\nTop loss-making products:')
print(df[df['Profit'] < 0].groupby('ProductName')['Profit'].sum().sort_values().head(5).to_string())
'''),
    ('md', '## 8. Business Questions'),
    ('code', '''
# Q1: Most revenue category
rev_by_cat = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
print(f'Q1: Top revenue category: {rev_by_cat.index[0]} (${rev_by_cat.iloc[0]:,.2f})')

# Q2: Most profitable segment
prof_by_seg = df.groupby('Segment')['Profit'].sum().sort_values(ascending=False)
print(f'Q2: Most profitable segment: {prof_by_seg.index[0]} (${prof_by_seg.iloc[0]:,.2f})')

# Q3: Highest sales region
sales_by_reg = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print(f'Q3: Highest sales region: {sales_by_reg.index[0]} (${sales_by_reg.iloc[0]:,.2f})')

# Q4: Overall profitability
print(f'Q4: Revenue=${df["Sales"].sum():,.2f}, Profit=${df["Profit"].sum():,.2f}')
''')
]
make_notebook(task2_cells, 'Task 2', os.path.join(BASE, 'Task-2-EDA/notebooks/eda.ipynb'))

# ── Task 3 Notebook ──
task3_cells = [
    ('md', '# Task 3: Data Visualization Dashboard\n\n**CodSoft Internship** — Dataset: Superstore Sales (cleaned)'),
    ('md', '## 1. Prepare Visualization Dataset'),
    ('code', '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4']
sns.set_palette(sns.color_palette(COLORS))

df = pd.read_csv('../Task-1-Data-Cleaning/data/processed/cleaned_dataset.csv')
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
print(f'Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns')
'''),
    ('md', '## 2. Bar Chart — Sales by Category'),
    ('code', '''
fig, ax = plt.subplots(figsize=(10, 6))
cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
bars = ax.barh(cat_sales.index, cat_sales.values, color=COLORS[:3], edgecolor='white', linewidth=0.8)
for bar, val in zip(bars, cat_sales.values):
    ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=10, fontweight='bold')
ax.set_title('Total Sales by Product Category', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Total Sales ($)', fontsize=11)
ax.set_ylabel('Category', fontsize=11)
plt.tight_layout()
plt.savefig('visualizations/bar_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print('[OK] Bar chart saved')
'''),
    ('md', '## 3. Line Chart — Monthly Sales Trend'),
    ('code', '''
fig, ax = plt.subplots(figsize=(12, 6))
monthly = df.groupby(df['OrderDate'].dt.to_period('M'))['Sales'].sum()
x_labels = [str(p) for p in monthly.index]
ax.plot(x_labels, monthly.values, marker='o', color=COLORS[0], linewidth=2, markersize=4)
ax.fill_between(range(len(x_labels)), monthly.values, alpha=0.1, color=COLORS[0])
ax.set_title('Monthly Sales Trend (2016-2019)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Total Sales ($)', fontsize=11)
plt.xticks(rotation=45, ha='right', fontsize=8)
ax.legend(['Sales Trend'], loc='upper left', fontsize=10)
plt.tight_layout()
plt.savefig('visualizations/line_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print('[OK] Line chart saved')
'''),
    ('md', '## 4. Pie Chart — Sales Composition by Category'),
    ('code', '''
fig, ax = plt.subplots(figsize=(8, 8))
cat_pie = df.groupby('Category')['Sales'].sum()
wedges, texts, autotexts = ax.pie(
    cat_pie.values, labels=cat_pie.index,
    autopct='%1.1f%%', colors=COLORS[:len(cat_pie)], startangle=90,
    explode=(0.02, 0.02, 0.02), textprops={'fontsize': 11}
)
for at in autotexts:
    at.set_fontweight('bold')
ax.set_title('Sales Distribution by Category', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('visualizations/pie_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print('[OK] Pie chart saved')
'''),
    ('md', '## 5. Histogram — Sales Distribution'),
    ('code', '''
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['Sales'], bins=50, color=COLORS[0], edgecolor='white', alpha=0.85)
ax.axvline(df['Sales'].mean(), color='red', linestyle='--', linewidth=2,
           label=f'Mean: ${df["Sales"].mean():,.0f}')
ax.axvline(df['Sales'].median(), color='green', linestyle='--', linewidth=2,
           label=f'Median: ${df["Sales"].median():,.0f}')
ax.set_title('Distribution of Sales', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Sales ($)', fontsize=11)
ax.set_ylabel('Frequency', fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('visualizations/histogram.png', dpi=150, bbox_inches='tight')
plt.show()
print('[OK] Histogram saved')
'''),
    ('md', '## 6. Scatter Plot — Sales vs Profit'),
    ('code', '''
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(
    df['Sales'], df['Profit'], c=df['Discount'], cmap='RdYlGn_r',
    alpha=0.6, edgecolors='white', linewidth=0.3, s=30
)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Discount Rate', fontsize=10)
ax.set_title('Sales vs Profit (colored by Discount)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Sales ($)', fontsize=11)
ax.set_ylabel('Profit ($)', fontsize=11)
ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
plt.tight_layout()
plt.savefig('visualizations/scatter_plot.png', dpi=150, bbox_inches='tight')
plt.show()
print('[OK] Scatter plot saved')
'''),
    ('md', '## 7. Interactive Plotly Dashboards (Bonus)'),
    ('code', '''
# Interactive bar chart
fig = px.bar(
    df.groupby('Category')['Sales'].sum().reset_index(),
    x='Category', y='Sales', color='Category',
    title='Total Sales by Category',
    labels={'Sales': 'Total Sales ($)', 'Category': 'Product Category'},
    color_discrete_sequence=COLORS, text_auto=True
)
fig.update_layout(template='plotly_white')
fig.write_html('visualizations/interactive_sales_by_category.html')
print('[OK] Interactive bar chart saved')

# Interactive line chart
monthly_df = monthly.reset_index()
monthly_df.columns = ['Period', 'Sales']
fig2 = px.line(monthly_df, x='Period', y='Sales', title='Monthly Sales Trend')
fig2.update_layout(template='plotly_white')
fig2.write_html('visualizations/interactive_monthly_sales.html')
print('[OK] Interactive line chart saved')

# Interactive pie chart
fig3 = px.pie(
    df.groupby('Category')['Profit'].sum().reset_index(),
    values='Profit', names='Category', title='Profit by Category',
    color_discrete_sequence=COLORS
)
fig3.write_html('visualizations/interactive_profit_by_category.html')
print('[OK] Interactive pie chart saved')
''')
]
make_notebook(task3_cells, 'Task 3', os.path.join(BASE, 'Task-3-Data-Visualization/notebooks/visualization.ipynb'))
