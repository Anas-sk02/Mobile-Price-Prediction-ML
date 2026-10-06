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

## 📊 Phase 1 Status: Completed
- [x] Dataset structure audit & validation
- [x] Data quality & missing value reporting
- [x] Target price categorization verification
