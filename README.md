# SmartPrice — Smartphone Price Category Prediction & ML Model Benchmarking System

An end-to-end Machine Learning system for predicting smartphone price categories and benchmarking 4 classification models (**Logistic Regression**, **K-Nearest Neighbors**, **Random Forest**, and **Support Vector Machine**).

---

## 📌 Project Overview

- **Problem Type:** Multi-Class Classification (4 Price Categories: *Budget*, *Mid-Range*, *Premium*, *Flagship*)
- **Dataset:** 980 smartphone records with 25 technical and hardware specifications
- **Models Evaluated:** Logistic Regression, KNN, Random Forest, SVM (No XGBoost)
- **Evaluation Metrics:** Accuracy, Precision, Recall, F1-Score (Macro & Weighted), ROC-AUC
- **Validation:** Stratified 5-Fold Cross-Validation & Hyperparameter Tuning

---

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Dataset Inspection (Phase 1)
```bash
python ml/src/01_inspect_dataset.py
```

---

## 📁 Repository Structure

```text
├── data/
│   ├── raw/
│   │   └── smartphone_cleaned_v5.csv
│   └── processed/
├── ml/
│   ├── src/
│   │   └── 01_inspect_dataset.py
│   ├── outputs/
│   │   ├── 01_inspection_report.json
│   │   └── 01_inspection_summary.md
│   └── models/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Phases Status
- [x] **Phase 1:** Dataset Inspection, Setup & Quality Audit
- [x] **Phase 2:** Exploratory Data Analysis & Statistical Profiling
- [x] **Phase 3:** Data Preprocessing, Imputation & Encoding
- [x] **Phase 4:** Baseline Model Training (4 Models: LR, KNN, RF, SVM)
- [x] **Phase 5:** Hyperparameter Tuning & Grid Search Optimization (Champion: Random Forest - 82.65% Acc, 0.9613 ROC-AUC)
- [x] **Phase 6:** Model Evaluation, Cross-Validation, ROC/PR Curves & Error Analysis
- [ ] **Phase 7:** Feature Importance & Explainability (SHAP / Tree MDI)
