# SmartPrice — Phase 6: Detailed Evaluation, ROC/PR Curves & Error Analysis

## 1. Multi-Class ROC-AUC Summary (One-vs-Rest)

| Model Name | Macro ROC-AUC | Micro ROC-AUC | Budget AUC | Mid-Range AUC | Premium AUC | Flagship AUC |
|---|---|---|---|---|---|---|
| **Random Forest (Champion)** | **0.9627** | 0.9672 | 0.9847 | 0.9484 | 0.9240 | 0.9882 |
| **Support Vector Machine** | **0.9612** | 0.9632 | 0.9840 | 0.9329 | 0.9358 | 0.9836 |
| **K-Nearest Neighbors** | **0.9531** | 0.9583 | 0.9681 | 0.9318 | 0.9220 | 0.9851 |
| **Logistic Regression** | **0.9470** | 0.9512 | 0.9766 | 0.9133 | 0.9158 | 0.9748 |

## 2. 5-Fold Stratified Cross-Validation Stability Analysis

| Model Name | Mean CV Accuracy (%) | Std Dev (%) | Mean CV Macro F1 (%) | Std Dev (%) |
|---|---|---|---|---|
| **Random Forest (Champion)** | **80.36%** | ±1.02% | **78.06%** | ±1.61% |
| **Support Vector Machine** | **78.44%** | ±2.70% | **75.28%** | ±3.86% |
| **K-Nearest Neighbors** | **78.06%** | ±1.07% | **74.68%** | ±1.92% |
| **Logistic Regression** | **76.91%** | ±4.22% | **74.22%** | ±5.24% |

## 3. Champion Model Error & Boundary Analysis

- **Total Test Samples:** 196
- **Misclassifications:** 34 (Error Rate: 17.35%)
- **Adjacent Tier Confusions:** **100.0%** of all errors occurred between contiguous tiers (e.g. Mid-Range vs. Premium boundary), confirming that the model learns the continuous price ordering rather than random guesses.
- **Extreme Tier Errors (Budget <-> Flagship):** **0%**.

## 4. Generated Artifacts in Phase 6

1. `05_multiclass_roc_curves.png`: 4-panel ROC curve grid with micro, macro, and individual class AUCs.
2. `06_precision_recall_curves.png`: 4-panel PR curve grid with Average Precision.
3. `07_cv_scores_distribution.png`: 5-fold CV accuracy and F1 score spread boxplots.
4. `08_error_analysis_breakdown.png`: Misclassification transition distribution.
5. `06_evaluation_and_curves_data.json`: Interactive chart coordinate datasets for frontend dashboard.
