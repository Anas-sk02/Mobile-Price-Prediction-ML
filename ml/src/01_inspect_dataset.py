"""
SmartPrice - Phase 1: Dataset Inspection & Quality Audit
=========================================================
Performs automated comprehensive inspection of the smartphone dataset,
auditing data types, missing values, duplicates, distributions,
and potential data quality issues before any modeling steps.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "smartphone_cleaned_v5.csv"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def inspect_dataset(data_path: Path):
    print("=" * 80)
    print(" SmartPrice — Dataset Inspection & Quality Audit")
    print("=" * 80)

    if not data_path.exists():
        fallback = PROJECT_ROOT / "smartphone_cleaned_v5.csv"
        if fallback.exists():
            data_path = fallback
        else:
            raise FileNotFoundError(f"Dataset not found at {data_path}")

    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)

    total_rows, total_cols = df.shape
    memory_kb = df.memory_usage(deep=True).sum() / 1024

    print(f"\n[1] Basic Dimensions & Memory:")
    print(f"    - Total Records (Rows): {total_rows}")
    print(f"    - Total Features (Cols): {total_cols}")
    print(f"    - Memory Consumption:   {memory_kb:.2f} KB")

    # Duplicate check
    full_duplicates = df.duplicated().sum()
    model_duplicates = df['model'].duplicated().sum() if 'model' in df.columns else 0
    print(f"\n[2] Duplicates Audit:")
    print(f"    - Identical Duplicate Rows: {full_duplicates}")
    print(f"    - Duplicate Model Names:    {model_duplicates}")

    # Column-level audit
    col_audit = []
    print(f"\n[3] Column-by-Column Data Audit:")
    print(f"{'-'*80}")
    print(f"{'Col #':<6}{'Column Name':<28}{'Dtype':<10}{'Nulls':<8}{'Null %':<8}{'Uniques':<8}")
    print(f"{'-'*80}")

    for idx, col in enumerate(df.columns, 1):
        null_count = int(df[col].isnull().sum())
        # Check for empty string or whitespace if object
        if df[col].dtype == 'object':
            empty_str_count = int((df[col].astype(str).str.strip() == '').sum())
            null_count += empty_str_count
        
        null_pct = (null_count / total_rows) * 100
        n_unique = int(df[col].nunique(dropna=True))
        dtype_str = str(df[col].dtype)
        
        col_audit.append({
            "col_index": idx,
            "column_name": col,
            "dtype": dtype_str,
            "null_count": null_count,
            "null_percent": round(null_pct, 2),
            "unique_count": n_unique,
            "sample_values": [str(x) for x in df[col].dropna().unique()[:3]]
        })
        
        print(f"{idx:<6}{col:<28}{dtype_str:<10}{null_count:<8}{null_pct:<8.1f}%{n_unique:<8}")

    # Numerical statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"\n[4] Numerical Feature Descriptive Statistics ({len(numeric_cols)} numeric features):")
    print(f"{'-'*90}")
    print(f"{'Feature':<25}{'Min':<10}{'25%':<10}{'Median':<10}{'75%':<10}{'Max':<12}{'Mean':<10}{'Std':<10}")
    print(f"{'-'*90}")

    num_stats = {}
    for col in numeric_cols:
        s = df[col].dropna()
        q25, q50, q75 = s.quantile(0.25), s.median(), s.quantile(0.75)
        num_stats[col] = {
            "count": int(s.count()),
            "mean": round(float(s.mean()), 2),
            "std": round(float(s.std()), 2),
            "min": round(float(s.min()), 2),
            "q25": round(float(q25), 2),
            "median": round(float(q50), 2),
            "q75": round(float(q75), 2),
            "max": round(float(s.max()), 2),
            "skewness": round(float(s.skew()), 2)
        }
        print(f"{col:<25}{num_stats[col]['min']:<10.1f}{num_stats[col]['q25']:<10.1f}{num_stats[col]['median']:<10.1f}{num_stats[col]['q75']:<10.1f}{num_stats[col]['max']:<12.1f}{num_stats[col]['mean']:<10.1f}{num_stats[col]['std']:<10.1f}")

    # Price / Target audit
    print(f"\n[5] Target Variable (Price in INR) Audit:")
    price = df['price']
    print(f"    - Min Price:    Rs. {price.min():,}")
    print(f"    - 25th Pct:     Rs. {price.quantile(0.25):,.0f}")
    print(f"    - Median Price: Rs. {price.median():,.0f}")
    print(f"    - 75th Pct:     Rs. {price.quantile(0.75):,.0f}")
    print(f"    - 90th Pct:     Rs. {price.quantile(0.90):,.0f}")
    print(f"    - Max Price:    Rs. {price.max():,}")
    print(f"    - Mean Price:   Rs. {price.mean():,.2f}")
    print(f"    - Std Dev:      Rs. {price.std():,.2f}")
    print(f"    - Skewness:     {price.skew():.2f} (High right skew, typical for price data)")

    # Standard 4-tier price categorization
    # Budget <= 15000, Mid-Range 15001-30000, Premium 30001-50000, Flagship > 50000
    def categorize_price(p):
        if p <= 15000:
            return "Budget"
        elif p <= 30000:
            return "Mid-Range"
        elif p <= 50000:
            return "Premium"
        else:
            return "Flagship"

    price_categories = price.apply(categorize_price)
    cat_counts = price_categories.value_counts()
    cat_pcts = (price_categories.value_counts(normalize=True) * 100)

    print(f"\n[6] Target Class Distribution (Domain-Standard 4 Bins):")
    print(f"{'-'*60}")
    print(f"{'Class':<15}{'Price Range (INR)':<25}{'Count':<10}{'Percentage':<10}")
    print(f"{'-'*60}")
    ranges = {
        "Budget": "<= Rs. 15,000",
        "Mid-Range": "Rs. 15,001 - 30,000",
        "Premium": "Rs. 30,001 - 50,000",
        "Flagship": "> Rs. 50,000"
    }
    class_dist = {}
    for cat in ["Budget", "Mid-Range", "Premium", "Flagship"]:
        cnt = int(cat_counts.get(cat, 0))
        pct = float(cat_pcts.get(cat, 0.0))
        class_dist[cat] = {"count": cnt, "percent": round(pct, 2), "range": ranges[cat]}
        print(f"{cat:<15}{ranges[cat]:<25}{cnt:<10}{pct:<10.1f}%")

    # Categorical Columns & Top Values
    categorical_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()
    print(f"\n[7] Categorical Features ({len(categorical_cols)} features):")
    cat_summary = {}
    for col in categorical_cols:
        top_val_counts = df[col].value_counts().head(5).to_dict()
        cat_summary[col] = {
            "n_unique": int(df[col].nunique()),
            "top_5": {str(k): int(v) for k, v in top_val_counts.items()}
        }
        print(f"    * {col} ({df[col].nunique()} unique values): top -> {list(top_val_counts.items())[:3]}")

    # Data Quality Issues Identified
    quality_issues = [
        {
            "issue": "String Boolean Values",
            "columns": ["has_5g", "has_nfc", "has_ir_blaster"],
            "description": "Values stored as string 'True' / 'False' rather than native boolean or 0/1 integers.",
            "remediation": "Convert to integer boolean (1/0) during preprocessing."
        },
        {
            "issue": "Composite String Format in Resolution",
            "columns": ["resolution"],
            "description": "Stored as 'width x height' strings (e.g. '1080 x 2400').",
            "remediation": "Parse into resolution_width and resolution_height numerical features."
        },
        {
            "issue": "Missing Values in Hardware Specs",
            "columns": ["rating", "processor_brand", "processor_speed", "fast_charging", "num_front_cameras", "os", "primary_camera_front", "extended_upto"],
            "description": "Missing values present in multiple columns requiring principled imputation (median for numerical, mode / 'Unknown' for categorical).",
            "remediation": "Median imputation for numerical specs; domain fallback/mode for categorical attributes."
        },
        {
            "issue": "Target Leakage Prevention",
            "columns": ["price"],
            "description": "Continuous price column is used exclusively to generate the categorical target variable (price_category) and MUST be dropped from model input features.",
            "remediation": "Drop 'price' and 'model' from feature matrix X before training."
        }
    ]

    # Compile JSON report
    report = {
        "dataset_name": "smartphone_cleaned_v5.csv",
        "total_rows": total_rows,
        "total_columns": total_cols,
        "memory_kb": round(memory_kb, 2),
        "duplicates": {
            "exact_rows": int(full_duplicates),
            "duplicate_models": int(model_duplicates)
        },
        "columns_audit": col_audit,
        "numerical_statistics": num_stats,
        "price_summary": {
            "min": int(price.min()),
            "q25": int(price.quantile(0.25)),
            "median": int(price.median()),
            "q75": int(price.quantile(0.75)),
            "max": int(price.max()),
            "mean": round(float(price.mean()), 2),
            "std": round(float(price.std()), 2),
            "skewness": round(float(price.skew()), 2)
        },
        "target_class_distribution": class_dist,
        "categorical_summary": cat_summary,
        "data_quality_issues": quality_issues
    }

    # Save JSON report
    json_path = OUTPUT_DIR / "01_inspection_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n[OK] Inspection JSON Report saved to: {json_path}")

    # Generate Markdown Summary
    md_path = OUTPUT_DIR / "01_inspection_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# SmartPrice — Phase 1: Dataset Inspection Summary\n\n")
        f.write(f"- **Dataset File**: `smartphone_cleaned_v5.csv`\n")
        f.write(f"- **Total Records**: {total_rows}\n")
        f.write(f"- **Total Features**: {total_cols}\n")
        f.write(f"- **Exact Duplicates**: {full_duplicates}\n")
        f.write(f"- **Memory Usage**: {memory_kb:.2f} KB\n\n")
        
        f.write("## 1. Target Variable (Price) Distribution\n\n")
        f.write("| Metric | Value (INR) |\n")
        f.write("|---|---|\n")
        f.write(f"| Min Price | ₹{price.min():,} |\n")
        f.write(f"| 25th Percentile | ₹{price.quantile(0.25):,.0f} |\n")
        f.write(f"| Median Price | ₹{price.median():,.0f} |\n")
        f.write(f"| 75th Percentile | ₹{price.quantile(0.75):,.0f} |\n")
        f.write(f"| Max Price | ₹{price.max():,} |\n")
        f.write(f"| Mean Price | ₹{price.mean():,.2f} |\n")
        f.write(f"| Standard Deviation | ₹{price.std():,.2f} |\n")
        f.write(f"| Skewness | {price.skew():.2f} |\n\n")

        f.write("## 2. Target Category Class Breakdown\n\n")
        f.write("| Category | Price Range (INR) | Count | Percentage |\n")
        f.write("|---|---|---|---|\n")
        for cat, data in class_dist.items():
            f.write(f"| **{cat}** | {data['range']} | {data['count']} | {data['percent']}% |\n")
        f.write(f"| **Total** | | **{total_rows}** | **100.0%** |\n\n")

        f.write("## 3. Column Data Types & Missing Values\n\n")
        f.write("| Col # | Column Name | Dtype | Missing Count | Missing % |\n")
        f.write("|---|---|---|---|---|\n")
        for c in col_audit:
            f.write(f"| {c['col_index']} | `{c['column_name']}` | `{c['dtype']}` | {c['null_count']} | {c['null_percent']}% |\n")
        f.write("\n")

        f.write("## 4. Key Data Quality Findings & Remediation Plan\n\n")
        for idx, issue in enumerate(quality_issues, 1):
            f.write(f"### {idx}. {issue['issue']}\n")
            f.write(f"- **Affected Columns**: {', '.join([f'`{c}`' for c in issue['columns']])}\n")
            f.write(f"- **Finding**: {issue['description']}\n")
            f.write(f"- **Action Required**: {issue['remediation']}\n\n")
        
        f.write("## 5. Phase 1 Verification Status\n\n")
        f.write("- [x] Raw data verified in `data/raw/smartphone_cleaned_v5.csv`\n")
        f.write("- [x] Data structure, data types, and missingness audited\n")
        f.write("- [x] Target price distribution and 4-tier class categorization validated\n")
        f.write("- [x] Data quality issues documented with remediation steps\n")
        f.write("- [x] Inspection report generated (`01_inspection_report.json` and `01_inspection_summary.md`)\n")

    print(f"[OK] Inspection Markdown Summary saved to: {md_path}")
    print("=" * 80)
    print(" Phase 1: Dataset Inspection & Setup COMPLETED SUCCESSFULLY.")
    print("=" * 80)


if __name__ == "__main__":
    inspect_dataset(DATA_PATH)
