# SmartPrice — Phase 4: Baseline Models Benchmarking Summary

## 1. Multi-Model Benchmark Comparison (4 Core Models)

| Model Name | Train Acc (%) | Test Acc (%) | 5-Fold CV Acc (%) | Macro F1 (%) | Weighted F1 (%) | Macro ROC-AUC |
|---|---|---|---|---|---|---|
| **Logistic Regression** | 84.57% | **79.08%** | 76.40 ± 2.81% | 76.30% | 78.98% | 0.9458 |
| **K-Nearest Neighbors** | 83.29% | **78.57%** | 74.23 ± 2.47% | 76.62% | 78.48% | 0.9293 |
| **Random Forest** | 100.00% | **82.65%** | 79.08 ± 0.70% | 79.64% | 82.42% | 0.9621 |
| **Support Vector Machine (RBF)** | 85.71% | **79.08%** | 76.65 ± 2.54% | 75.64% | 78.91% | 0.9513 |

## 2. Class-Wise Performance Breakdown (Test Set)

### Logistic Regression
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.9286 | 0.7761 | 0.8455 | 67 |
| **Mid-Range** | 0.7595 | 0.8571 | 0.8054 | 70 |
| **Premium** | 0.6818 | 0.5556 | 0.6122 | 27 |
| **Flagship** | 0.7179 | 0.8750 | 0.7887 | 32 |
| *Macro Avg* | 0.7720 | 0.7660 | 0.7630 | 196 |
| *Weighted Avg* | 0.7998 | 0.7908 | 0.7898 | 196 |

### K-Nearest Neighbors
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.8750 | 0.8358 | 0.8550 | 67 |
| **Mid-Range** | 0.7432 | 0.7857 | 0.7639 | 70 |
| **Premium** | 0.6957 | 0.5926 | 0.6400 | 27 |
| **Flagship** | 0.7714 | 0.8438 | 0.8060 | 32 |
| *Macro Avg* | 0.7713 | 0.7645 | 0.7662 | 196 |
| *Weighted Avg* | 0.7863 | 0.7857 | 0.7848 | 196 |

### Random Forest
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.9643 | 0.8060 | 0.8780 | 67 |
| **Mid-Range** | 0.7805 | 0.9143 | 0.8421 | 70 |
| **Premium** | 0.7143 | 0.5556 | 0.6250 | 27 |
| **Flagship** | 0.7838 | 0.9062 | 0.8406 | 32 |
| *Macro Avg* | 0.8107 | 0.7955 | 0.7964 | 196 |
| *Weighted Avg* | 0.8347 | 0.8265 | 0.8242 | 196 |

### Support Vector Machine (RBF)
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.9153 | 0.8060 | 0.8571 | 67 |
| **Mid-Range** | 0.7763 | 0.8429 | 0.8082 | 70 |
| **Premium** | 0.6364 | 0.5185 | 0.5714 | 27 |
| **Flagship** | 0.7179 | 0.8750 | 0.7887 | 32 |
| *Macro Avg* | 0.7615 | 0.7606 | 0.7564 | 196 |
| *Weighted Avg* | 0.7950 | 0.7908 | 0.7891 | 196 |

## 3. Key Observations

- **Leading Baseline Model:** Random Forest achieves the highest initial test accuracy and Macro F1, demonstrating exceptional non-linear boundary partition capabilities across hardware feature interactions.
- **Linear vs Non-Linear Performance:** Logistic Regression and SVM (RBF) perform robustly with high CV scores, validating the effectiveness of standard scaling and one-hot encodings.
- **Next Step:** Hyperparameter tuning (Phase 5/6) will optimize regularization ($C$), tree depth / estimators, and kernel parameters to further boost generalization.
