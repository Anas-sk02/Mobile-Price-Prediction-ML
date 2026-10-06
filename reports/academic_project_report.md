# SmartPrice: Smartphone Price Category Prediction & Multi-Model Benchmarking System

**Academic Coursework & Laboratory Project Report**  
*Department of Computer Science & Engineering / Artificial Intelligence*

---

## Abstract

Smartphone pricing classification represents a complex multi-class non-linear supervised learning challenge driven by rapid hardware evolution, heterogeneous feature scales, and composite technical specifications. This paper presents **SmartPrice**, an end-to-end Machine Learning benchmarking and inference system developed to categorize smartphones into four domain-standard price tiers: **Budget** ($\le$ ₹15,000), **Mid-Range** (₹15,001 – ₹30,000), **Premium** (₹30,001 – ₹50,000), and **Flagship** (> ₹50,000). 

Using a real-world dataset of 980 smartphone records across 25 raw features, we design a strict zero-data-leakage pipeline incorporating domain interaction feature engineering (such as Screen Pixels Per Inch $PPI$, Hardware Performance Synergy Index, and Battery Density). We benchmark four supervised classification paradigms: **Multinomial Logistic Regression**, **K-Nearest Neighbors (KNN)**, **Random Forest Classifier**, and **Support Vector Machines (SVM with RBF Kernel)** under 5-fold stratified cross-validation and exhaustive hyperparameter grid search. The optimized **Random Forest Classifier** achieved the highest test accuracy (**82.65%**), macro F1-score (**79.96%**), and multi-class One-vs-Rest ROC-AUC (**0.9613**). Model explainability via model-agnostic Permutation Importance identified the engineered `performance_score` and `processor_speed` as the primary discriminative drivers. The system is deployed via a high-performance **FastAPI** backend and an enterprise-grade **React/TypeScript** interactive web dashboard.

**Keywords:** *Smartphone Price Prediction, Multi-Class Classification, Random Forest, Support Vector Machines, Feature Importance, Model Benchmarking, Zero-Leakage Pipeline, FastAPI.*

---

## 1. Introduction & Problem Statement

### 1.1 Motivation
Consumer electronics markets, particularly smartphones, exhibit high feature volatility. Consumers and retailers require automated, objective classification mechanisms to evaluate whether a device's hardware bill-of-materials justifies its market price tier.

### 1.2 Objectives
1. Perform rigorous Exploratory Data Analysis (EDA) and quality auditing on 980 smartphone records.
2. Build an automated, reproducible scikit-learn preprocessing pipeline ensuring zero target leakage.
3. Formulate and benchmark four fundamental classification algorithms:
   - Linear Baseline: Multinomial Logistic Regression
   - Instance-Based: K-Nearest Neighbors (KNN)
   - Ensemble Decision Trees: Random Forest Classifier
   - Kernel Methods: Support Vector Classifier (RBF Kernel)
4. Evaluate multi-class classification performance using Accuracy, Precision, Recall, Macro/Weighted F1-score, and One-vs-Rest (OvR) ROC-AUC curves.
5. Provide post-hoc explainability via Permutation Feature Importance and Gini Impurity (MDI).
6. Deliver a full-stack production application (FastAPI backend + React/TypeScript dashboard).

---

## 2. Dataset Description & Statistical Profiling

### 2.1 Raw Dataset Overview
The dataset contains **980 valid smartphone models** with **25 raw attributes** spanning hardware specifications, physical display dimensions, connectivity protocols, and market ratings.

| Attribute Name | Raw Dtype | Description |
|---|---|---|
| `brand_name` | Categorical | Smartphone manufacturer (Xiaomi, Samsung, Vivo, Apple, OnePlus, etc.) |
| `price` | Continuous (INR) | Retail price in Indian Rupees (Used strictly as target source) |
| `rating` | Continuous | Expert/reviewer benchmark score (60.0 – 89.0) |
| `has_5g`, `has_nfc`, `has_ir_blaster` | String/Boolean | Hardware connectivity features |
| `processor_brand` | Categorical | Qualcomm Snapdragon, MediaTek Dimensity/Helio, Apple Bionic, etc. |
| `num_cores`, `processor_speed` | Numerical | Number of CPU cores and peak clock speed in GHz |
| `battery_capacity`, `fast_charging` | Numerical | Battery capacity (mAh) and charging rate (Watts) |
| `ram_capacity`, `internal_memory` | Numerical | Primary RAM (GB) and internal flash storage (GB) |
| `screen_size`, `refresh_rate` | Numerical | Display diagonal size (inches) and refresh frequency (Hz) |
| `resolution` | String | Display pixel resolution format (e.g., `"1080 x 2400"`) |
| `num_rear_cameras`, `num_front_cameras` | Numerical | Physical sensor count |
| `primary_camera_rear`, `front` | Numerical | Primary camera megapixel resolutions |

### 2.2 Target Categorization Scheme
The continuous price distribution displays strong right-skewness ($\text{Skewness} = 6.59$). We discretize `price` into 4 industry-standard economic segments:

$$\text{Price Category} = \begin{cases} 
\text{Budget (0)} & \text{if } \text{Price} \le ₹15,000 \\
\text{Mid-Range (1)} & \text{if } ₹15,000 < \text{Price} \le ₹30,000 \\
\text{Premium (2)} & \text{if } ₹30,000 < \text{Price} \le ₹50,000 \\
\text{Flagship (3)} & \text{if } \text{Price} > ₹50,000 
\end{cases}$$

- **Budget:** 337 phones (34.4%) — Train: 270, Test: 67
- **Mid-Range:** 349 phones (35.6%) — Train: 279, Test: 70
- **Premium:** 133 phones (13.6%) — Train: 106, Test: 27
- **Flagship:** 161 phones (16.4%) — Train: 129, Test: 32

---

## 3. Data Preprocessing & Feature Engineering

### 3.1 Zero Data Leakage Protocol
To guarantee strict scientific validity:
1. The continuous `price` and string `model` identifiers were immediately isolated and removed from the feature matrix $X$.
2. An **80/20 Stratified Train-Test Split** (`random_state=42`) was performed before computing any transformation statistics.
3. Imputation medians, standard scaling means/variances, and one-hot categorical dictionaries were fitted **strictly on $X_{\text{train}}$** ($N=784$) and applied blindly to $X_{\text{test}}$ ($N=196$).

### 3.2 Domain Feature Engineering
Eight specialized interaction features were derived from first principles:
1. **Resolution Dimensions:** Parsed into integer width ($W$) and height ($H$).
2. **Total Pixels:** $\text{Pixel Count} = W \times H$.
3. **Aspect Ratio:** $\text{Aspect Ratio} = \frac{H}{W}$.
4. **Pixels Per Inch (PPI):**
   $$\text{PPI} = \frac{\sqrt{W^2 + H^2}}{\text{Screen Size (inches)}}$$
5. **Hardware Performance Synergy Index:**
   $$\text{Performance Score} = \text{Cores} \times \text{Clock Speed (GHz)} \times \text{RAM (GB)}$$
6. **Battery Density Index:** $\text{Battery per Inch} = \frac{\text{Battery Capacity (mAh)}}{\text{Screen Size (inches)}}$.
7. **Memory Balance Ratio:** $\text{RAM-to-Storage Ratio} = \frac{\text{RAM (GB)}}{\text{Internal Storage (GB)}}$.
8. **Total Sensor Count:** $\text{Total Cameras} = \text{Rear Cameras} + \text{Front Cameras}$.

### 3.3 Scikit-Learn Pipeline Architecture
- **Numerical Pipeline (28 features):** `SimpleImputer(strategy='median')` followed by `StandardScaler()`.
- **Categorical Pipeline (3 features):** `SimpleImputer(strategy='most_frequent')` followed by `OneHotEncoder(handle_unknown='ignore')`.
- **Post-Transformation Dimensionality:** **62 numerical features**.

---

## 4. Machine Learning Algorithms & Mathematical Formulation

### 4.1 Multinomial Logistic Regression
Multinomial logistic regression computes class probabilities using the softmax activation function:

$$P(Y = k \mid \mathbf{x}) = \frac{e^{\mathbf{w}_k^T \mathbf{x} + b_k}}{\sum_{j=0}^{K-1} e^{\mathbf{w}_j^T \mathbf{x} + b_j}}$$

Optimization minimizes the cross-entropy loss with $L_2$ regularization:

$$\mathcal{L}(\mathbf{w}) = -\sum_{i=1}^N \sum_{k=0}^{K-1} y_{ik} \ln P(Y = k \mid \mathbf{x}_i) + \frac{1}{2C} \sum_{k=0}^{K-1} \|\mathbf{w}_k\|_2^2$$

### 4.2 K-Nearest Neighbors (KNN)
KNN assigns labels based on the majority vote or distance-weighted votes of the $k$ closest training vectors under Manhattan distance:

$$d_1(\mathbf{x}, \mathbf{z}) = \sum_{j=1}^D |x_j - z_j|$$

The posterior probability weighting for distance mode is given by:

$$w_i = \frac{1}{d_1(\mathbf{x}, \mathbf{x}_i) + \epsilon}$$

### 4.3 Random Forest Classifier
An ensemble of $B$ decorrelated decision trees built using bootstrap aggregation (bagging) and random feature subspace selection. The ensemble prediction is:

$$\hat{y} = \arg\max_k \frac{1}{B} \sum_{b=1}^B I(T_b(\mathbf{x}) = k)$$

Node splitting minimizes Gini impurity:

$$\text{Gini}(m) = 1 - \sum_{k=0}^{K-1} p_{mk}^2$$

### 4.4 Support Vector Machine (SVM)
Multi-class classification uses One-vs-Rest (OvR) hyperplanes with a Radial Basis Function (RBF) kernel mapping inputs to infinite-dimensional Hilbert space:

$$K(\mathbf{x}, \mathbf{z}) = \exp\left(-\gamma \|\mathbf{x} - \mathbf{z}\|^2\right)$$

The dual optimization objective is:

$$\max_{\boldsymbol{\alpha}} \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i=1}^N \sum_{j=1}^N \alpha_i \alpha_j y_i y_j K(\mathbf{x}_i, \mathbf{x}_j) \quad \text{s.t.} \quad 0 \le \alpha_i \le C, \; \sum_{i=1}^N \alpha_i y_i = 0$$

Calibrated class probabilities are obtained via Platt scaling.

---

## 5. Experimental Results & Model Benchmarking

### 5.1 Hyperparameter Tuning Results
Hyperparameter tuning was conducted using **5-Fold Stratified GridSearchCV** (`scoring='f1_macro'`).

| Model Architecture | Optimal Hyperparameters | Best CV Macro F1 | Test Accuracy | Macro F1 | Weighted F1 | Macro ROC-AUC |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Random Forest (Champion)** 🏆 | `n_estimators=300, max_depth=15, max_features='log2', min_samples_split=2` | **78.06%** | **82.65%** | **79.96%** | **82.39%** | **0.9613** |
| **Support Vector Machine (SVM)** | `C=5.0, gamma='auto', kernel='rbf'` | **75.28%** | **80.10%** | **78.07%** | **80.05%** | **0.9591** |
| **K-Nearest Neighbors (KNN)** | `n_neighbors=19, weights='distance', metric='manhattan'` | **74.68%** | **79.59%** | **76.38%** | **79.50%** | **0.9517** |
| **Logistic Regression** | `C=5.0, solver='lbfgs'` | **74.22%** | **78.57%** | **76.39%** | **78.57%** | **0.9451** |

### 5.2 Per-Class Classification Performance (Champion Random Forest)
- **Budget Tier:** Precision = 0.887, Recall = 0.940, F1-Score = **0.913** (Support = 67)
- **Mid-Range Tier:** Precision = 0.771, Recall = 0.771, F1-Score = **0.771** (Support = 70)
- **Premium Tier:** Precision = 0.720, Recall = 0.667, F1-Score = **0.692** (Support = 27)
- **Flagship Tier:** Precision = 0.875, Recall = 0.875, F1-Score = **0.875** (Support = 32)

### 5.3 Error Analysis & Contiguous Boundary Confirmation
- **Total Test Samples:** 196 | **Total Misclassifications:** 34 (17.35% error rate)
- **Adjacent Tier Confusions:** **85.3%** of all errors occurred between adjacent classes (e.g. Mid-Range $\leftrightarrow$ Premium boundary).
- **Extreme Tier Confusions:** **0.0%** (no Budget device was ever confused for a Flagship).

---

## 6. Model Explainability & Feature Importance

### 6.1 Permutation Importance vs. Gini MDI
Permutation feature importance was evaluated across 15 iterations on the unseen test partition to measure the empirical loss in Macro F1 when each feature column is shuffled:

1. **`performance_score`** ($\Delta \text{Macro F1} = 0.0369 \pm 0.0175$) — *Top overall predictor*
2. **`processor_speed`** ($\Delta \text{Macro F1} = 0.0298 \pm 0.0142$)
3. **`ram_capacity`** ($\Delta \text{Macro F1} = 0.0242 \pm 0.0115$)
4. **`rating`** ($\Delta \text{Macro F1} = 0.0242 \pm 0.0093$)
5. **`primary_camera_front`** ($\Delta \text{Macro F1} = 0.0189 \pm 0.0092$)
6. **`has_nfc`** ($\Delta \text{Macro F1} = 0.0162 \pm 0.0087$)
7. **`internal_memory`** ($\Delta \text{Macro F1} = 0.0158 \pm 0.0074$)
8. **`ppi`** ($\Delta \text{Macro F1} = 0.0147 \pm 0.0047$)

### 6.2 Functional Hardware Group Contributions
- **Core Hardware & Processor:** **29.64%**
- **Display & Visuals:** **27.78%**
- **Battery & Charging:** **9.54%**
- **Camera Systems:** **9.28%**
- **Connectivity & Expansion:** **9.08%**
- **Brand & OS:** **6.75%**

---

## 7. Software Architecture & Deployment

### 7.1 Backend (FastAPI)
- **Framework:** FastAPI with Uvicorn ASGI server and Pydantic validation.
- **Endpoints:** 10 REST endpoints covering real-time inference (`/api/predict`), multi-model consensus (`/api/predict/compare`), batch prediction (`/api/predict/batch`), ROC curve points (`/api/models/roc-curves`), and dataset stats (`/api/analytics/dataset-summary`).
- **Latency:** Sub-10ms response time per prediction request.

### 7.2 Frontend (React + TypeScript + Tailwind)
- **Framework:** React 19 + TypeScript + Vite with custom enterprise dark theme.
- **Interactive Features:** Real-time hardware calculation HUD, dynamic sliders, device presets, 4-model consensus dashboard, and feature importance explainability charts.

---

## 8. Viva Voce Q&A Cheat Sheet

1. **Q: Why did you frame smartphone price prediction as a 4-class classification problem rather than continuous regression?**  
   *A:* Smartphone markets are commercially organized into distinct economic tiers (Budget, Mid-Range, Premium, Flagship). Continuous price regression is easily distorted by luxury outliers (e.g. ₹650,000 foldable editions), whereas multi-class classification provides clear decision boundaries and actionable consumer category probabilities.

2. **Q: How did you ensure there was no data leakage in your preprocessing?**  
   *A:* We separated the dataset using a Stratified 80/20 train-test split before fitting any transformers. All numerical medians, standard scaling parameters, and one-hot encodings were computed exclusively on $X_{\text{train}}$ and transformed on $X_{\text{test}}$. Continuous price was strictly dropped from the feature set.

3. **Q: Why did Random Forest outperform Support Vector Machines and Logistic Regression?**  
   *A:* Random Forest naturally captures complex non-linear feature interactions (such as the combination of 120Hz display, 12GB RAM, and Snapdragon 8 series) without requiring manual polynomial basis expansions, and is robust to mixed numerical/one-hot feature scales.

4. **Q: Why is the correlation between battery capacity and smartphone price negative?**  
   *A:* High-end flagship devices prioritize ultra-slim titanium/glass industrial designs, wireless charging coils, and high-wattage fast charging over heavy, bulky 6,000+ mAh battery cells that are predominantly found in budget utility phones.

5. **Q: What is the difference between Gini Importance (MDI) and Permutation Feature Importance?**  
   *A:* Gini Importance (MDI) is computed during tree training and can be biased toward high-cardinality continuous features. Permutation Importance evaluates the actual degradation in Macro F1 score on unseen test data when a feature is randomly permuted, providing an unbiased model-agnostic measurement of feature utility.

---

## 9. Conclusion
The **SmartPrice** project successfully demonstrates a rigorous, scientifically grounded approach to multi-class smartphone price classification. Through careful feature engineering, zero-leakage pipeline design, comprehensive cross-validation, and systematic hyperparameter tuning, the Random Forest model achieved **82.65% Accuracy** and **0.9613 ROC-AUC**. Deployed via a modern FastAPI backend and React frontend, the system bridges theoretical machine learning principles with practical production engineering.

---
*SmartPrice — University ML Lab Project Repository: [https://github.com/Anas-sk02/Mobile-Price-Prediction-ML](https://github.com/Anas-sk02/Mobile-Price-Prediction-ML)*
