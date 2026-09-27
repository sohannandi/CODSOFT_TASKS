"""
Task 1 — Data Cleaning & Preprocessing
CodSoft Data Analytics Internship
Dataset: Superstore Sales Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# Fix encoding for Windows console
import sys
if sys.stdout.encoding.lower() in ['cp1252', 'latin1']:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_PATH = os.path.join(BASE_DIR, "Task-1-Data-Cleaning", "data", "raw", "superstore.csv")
CLEANED_PATH = os.path.join(BASE_DIR, "Task-1-Data-Cleaning", "data", "processed", "cleaned_dataset.csv")

def main():
    print("=" * 70)
    print("TASK 1: Data Cleaning & Preprocessing")
    print("=" * 70)

    # ── FR-1: Import Dataset ──
    print("\n[FR-1] Loading dataset...")
    df = pd.read_csv(RAW_PATH)
    print(f"    [OK] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")

    # ── FR-2: Inspect Dataset Structure ──
    print("\n[FR-2] Inspecting dataset structure...")
    print(f"    - Number of rows: {df.shape[0]}")
    print(f"    - Number of columns: {df.shape[1]}")
    print(f"    - Column names: {list(df.columns)}")
    print(f"    - Data types:")
    print(df.dtypes.to_string())
    print(f"    - Sample records:")
    print(df.head().to_string())

    # ── FR-3: Identify Missing Values ──
    print("\n[FR-3] Identifying missing values...")
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df) * 100).round(2)
    missing_info = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing %': missing_pct
    })
    missing_info = missing_info[missing_info['Missing Count'] > 0].sort_values(
        'Missing Count', ascending=False
    )
    print(f"    - Columns with missing values:")
    print(missing_info.to_string())
    if not missing_info.empty:
        total_missing = missing_info['Missing Count'].sum()
        total_pct = missing_info['Missing %'].sum()
        print(f"    - Total missing cells: {total_missing}")
        print(f"    - Total missing %: {total_pct:.2f}%")

    # ── FR-4: Identify Duplicate Records ──
    print("\n[FR-4] Identifying duplicate records...")
    dup_mask = df.duplicated(keep=False)
    n_dupes = dup_mask.sum()
    print(f"    - Total duplicate rows: {n_dupes}")
    if n_dupes > 0:
        print(f"    - Duplicate row example(s):")
        dupes = df[dup_mask].head(3)
        print(dupes.to_string())

    # Remove duplicates (keep first occurrence)
    df_clean = df.drop_duplicates(keep='first')
    n_removed = len(df) - len(df_clean)
    print(f"    - Duplicates removed: {n_removed}")
    print(f"    - Remaining rows: {len(df_clean)}")

    # ── FR-5: Identify Inconsistent Data ──
    print("\n[FR-5] Checking for inconsistent data...")

    # Check OrderYear vs OrderDate consistency
    print("    - Checking OrderYear vs actual date...")
    try:
        df['OrderDate_parsed'] = pd.to_datetime(df['OrderDate'], format='mixed', dayfirst=False)
        year_from_date = df['OrderDate_parsed'].dt.year
        mismatch = (df['OrderYear'] != year_from_date).sum()
        print(f"    - OrderYear vs parsed OrderDate mismatch: {mismatch} rows")
    except Exception as e:
        print(f"    - Note: Date parsing issue: {e}")

    # Check for inconsistent ShipMode values
    print(f"    - Unique ShipMode values: {df['ShipMode'].nunique()}")
    print(f"    - ShipMode distribution:")
    print(df['ShipMode'].value_counts().to_string())

    # Check for inconsistent Region values
    print(f"    - Unique Region values: {df['Region'].nunique()}")
    print(f"    - Region distribution:")
    print(df['Region'].value_counts().to_string())

    # Check Category consistency
    print(f"    - Unique Category values: {df['Category'].nunique()}")
    print(f"    - Category distribution:")
    print(df['Category'].value_counts().to_string())

    # ── FR-6: Handle Null Values ──
    print("\n[FR-6] Handling null values...")
    postal_missing = df_clean['Postal Code'].isnull().sum()
    print(f"    - Postal Code missing values: {postal_missing} out of {len(df_clean)} ({postal_missing/len(df_clean)*100:.2f}%)")

    # Strategy: Fill missing Postal Code with mode (most frequent)
    if postal_missing > 0:
        mode_postal = df_clean['Postal Code'].mode()[0]
        df_clean['Postal Code'] = df_clean['Postal Code'].fillna(mode_postal)
        print(f"    - Filled missing Postal Code with mode: {mode_postal}")
    else:
        print("    - No handling needed - Postal Code has no missing values after dedup")

    # Check for any other remaining missing
    remaining_missing = df_clean.isnull().sum().sum()
    if remaining_missing == 0:
        print("    - [OK] No remaining missing values in cleaned dataset")
    else:
        print(f"    - [WARNING] {remaining_missing} missing values remain - reviewing...")

    # ── FR-7: Correct Data Types ──
    print("\n[FR-7] Correcting data types...")

    # OrderDate: convert from string to datetime
    print("    - Converting OrderDate from string to datetime...")
    df_clean['OrderDate'] = pd.to_datetime(df_clean['OrderDate'], format='mixed')
    print(f"    - OrderDate dtype: {df_clean['OrderDate'].dtype}")

    # ShipDate: convert from string to datetime
    print("    - Converting ShipDate from string to datetime...")
    df_clean['ShipDate'] = pd.to_datetime(df_clean['ShipDate'], format='mixed')
    print(f"    - ShipDate dtype: {df_clean['ShipDate'].dtype}")

    # Postal Code: convert to nullable integer
    print("    - Converting Postal Code to nullable integer...")
    df_clean['Postal Code'] = df_clean['Postal Code'].astype('Int64')
    print(f"    - Postal Code dtype: {df_clean['Postal Code'].dtype}")

    # Ensure numeric columns are proper types
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    for col in numeric_cols:
        if df_clean[col].dtype != 'float64' and df_clean[col].dtype != 'int64':
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        print(f"    - {col} dtype: {df_clean[col].dtype}")

    # OrderYear: verify it's consistent with OrderDate
    year_from_new_date = df_clean['OrderDate'].dt.year
    year_mismatches = (df_clean['OrderYear'] != year_from_new_date).sum()
    if year_mismatches > 0:
        print(f"    - [NOTE] {year_mismatches} OrderYear values inconsistent with parsed dates - correcting...")
        df_clean['OrderYear'] = year_from_new_date
    else:
        print(f"    - [OK] OrderYear consistent with parsed dates")

    # ── FR-8: Prepare Final Dataset ──
    print("\n[FR-8] Final dataset verification...")

    # Recheck missing values
    print(f"    - Missing values after cleaning:")
    print(df_clean.isnull().sum().to_string())

    # Recheck duplicate records
    new_dupes = df_clean.duplicated().sum()
    print(f"    - Duplicate rows after cleaning: {new_dupes}")

    # Recheck data types
    print(f"    - Final dtypes:")
    print(df_clean.dtypes.to_string())

    # Verify dataset is suitable for analysis
    print(f"    - Dataset info:")
    print(f"      - Rows: {df_clean.shape[0]}")
    print(f"      - Columns: {df_clean.shape[1]}")
    print(f"      - No critical missing values: {df_clean.isnull().sum().max() == 0}")
    print(f"      - No duplicate records: {new_dupes == 0}")

    # ── FR-9: Export Cleaned Dataset ──
    print(f"\n[FR-9] Exporting cleaned dataset to {CLEANED_PATH}...")
    os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
    df_clean.to_csv(CLEANED_PATH, index=False)
    print(f"    [OK] Cleaned dataset saved")
    print(f"    - Shape of cleaned dataset: {df_clean.shape}")

    # ── Create visualization of data quality improvements ──
    plt.figure(figsize=(10, 6))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Missing values before
    missing_before = df.isnull().sum()
    missing_before = missing_before[missing_before > 0].sort_values(ascending=False)
    ax1.barh(missing_before.index.astype(str), missing_before.values, color='red', alpha=0.7)
    ax1.set_title('Missing Values - Before Cleaning', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Count')
    ax1.invert_yaxis()

    # Missing values after
    missing_after = df_clean.isnull().sum()
    missing_after = missing_after[missing_after > 0].sort_values(ascending=False)
    colors = ['green' if v == 0 else 'red' for v in missing_after.values]
    ax2.barh(missing_after.index.astype(str), missing_after.values, color=colors, alpha=0.7)
    ax2.set_title('Missing Values - After Cleaning', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Count')
    ax2.invert_yaxis()

    plt.tight_layout()
    viz_dir = os.path.join(BASE_DIR, "Task-1-Data-Cleaning", "visuals")
    os.makedirs(viz_dir, exist_ok=True)
    viz_path = os.path.join(viz_dir, "missing_data_comparison.png")
    plt.savefig(viz_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    [OK] Missing data comparison chart saved")

    print("\n" + "=" * 70)
    print("CLEANING SUMMARY")
    print("=" * 70)
    print(f"- Original rows: {len(df)} -> Cleaned rows: {len(df_clean)}")
    print(f"- Duplicates removed: {n_removed}")
    print(f"- Missing values handled: {df['Postal Code'].isnull().sum()} -> 0")
    print(f"- Data types corrected: OrderDate, ShipDate, Postal Code, numeric verification")
    print(f"- Dataset exported and ready for EDA")

    print("\n" + "=" * 70)
    print("TASK 1 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()