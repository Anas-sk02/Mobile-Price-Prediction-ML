# SmartPrice — Phase 7: Feature Importance & Model Explainability Report

## 1. Top 10 Most Influential Features (Permutation Importance on Test Set)

| Rank | Feature Name | Domain Group | Permutation Mean ($\Delta$ Macro F1) | MDI Gini Importance |
|:---:|---|---|:---:|:---:|
| 1 | **`performance_score`** | Core Hardware & Processor | **0.0369** $\pm$ 0.0175 | 0.0956 |
| 2 | **`processor_speed`** | Core Hardware & Processor | **0.0298** $\pm$ 0.0142 | 0.0533 |
| 3 | **`ram_capacity`** | Core Hardware & Processor | **0.0242** $\pm$ 0.0115 | 0.0498 |
| 4 | **`rating`** | Other / Miscellaneous | **0.0242** $\pm$ 0.0093 | 0.0793 |
| 5 | **`primary_camera_front`** | Camera Systems | **0.0189** $\pm$ 0.0092 | 0.0394 |
| 6 | **`has_nfc`** | Connectivity & Expansion | **0.0162** $\pm$ 0.0087 | 0.0315 |
| 7 | **`internal_memory`** | Core Hardware & Processor | **0.0158** $\pm$ 0.0074 | 0.0432 |
| 8 | **`ppi`** | Display & Visuals | **0.0147** $\pm$ 0.0047 | 0.0561 |
| 9 | **`processor_grouped_helio`** | Core Hardware & Processor | **0.0142** $\pm$ 0.0056 | 0.0066 |
| 10 | **`refresh_rate`** | Display & Visuals | **0.0136** $\pm$ 0.0080 | 0.0224 |

## 2. Hardware Domain Group Contributions

| Functional Group | Cumulative Tree Importance (%) |
|---|:---:|
| **Core Hardware & Processor** | **29.64%** |
| **Display & Visuals** | **27.78%** |
| **Battery & Power** | **9.54%** |
| **Camera Systems** | **9.28%** |
| **Connectivity & Expansion** | **9.08%** |
| **Other / Miscellaneous** | **7.93%** |
| **Brand & Operating System** | **6.75%** |

## 3. Directional Influence (Logistic Regression Weights)

- **Budget Drivers:** Higher `ram_capacity`, `performance_score`, and `refresh_rate` strongly decrease the odds of a device being in the Budget class (large negative weights).
- **Flagship Drivers:** High `processor_speed`, `internal_memory` (>= 256GB), `refresh_rate` (120Hz+), and Apple/Samsung ecosystem indicators exhibit large positive coefficients for the Flagship category.
- **Mid-Range / Premium Boundary:** `fast_charging` (W) and `primary_camera_rear` (50-200MP) are the primary discriminators pushing phones from Mid-Range into Premium.

## 4. Generated Artifacts in Phase 7

1. `09_random_forest_feature_importance.png`: Dual comparison of Permutation vs. MDI Gini importance.
2. `10_logistic_regression_coefficients.png`: Directional log-odds coefficients heatmap across all 4 tiers.
3. `11_feature_importance_by_group.png`: Donut chart of aggregate domain hardware contributions.
4. `07_feature_importance.json`: Full ranking and weights payload for API/UI explainability components.
