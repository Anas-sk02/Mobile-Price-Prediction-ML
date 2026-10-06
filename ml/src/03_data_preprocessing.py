"""
SmartPrice - Phase 3: Data Preprocessing, Feature Engineering & Pipeline Construction
======================================================================================
Implements reproducible preprocessing with zero data leakage:
1. Target Variable Definition (4-tier categorical encoding)
2. String parsing (resolution -> width, height, PPI, aspect ratio)
3. Category grouping for low-frequency brands & processors
4. Derived domain feature engineering (performance score, PPI, battery density)
5. Stratified 80/20 Train-Test split (random_state=42)
6. Scikit-Learn ColumnTransformer pipeline (Imputation, Standard Scaling, One-Hot Encoding)
7. Serializes preprocessor pipeline and train/test arrays
"""

import sys
import json
import re
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Reconfigure stdout for Windows console UTF-8 support
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

# Paths setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "smartphone_cleaned_v5.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "ml" / "models"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Target price category mapping
PRICE_BINS = [0, 15000, 30000, 50000, np.inf]
CLASS_NAMES = ["Budget", "Mid-Range", "Premium", "Flagship"]
CLASS_MAPPING = {0: "Budget", 1: "Mid-Range", 2: "Premium", 3: "Flagship"}
REVERSE_CLASS_MAPPING = {v: k for k, v in CLASS_MAPPING.items()}


def parse_resolution(res_str: str) -> tuple[int, int]:
    """Extract width and height integers from various resolution string formats."""
    if not isinstance(res_str, str) or not res_str.strip():
        return 1080, 2400  # Domain default
    
    # Clean whitespace and unicode thin spaces (\u2009)
    cleaned = res_str.replace('\u2009', ' ').replace('&nbsp;', ' ').strip()
    match = re.findall(r'(\d+)', cleaned)
    if len(match) >= 2:
        val1, val2 = int(match[0]), int(match[1])
        width = min(val1, val2)
        height = max(val1, val2)
        return width, height
    return 1080, 2400


def clean_raw_dataset(raw_path: Path) -> pd.DataFrame:
    """Load raw dataset, clean columns, engineer features, and assign target labels."""
    if not raw_path.exists():
        fallback = PROJECT_ROOT / "smartphone_cleaned_v5.csv"
        if fallback.exists():
            raw_path = fallback
        else:
            raise FileNotFoundError(f"Dataset not found at {raw_path}")

    df = pd.read_csv(raw_path)
    print(f"Loaded raw dataset with shape: {df.shape}")

    # 1. Target Label Creation
    def get_category_label(p):
        if p <= 15000:
            return 0  # Budget
        elif p <= 30000:
            return 1  # Mid-Range
        elif p <= 50000:
            return 2  # Premium
        else:
            return 3  # Flagship

    df['target_category_idx'] = df['price'].apply(get_category_label)
    df['target_category'] = df['target_category_idx'].map(CLASS_MAPPING)

    # 2. Boolean Conversion (0/1)
    bool_cols = ['has_5g', 'has_nfc', 'has_ir_blaster']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().map({'true': 1, '1': 1, 'false': 0, '0': 0}).fillna(0).astype(int)

    # 3. Categorical normalizations & rare grouping
    # Brands: keep top brands, group rare (< 6 occurrences)
    df['brand_name'] = df['brand_name'].astype(str).str.strip().str.lower()
    brand_counts = df['brand_name'].value_counts()
    frequent_brands = brand_counts[brand_counts >= 6].index.tolist()
    df['brand_grouped'] = df['brand_name'].apply(lambda x: x if x in frequent_brands else 'other_brand')

    # Processor Brands: normalize and group
    df['processor_brand'] = df['processor_brand'].astype(str).str.strip().str.lower()
    df['processor_brand'] = df['processor_brand'].replace({'nan': 'other_proc', '': 'other_proc', 'none': 'other_proc'})
    proc_counts = df['processor_brand'].value_counts()
    frequent_procs = proc_counts[proc_counts >= 5].index.tolist()
    df['processor_grouped'] = df['processor_brand'].apply(lambda x: x if x in frequent_procs else 'other_proc')

    # Operating System: normalize
    df['os'] = df['os'].astype(str).str.strip().str.lower()
    df['os'] = df['os'].replace({'nan': 'android', '': 'android', 'none': 'android'})
    df['os_grouped'] = df['os'].apply(lambda x: x if x in ['android', 'ios'] else 'other_os')

    # 4. Resolution parsing & geometric features
    res_parsed = df['resolution'].apply(parse_resolution)
    df['resolution_width'] = [r[0] for r in res_parsed]
    df['resolution_height'] = [r[1] for r in res_parsed]
    df['pixel_count'] = df['resolution_width'] * df['resolution_height']
    df['aspect_ratio'] = (df['resolution_height'] / df['resolution_width']).round(2)
    
    # PPI = sqrt(w^2 + h^2) / screen_size
    diagonal_pixels = np.sqrt(df['resolution_width']**2 + df['resolution_height']**2)
    df['ppi'] = (diagonal_pixels / df['screen_size'].clip(lower=3.0)).round(1)

    # 5. Domain Interaction Features
    df['num_front_cameras'] = df['num_front_cameras'].fillna(1.0)
    df['total_cameras'] = df['num_rear_cameras'] + df['num_front_cameras']
    
    # Battery capacity per screen inch
    df['screen_to_battery_ratio'] = (df['battery_capacity'].fillna(5000.0) / df['screen_size'].clip(lower=3.0)).round(1)
    
    # RAM to Storage ratio
    df['ram_to_storage_ratio'] = (df['ram_capacity'] / df['internal_memory'].clip(lower=8.0)).round(4)

    # Performance Score: cores * speed * ram
    proc_speed_imputed = df['processor_speed'].fillna(df['processor_speed'].median())
    cores_imputed = df['num_cores'].fillna(8.0)
    df['performance_score'] = (cores_imputed * proc_speed_imputed * df['ram_capacity']).round(2)

    return df


def build_preprocessor_pipeline(numerical_cols: list[str], categorical_cols: list[str]) -> ColumnTransformer:
    """Constructs scikit-learn ColumnTransformer with median imputation, standard scaling, and one-hot encoding."""
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, numerical_cols),
            ('cat', cat_pipeline, categorical_cols)
        ],
        remainder='drop'
    )

    return preprocessor


def main():
    print("=" * 80)
    print(" SmartPrice - Phase 3: Data Preprocessing & Pipeline Construction")
    print("=" * 80)

    # Clean & engineer features
    df = clean_raw_dataset(RAW_DATA_PATH)

    # Define feature subsets (excluding target 'price', 'target_category', 'model')
    numerical_features = [
        'rating', 'num_cores', 'processor_speed', 'battery_capacity',
        'fast_charging_available', 'fast_charging', 'ram_capacity', 'internal_memory',
        'screen_size', 'refresh_rate', 'num_rear_cameras', 'num_front_cameras',
        'primary_camera_rear', 'primary_camera_front', 'extended_memory_available',
        'extended_upto', 'has_5g', 'has_nfc', 'has_ir_blaster',
        'resolution_width', 'resolution_height', 'pixel_count', 'aspect_ratio',
        'ppi', 'total_cameras', 'screen_to_battery_ratio', 'ram_to_storage_ratio',
        'performance_score'
    ]

    categorical_features = ['brand_grouped', 'processor_grouped', 'os_grouped']

    all_features = numerical_features + categorical_features
    X = df[all_features].copy()
    y = df['target_category_idx'].copy()

    print(f"\nFeature Matrix X Shape: {X.shape} ({len(numerical_features)} numerical, {len(categorical_features)} categorical)")
    print(f"Target Vector y Shape:   {y.shape} (4 classes: Budget, Mid-Range, Premium, Flagship)")

    # Stratified 80/20 Train-Test Split (strictly random_state=42)
    X_train_df, X_test_df, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"\n[Split] Train Set: {X_train_df.shape[0]} samples (80%)")
    print(f"[Split] Test Set:  {X_test_df.shape[0]} samples (20%)")
    print("Train Class Counts:", pd.Series(y_train).value_counts().to_dict())
    print("Test Class Counts: ", pd.Series(y_test).value_counts().to_dict())

    # Build and fit preprocessing pipeline strictly on X_train (Zero Data Leakage)
    preprocessor = build_preprocessor_pipeline(numerical_features, categorical_features)
    
    print("\nFitting preprocessing pipeline on Training set...")
    X_train_trans = preprocessor.fit_transform(X_train_df)
    X_test_trans = preprocessor.transform(X_test_df)

    # Extract transformed feature names
    cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
    cat_feature_names = cat_encoder.get_feature_names_out(categorical_features).tolist()
    transformed_feature_names = numerical_features + cat_feature_names

    print(f"Transformed Features Count: {len(transformed_feature_names)} features")
    print(f"X_train Transformed Shape:  {X_train_trans.shape}")
    print(f"X_test Transformed Shape:   {X_test_trans.shape}")

    # Save artifacts
    # 1. Cleaned and enriched dataset
    cleaned_csv_path = PROCESSED_DATA_DIR / "smartphones_cleaned.csv"
    df.to_csv(cleaned_csv_path, index=False)
    print(f"\n[OK] Enriched dataset saved to: {cleaned_csv_path}")

    # 2. Raw train/test splits (for reference / tabulations)
    train_df = X_train_df.copy()
    train_df['target_category_idx'] = y_train
    train_df['target_category'] = train_df['target_category_idx'].map(CLASS_MAPPING)
    train_df.to_csv(PROCESSED_DATA_DIR / "train.csv", index=False)

    test_df = X_test_df.copy()
    test_df['target_category_idx'] = y_test
    test_df['target_category'] = test_df['target_category_idx'].map(CLASS_MAPPING)
    test_df.to_csv(PROCESSED_DATA_DIR / "test.csv", index=False)

    # 3. Transformed NumPy arrays
    np.save(PROCESSED_DATA_DIR / "X_train.npy", X_train_trans)
    np.save(PROCESSED_DATA_DIR / "X_test.npy", X_test_trans)
    np.save(PROCESSED_DATA_DIR / "y_train.npy", y_train.to_numpy())
    np.save(PROCESSED_DATA_DIR / "y_test.npy", y_test.to_numpy())
    print("[OK] Transformed NumPy arrays (X_train, X_test, y_train, y_test) saved.")

    # 4. Scikit-learn Pipeline Model
    preprocessor_path = MODEL_DIR / "preprocessor.joblib"
    joblib.dump({
        "pipeline": preprocessor,
        "numerical_features": numerical_features,
        "categorical_features": categorical_features,
        "transformed_feature_names": transformed_feature_names,
        "class_mapping": CLASS_MAPPING,
        "reverse_class_mapping": REVERSE_CLASS_MAPPING,
        "random_state": 42
    }, preprocessor_path)
    print(f"[OK] Preprocessor Pipeline saved to: {preprocessor_path}")

    # 5. Preprocessing Summary Report
    report = {
        "raw_samples": len(df),
        "train_samples": len(X_train_df),
        "test_samples": len(X_test_df),
        "split_ratio": "80/20 Stratified",
        "random_state": 42,
        "total_input_features": len(all_features),
        "numerical_features_count": len(numerical_features),
        "categorical_features_count": len(categorical_features),
        "transformed_features_count": len(transformed_feature_names),
        "classes": CLASS_MAPPING,
        "train_distribution": {CLASS_MAPPING[k]: int(v) for k, v in pd.Series(y_train).value_counts().items()},
        "test_distribution": {CLASS_MAPPING[k]: int(v) for k, v in pd.Series(y_test).value_counts().items()},
        "transformed_feature_list": transformed_feature_names
    }

    report_json_path = OUTPUT_DIR / "03_preprocessing_report.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"[OK] Preprocessing Report saved to: {report_json_path}")

    # 6. Markdown Summary
    report_md_path = OUTPUT_DIR / "03_preprocessing_summary.md"
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("# SmartPrice — Phase 3: Data Preprocessing & Pipeline Summary\n\n")
        f.write("## 1. Dataset Partitioning (Zero Data Leakage Protocol)\n\n")
        f.write("| Partition | Sample Count | Percentage | Stratification Strategy |\n")
        f.write("|---|---|---|---|\n")
        f.write(f"| **Training Set (`X_train`)** | {len(X_train_df)} | 80.0% | Stratified by Price Category (`random_state=42`) |\n")
        f.write(f"| **Testing Set (`X_test`)** | {len(X_test_df)} | 20.0% | Stratified by Price Category (`random_state=42`) |\n")
        f.write(f"| **Total Records** | **{len(df)}** | **100.0%** | |\n\n")

        f.write("## 2. Target Class Representation\n\n")
        f.write("| Class Index | Category Name | Price Boundary (INR) | Train Count | Test Count | Total Count |\n")
        f.write("|---|---|---|---|---|---|\n")
        for idx in range(4):
            c_name = CLASS_MAPPING[idx]
            tr_cnt = int(pd.Series(y_train).value_counts().get(idx, 0))
            te_cnt = int(pd.Series(y_test).value_counts().get(idx, 0))
            ranges = ["<= ₹15,000", "₹15,001 - ₹30,000", "₹30,001 - ₹50,000", "> ₹50,000"]
            f.write(f"| `{idx}` | **{c_name}** | {ranges[idx]} | {tr_cnt} | {te_cnt} | {tr_cnt + te_cnt} |\n")
        f.write("\n")

        f.write("## 3. Feature Engineering & Column Transformations\n\n")
        f.write("### A. Engineered Domain Features (8 new features):\n")
        f.write("1. `resolution_width` & `resolution_height`: Cleaned integer dimensions parsed from raw string.\n")
        f.write("2. `pixel_count`: Total screen resolution pixels ($W \\times H$).\n")
        f.write("3. `aspect_ratio`: Screen height-to-width ratio ($H / W$).\n")
        f.write("4. `ppi`: Screen Pixel Density ($\\frac{\\sqrt{W^2 + H^2}}{\\text{Screen Size}}$).\n")
        f.write("5. `total_cameras`: Sum of rear and front physical camera sensors.\n")
        f.write("6. `screen_to_battery_ratio`: Battery capacity per inch of screen display.\n")
        f.write("7. `ram_to_storage_ratio`: RAM capacity divided by internal storage capacity.\n")
        f.write("8. `performance_score`: Hardware synergy index ($\\text{Cores} \\times \\text{Speed} \\times \\text{RAM}$).\n\n")

        f.write("### B. Preprocessing Pipeline Architecture:\n")
        f.write("- **Numerical Pipeline (28 features):** `SimpleImputer(strategy='median')` -> `StandardScaler()`\n")
        f.write("- **Categorical Pipeline (3 grouped features):** `SimpleImputer(strategy='most_frequent')` -> `OneHotEncoder(handle_unknown='ignore')`\n")
        f.write(f"- **Total Post-Transformation Dimension:** **{len(transformed_feature_names)} features**.\n\n")

        f.write("## 4. Verification Checkpoints\n\n")
        f.write("- [x] `price` target column strictly removed from `X` to eliminate target leakage.\n")
        f.write("- [x] Pipeline fitted exclusively on `X_train` with no test set information leakage.\n")
        f.write("- [x] Preprocessor pipeline serialized to `ml/models/preprocessor.joblib`.\n")
        f.write("- [x] NumPy arrays `X_train.npy`, `X_test.npy`, `y_train.npy`, `y_test.npy` ready for model training.\n")

    print(f"[OK] Preprocessing Markdown Summary saved to: {report_md_path}")
    print("=" * 80)
    print(" Phase 3: Data Preprocessing & Pipeline Construction COMPLETED.")
    print("=" * 80)


if __name__ == "__main__":
    main()
