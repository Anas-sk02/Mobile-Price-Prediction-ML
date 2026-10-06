# SmartPrice — Phase 1: Dataset Inspection Summary

- **Dataset File**: `smartphone_cleaned_v5.csv`
- **Total Records**: 980
- **Total Features**: 25
- **Exact Duplicates**: 0
- **Memory Usage**: 490.24 KB

## 1. Target Variable (Price) Distribution

| Metric | Value (INR) |
|---|---|
| Min Price | ₹3,499 |
| 25th Percentile | ₹12,999 |
| Median Price | ₹19,994 |
| 75th Percentile | ₹35,492 |
| Max Price | ₹650,000 |
| Mean Price | ₹32,520.50 |
| Standard Deviation | ₹39,531.81 |
| Skewness | 6.59 |

## 2. Target Category Class Breakdown

| Category | Price Range (INR) | Count | Percentage |
|---|---|---|---|
| **Budget** | <= Rs. 15,000 | 337 | 34.39% |
| **Mid-Range** | Rs. 15,001 - 30,000 | 349 | 35.61% |
| **Premium** | Rs. 30,001 - 50,000 | 133 | 13.57% |
| **Flagship** | > Rs. 50,000 | 161 | 16.43% |
| **Total** | | **980** | **100.0%** |

## 3. Column Data Types & Missing Values

| Col # | Column Name | Dtype | Missing Count | Missing % |
|---|---|---|---|---|
| 1 | `brand_name` | `object` | 0 | 0.0% |
| 2 | `model` | `object` | 0 | 0.0% |
| 3 | `price` | `int64` | 0 | 0.0% |
| 4 | `rating` | `float64` | 101 | 10.31% |
| 5 | `has_5g` | `bool` | 0 | 0.0% |
| 6 | `has_nfc` | `bool` | 0 | 0.0% |
| 7 | `has_ir_blaster` | `bool` | 0 | 0.0% |
| 8 | `processor_brand` | `object` | 20 | 2.04% |
| 9 | `num_cores` | `float64` | 6 | 0.61% |
| 10 | `processor_speed` | `float64` | 42 | 4.29% |
| 11 | `battery_capacity` | `float64` | 11 | 1.12% |
| 12 | `fast_charging_available` | `int64` | 0 | 0.0% |
| 13 | `fast_charging` | `float64` | 211 | 21.53% |
| 14 | `ram_capacity` | `float64` | 0 | 0.0% |
| 15 | `internal_memory` | `float64` | 0 | 0.0% |
| 16 | `screen_size` | `float64` | 0 | 0.0% |
| 17 | `refresh_rate` | `int64` | 0 | 0.0% |
| 18 | `resolution` | `object` | 0 | 0.0% |
| 19 | `num_rear_cameras` | `int64` | 0 | 0.0% |
| 20 | `num_front_cameras` | `float64` | 4 | 0.41% |
| 21 | `os` | `object` | 14 | 1.43% |
| 22 | `primary_camera_rear` | `float64` | 0 | 0.0% |
| 23 | `primary_camera_front` | `float64` | 5 | 0.51% |
| 24 | `extended_memory_available` | `int64` | 0 | 0.0% |
| 25 | `extended_upto` | `float64` | 480 | 48.98% |

## 4. Key Data Quality Findings & Remediation Plan

### 1. String Boolean Values
- **Affected Columns**: `has_5g`, `has_nfc`, `has_ir_blaster`
- **Finding**: Values stored as string 'True' / 'False' rather than native boolean or 0/1 integers.
- **Action Required**: Convert to integer boolean (1/0) during preprocessing.

### 2. Composite String Format in Resolution
- **Affected Columns**: `resolution`
- **Finding**: Stored as 'width x height' strings (e.g. '1080 x 2400').
- **Action Required**: Parse into resolution_width and resolution_height numerical features.

### 3. Missing Values in Hardware Specs
- **Affected Columns**: `rating`, `processor_brand`, `processor_speed`, `fast_charging`, `num_front_cameras`, `os`, `primary_camera_front`, `extended_upto`
- **Finding**: Missing values present in multiple columns requiring principled imputation (median for numerical, mode / 'Unknown' for categorical).
- **Action Required**: Median imputation for numerical specs; domain fallback/mode for categorical attributes.

### 4. Target Leakage Prevention
- **Affected Columns**: `price`
- **Finding**: Continuous price column is used exclusively to generate the categorical target variable (price_category) and MUST be dropped from model input features.
- **Action Required**: Drop 'price' and 'model' from feature matrix X before training.

## 5. Phase 1 Verification Status

- [x] Raw data verified in `data/raw/smartphone_cleaned_v5.csv`
- [x] Data structure, data types, and missingness audited
- [x] Target price distribution and 4-tier class categorization validated
- [x] Data quality issues documented with remediation steps
- [x] Inspection report generated (`01_inspection_report.json` and `01_inspection_summary.md`)
