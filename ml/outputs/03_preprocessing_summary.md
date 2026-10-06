# SmartPrice — Phase 3: Data Preprocessing & Pipeline Summary

## 1. Dataset Partitioning (Zero Data Leakage Protocol)

| Partition | Sample Count | Percentage | Stratification Strategy |
|---|---|---|---|
| **Training Set (`X_train`)** | 784 | 80.0% | Stratified by Price Category (`random_state=42`) |
| **Testing Set (`X_test`)** | 196 | 20.0% | Stratified by Price Category (`random_state=42`) |
| **Total Records** | **980** | **100.0%** | |

## 2. Target Class Representation

| Class Index | Category Name | Price Boundary (INR) | Train Count | Test Count | Total Count |
|---|---|---|---|---|---|
| `0` | **Budget** | <= ₹15,000 | 270 | 67 | 337 |
| `1` | **Mid-Range** | ₹15,001 - ₹30,000 | 279 | 70 | 349 |
| `2` | **Premium** | ₹30,001 - ₹50,000 | 106 | 27 | 133 |
| `3` | **Flagship** | > ₹50,000 | 129 | 32 | 161 |

## 3. Feature Engineering & Column Transformations

### A. Engineered Domain Features (8 new features):
1. `resolution_width` & `resolution_height`: Cleaned integer dimensions parsed from raw string.
2. `pixel_count`: Total screen resolution pixels ($W \times H$).
3. `aspect_ratio`: Screen height-to-width ratio ($H / W$).
4. `ppi`: Screen Pixel Density ($\frac{\sqrt{W^2 + H^2}}{\text{Screen Size}}$).
5. `total_cameras`: Sum of rear and front physical camera sensors.
6. `screen_to_battery_ratio`: Battery capacity per inch of screen display.
7. `ram_to_storage_ratio`: RAM capacity divided by internal storage capacity.
8. `performance_score`: Hardware synergy index ($\text{Cores} \times \text{Speed} \times \text{RAM}$).

### B. Preprocessing Pipeline Architecture:
- **Numerical Pipeline (28 features):** `SimpleImputer(strategy='median')` -> `StandardScaler()`
- **Categorical Pipeline (3 grouped features):** `SimpleImputer(strategy='most_frequent')` -> `OneHotEncoder(handle_unknown='ignore')`
- **Total Post-Transformation Dimension:** **62 features**.

## 4. Verification Checkpoints

- [x] `price` target column strictly removed from `X` to eliminate target leakage.
- [x] Pipeline fitted exclusively on `X_train` with no test set information leakage.
- [x] Preprocessor pipeline serialized to `ml/models/preprocessor.joblib`.
- [x] NumPy arrays `X_train.npy`, `X_test.npy`, `y_train.npy`, `y_test.npy` ready for model training.
