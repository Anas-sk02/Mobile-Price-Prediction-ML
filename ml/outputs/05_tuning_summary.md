# SmartPrice — Phase 5: Hyperparameter Tuning & Grid Search Report

## 1. Champion Model: **Random Forest** 🏆

- **Optimal Parameters:** `{'max_depth': 15, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 300}`
- **Test Accuracy:** **82.65%**
- **Macro F1-Score:** **79.96%**
- **Multi-Class ROC-AUC (OvR):** **0.9613**

## 2. Baseline vs. Tuned Performance Benchmark

| Model Name | Baseline Acc (%) | Tuned Acc (%) | Baseline F1 (%) | Tuned F1 (%) | Tuned ROC-AUC | Optimal Hyperparameters |
|---|---|---|---|---|---|---|
| **Logistic Regression** | 79.08% | **78.57%** | 76.30% | **76.39%** | 0.9451 | `{'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'}` |
| **K-Nearest Neighbors** | 78.57% | **79.59%** | 76.62% | **76.38%** | 0.9517 | `{'metric': 'manhattan', 'n_neighbors': 19, 'weights': 'distance'}` |
| **Random Forest** | 82.65% | **82.65%** | 79.64% | **79.96%** | 0.9613 | `{'max_depth': 15, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 300}` |
| **Support Vector Machine** | 79.08% | **80.10%** | 75.64% | **78.07%** | 0.9591 | `{'C': 5.0, 'gamma': 'auto', 'kernel': 'rbf'}` |

## 3. Tuned Class-Wise Classification Metrics

### Logistic Regression (Tuned)
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.9273 | 0.7612 | 0.8361 | 67 |
| **Mid-Range** | 0.7468 | 0.8429 | 0.7919 | 70 |
| **Premium** | 0.6667 | 0.5926 | 0.6275 | 27 |
| **Flagship** | 0.7368 | 0.8750 | 0.8000 | 32 |
| *Macro Avg* | 0.7694 | 0.7679 | 0.7639 | 196 |
| *Weighted Avg* | 0.7958 | 0.7857 | 0.7857 | 196 |

### K-Nearest Neighbors (Tuned)
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.8769 | 0.8507 | 0.8636 | 67 |
| **Mid-Range** | 0.8028 | 0.8143 | 0.8085 | 70 |
| **Premium** | 0.6000 | 0.5556 | 0.5769 | 27 |
| **Flagship** | 0.7714 | 0.8438 | 0.8060 | 32 |
| *Macro Avg* | 0.7628 | 0.7661 | 0.7638 | 196 |
| *Weighted Avg* | 0.7951 | 0.7959 | 0.7950 | 196 |

### Random Forest (Tuned)
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.9474 | 0.8060 | 0.8710 | 67 |
| **Mid-Range** | 0.7711 | 0.9143 | 0.8366 | 70 |
| **Premium** | 0.7143 | 0.5556 | 0.6250 | 27 |
| **Flagship** | 0.8286 | 0.9062 | 0.8657 | 32 |
| *Macro Avg* | 0.8153 | 0.7955 | 0.7996 | 196 |
| *Weighted Avg* | 0.8329 | 0.8265 | 0.8239 | 196 |

### Support Vector Machine (Tuned)
| Category | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Budget** | 0.9310 | 0.8060 | 0.8640 | 67 |
| **Mid-Range** | 0.7600 | 0.8143 | 0.7862 | 70 |
| **Premium** | 0.6667 | 0.5926 | 0.6275 | 27 |
| **Flagship** | 0.7692 | 0.9375 | 0.8451 | 32 |
| *Macro Avg* | 0.7817 | 0.7876 | 0.7807 | 196 |
| *Weighted Avg* | 0.8071 | 0.8010 | 0.8005 | 196 |

