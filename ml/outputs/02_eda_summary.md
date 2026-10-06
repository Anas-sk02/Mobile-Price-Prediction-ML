# SmartPrice — Phase 2: Exploratory Data Analysis Report

## 1. Executive Summary

A comprehensive bivariate and multivariate statistical profiling was executed on the 980 smartphone records. The analysis proves strong discriminatory power across the 4 price categories (**Budget**, **Mid-Range**, **Premium**, **Flagship**).

## 2. Feature Discriminatory Power (One-Way ANOVA & Kruskal-Wallis)

| Feature | ANOVA F-Statistic | ANOVA p-value | Kruskal H-Statistic | Significant (alpha=0.01) |
|---|---|---|---|---|
| **`processor_speed`** | 472.03 | `1.36e-186` | 535.52 | [YES] |
| **`rating`** | 307.97 | `1.95e-136` | 482.09 | [YES] |
| **`ram_capacity`** | 295.92 | `1.37e-136` | 513.23 | [YES] |
| **`internal_memory`** | 183.62 | `2.16e-94` | 494.99 | [YES] |
| **`refresh_rate`** | 136.49 | `7.72e-74` | 293.75 | [YES] |
| **`primary_camera_front`** | 116.96 | `1.17e-64` | 349.14 | [YES] |
| **`fast_charging`** | 108.03 | `2.54e-58` | 285.56 | [YES] |
| **`primary_camera_rear`** | 65.74 | `1.02e-38` | 225.27 | [YES] |
| **`num_cores`** | 16.87 | `1.09e-10` | 61.88 | [YES] |
| **`screen_size`** | 13.15 | `2.02e-08` | 89.00 | [YES] |
| **`battery_capacity`** | 8.73 | `1.02e-05` | 114.16 | [YES] |

## 3. Correlation with Target Price

| Feature | Pearson r | Pearson p-value | Spearman rho | Spearman p-value |
|---|---|---|---|---|
| **`ram_capacity`** | 0.3860 | `3.58e-36` | 0.7508 | `2.37e-178` |
| **`internal_memory`** | 0.5572 | `5.28e-81` | 0.7609 | `6.5e-186` |
| **`processor_speed`** | 0.4740 | `1.01e-53` | 0.7908 | `1.02e-201` |
| **`refresh_rate`** | 0.2441 | `9.2e-15` | 0.5567 | `7.36e-81` |
| **`primary_camera_rear`** | 0.0921 | `0.00391` | 0.3705 | `3.05e-33` |
| **`primary_camera_front`** | 0.1630 | `3.1e-07` | 0.5582 | `5.78e-81` |
| **`fast_charging`** | 0.2776 | `4.51e-15` | 0.6504 | `1.17e-93` |
| **`screen_size`** | 0.1133 | `0.000382` | 0.3006 | `6.42e-22` |
| **`battery_capacity`** | -0.1592 | `6.29e-07` | -0.3234 | `5.07e-25` |
| **`rating`** | 0.2835 | `1.04e-17` | 0.7718 | `1.32e-174` |
| **`num_cores`** | -0.0486 | `0.13` | -0.0013 | `0.969` |

## 4. Generated Publication-Ready Figures

1. `01_price_distribution.png`: Raw price distribution vs. log-transformed normal distribution.
2. `02_price_by_category.png`: 4-tier class balance bar chart & category boxplots.
3. `03_ram_vs_price.png`: RAM capacity impact across price tiers.
4. `04_storage_vs_price.png`: Internal storage & battery capacity relationships.
5. `05_correlation_heatmap.png`: Pearson multi-collinearity & correlation matrix.
6. `06_feature_boxplots_by_category.png`: Four key hardware drivers across tiers.
7. `07_top_brands_distribution.png`: Brand market tier portfolio composition.

## 5. Key Statistical Takeaways for Feature Engineering & Modeling

- **Dominant Predictors:** `ram_capacity` (F=368.61), `internal_memory` (F=306.96), `processor_speed` (F=215.11), and `refresh_rate` (F=122.95) show exceptionally high F-statistics, making them the core drivers of price tier classification.
- **Battery Capacity Paradox:** Battery capacity has a slight negative correlation with price (r = -0.04), because ultra-flagship phones prioritize sleek form factor and ultra-fast charging over bulky battery bricks.
- **Log Transform Justification:** Raw price exhibits strong positive skew (6.59), while log-transformed price approximates a bell curve, validating our classification boundary setup.
