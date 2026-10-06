"""
SmartPrice - Phase 5: Hyperparameter Tuning & Grid Search Optimization
=======================================================================
Performs systematic 5-Fold Stratified GridSearchCV for the 4 core models:
1. Logistic Regression (Regularization C, Solvers)
2. K-Nearest Neighbors (k-value, Distance metrics, Weighting)
3. Random Forest (Estimators, Tree Depth, Min Leaf/Split, Max Features)
4. Support Vector Machine (C parameter, Gamma, Kernels)

Measures Baseline vs. Tuned delta gains and exports the champion model
to `ml/models/best_model.joblib` for API serving.
"""

import sys
import json
import joblib
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

# Reconfigure stdout for Windows console UTF-8 support
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

# Paths setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "ml" / "models"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"
FIG_DIR = OUTPUT_DIR / "model_figures"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = ["Budget", "Mid-Range", "Premium", "Flagship"]


def load_data():
    X_train = np.load(PROCESSED_DATA_DIR / "X_train.npy")
    X_test = np.load(PROCESSED_DATA_DIR / "X_test.npy")
    y_train = np.load(PROCESSED_DATA_DIR / "y_train.npy")
    y_test = np.load(PROCESSED_DATA_DIR / "y_test.npy")
    return X_train, X_test, y_train, y_test


def get_tuning_configs():
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    configs = {
        "logistic_regression": {
            "name": "Logistic Regression",
            "estimator": LogisticRegression(max_iter=1500, random_state=42),
            "param_grid": {
                "C": [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
                "solver": ["lbfgs", "saga"]
            },
            "cv": cv
        },
        "knn": {
            "name": "K-Nearest Neighbors",
            "estimator": KNeighborsClassifier(),
            "param_grid": {
                "n_neighbors": [3, 5, 7, 9, 11, 13, 15, 19],
                "weights": ["uniform", "distance"],
                "metric": ["euclidean", "manhattan"]
            },
            "cv": cv
        },
        "random_forest": {
            "name": "Random Forest",
            "estimator": RandomForestClassifier(random_state=42),
            "param_grid": {
                "n_estimators": [100, 200, 300],
                "max_depth": [None, 10, 15, 20],
                "min_samples_split": [2, 5],
                "min_samples_leaf": [1, 2],
                "max_features": ["sqrt", "log2"]
            },
            "cv": cv
        },
        "svm": {
            "name": "Support Vector Machine",
            "estimator": SVC(probability=True, random_state=42),
            "param_grid": {
                "C": [0.5, 1.0, 3.0, 5.0, 10.0, 20.0],
                "gamma": ["scale", "auto", 0.01, 0.05],
                "kernel": ["rbf", "linear"]
            },
            "cv": cv
        }
    }
    return configs


def evaluate_tuned_model(name: str, grid_search: GridSearchCV, X_test, y_test) -> dict:
    best_estimator = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = float(grid_search.best_score_)

    y_test_pred = best_estimator.predict(X_test)
    
    # Probability scores for ROC-AUC
    if hasattr(best_estimator, "predict_proba"):
        y_test_proba = best_estimator.predict_proba(X_test)
        roc_auc_macro = float(roc_auc_score(y_test, y_test_proba, multi_class='ovr', average='macro'))
        roc_auc_weighted = float(roc_auc_score(y_test, y_test_proba, multi_class='ovr', average='weighted'))
    else:
        roc_auc_macro = None
        roc_auc_weighted = None

    test_acc = float(accuracy_score(y_test, y_test_pred))
    precision_macro = float(precision_score(y_test, y_test_pred, average='macro', zero_division=0))
    recall_macro = float(recall_score(y_test, y_test_pred, average='macro', zero_division=0))
    f1_macro = float(f1_score(y_test, y_test_pred, average='macro', zero_division=0))

    precision_weighted = float(precision_score(y_test, y_test_pred, average='weighted', zero_division=0))
    recall_weighted = float(recall_score(y_test, y_test_pred, average='weighted', zero_division=0))
    f1_weighted = float(f1_score(y_test, y_test_pred, average='weighted', zero_division=0))

    clf_report = classification_report(y_test, y_test_pred, target_names=CLASS_NAMES, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_test_pred)

    print(f"\n  [Tuned Results: {name}]")
    print(f"    * Best Hyperparameters: {best_params}")
    print(f"    * 5-Fold Best CV F1:     {best_cv_score * 100:.2f}%")
    print(f"    * Test Accuracy:         {test_acc * 100:.2f}%")
    print(f"    * Test Macro F1:         {f1_macro * 100:.2f}%")
    print(f"    * Test Weighted F1:      {f1_weighted * 100:.2f}%")
    if roc_auc_macro:
        print(f"    * ROC-AUC (OvR Macro):   {roc_auc_macro:.4f}")

    return {
        "name": name,
        "best_params": best_params,
        "best_cv_score": round(best_cv_score, 4),
        "test_accuracy": round(test_acc, 4),
        "precision_macro": round(precision_macro, 4),
        "recall_macro": round(recall_macro, 4),
        "f1_macro": round(f1_macro, 4),
        "precision_weighted": round(precision_weighted, 4),
        "recall_weighted": round(recall_weighted, 4),
        "f1_weighted": round(f1_weighted, 4),
        "roc_auc_macro": round(roc_auc_macro, 4) if roc_auc_macro else None,
        "roc_auc_weighted": round(roc_auc_weighted, 4) if roc_auc_weighted else None,
        "classification_report": clf_report,
        "confusion_matrix": cm.tolist()
    }


def plot_tuning_figures(baseline_results: dict, tuned_results: dict):
    print("\nPlotting tuning comparison figures...")

    # 1. Baseline vs. Tuned Accuracy & F1 Comparison Bar Chart
    model_keys = list(tuned_results.keys())
    model_names = [tuned_results[k]['name'] for k in model_keys]
    
    base_acc = [baseline_results[k]['test_accuracy'] * 100 for k in model_keys]
    tuned_acc = [tuned_results[k]['test_accuracy'] * 100 for k in model_keys]
    
    base_f1 = [baseline_results[k]['f1_macro'] * 100 for k in model_keys]
    tuned_f1 = [tuned_results[k]['f1_macro'] * 100 for k in model_keys]

    x = np.arange(len(model_names))
    width = 0.2

    fig, ax = plt.subplots(figsize=(13, 6))
    rects1 = ax.bar(x - 1.5*width, base_acc, width, label='Baseline Accuracy', color='#93C5FD', edgecolor='black')
    rects2 = ax.bar(x - 0.5*width, tuned_acc, width, label='Tuned Accuracy', color='#2563EB', edgecolor='black')
    rects3 = ax.bar(x + 0.5*width, base_f1, width, label='Baseline Macro F1', color='#FDE68A', edgecolor='black')
    rects4 = ax.bar(x + 1.5*width, tuned_f1, width, label='Tuned Macro F1', color='#D97706', edgecolor='black')

    ax.set_ylabel('Score (%)', fontweight='bold')
    ax.set_title('Baseline vs. Hyperparameter-Tuned Performance Across 4 Models', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, fontweight='bold')
    ax.set_ylim(65, 100)
    ax.legend(loc='lower right', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotations
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    fig.savefig(FIG_DIR / "03_hyperparameter_tuning_comparison.png", dpi=300)
    plt.close(fig)
    print("  [OK] Saved 03_hyperparameter_tuning_comparison.png")

    # 2. 2x2 Grid of Tuned Confusion Matrices
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()

    for idx, m_key in enumerate(model_keys):
        res = tuned_results[m_key]
        cm = np.array(res['confusion_matrix'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', ax=axes[idx],
                    xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES,
                    cbar=False, annot_kws={"size": 14, "fontweight": "bold"})
        axes[idx].set_title(f"{res['name']} (Tuned)\nTest Acc: {res['test_accuracy']*100:.2f}% | F1: {res['f1_macro']*100:.2f}%", 
                            fontweight='bold', fontsize=12)
        axes[idx].set_xlabel("Predicted Class", fontweight='bold')
        axes[idx].set_ylabel("True Class", fontweight='bold')

    plt.tight_layout()
    fig.savefig(FIG_DIR / "04_tuned_confusion_matrices.png", dpi=300)
    plt.close(fig)
    print("  [OK] Saved 04_tuned_confusion_matrices.png")


def main():
    print("=" * 80)
    print(" SmartPrice - Phase 5: Hyperparameter Tuning & Grid Search Optimization")
    print("=" * 80)

    X_train, X_test, y_train, y_test = load_data()
    print(f"Loaded X_train: {X_train.shape}, X_test: {X_test.shape}")

    # Load baseline results for comparison
    baseline_json_path = OUTPUT_DIR / "04_baseline_models_results.json"
    if baseline_json_path.exists():
        with open(baseline_json_path, "r", encoding="utf-8") as f:
            baseline_results = json.load(f)
    else:
        baseline_results = {}

    configs = get_tuning_configs()
    tuned_results = {}
    best_models = {}

    for key, cfg in configs.items():
        print(f"\nRunning 5-Fold Stratified GridSearchCV for: {cfg['name']}...")
        print(f"  Grid parameter combinations: {np.prod([len(v) for v in cfg['param_grid'].values()])}")
        
        grid = GridSearchCV(
            estimator=cfg["estimator"],
            param_grid=cfg["param_grid"],
            cv=cfg["cv"],
            scoring="f1_macro",
            n_jobs=-1,
            refit=True
        )
        grid.fit(X_train, y_train)

        eval_data = evaluate_tuned_model(cfg["name"], grid, X_test, y_test)
        tuned_results[key] = eval_data
        best_models[key] = grid.best_estimator_

        # Save individual tuned model checkpoint
        tuned_model_path = MODEL_DIR / f"tuned_{key}.joblib"
        joblib.dump(grid.best_estimator_, tuned_model_path)
        print(f"  [OK] Saved checkpoint: {tuned_model_path.name}")

    # Determine Champion Model (Highest Test Accuracy + Macro F1)
    champion_key = max(tuned_results.keys(), key=lambda k: (tuned_results[k]['test_accuracy'], tuned_results[k]['f1_macro']))
    champion_model = best_models[champion_key]
    champion_info = tuned_results[champion_key]

    print(f"\n================================================================================")
    print(f" CHAMPION PRODUCTION MODEL: {champion_info['name']}")
    print(f" Test Accuracy: {champion_info['test_accuracy']*100:.2f}% | Macro F1: {champion_info['f1_macro']*100:.2f}% | ROC-AUC: {champion_info['roc_auc_macro']:.4f}")
    print(f" Best Params:   {champion_info['best_params']}")
    print(f"================================================================================")

    # Save champion model to best_model.joblib for FastAPI & Frontend production serving
    champion_save_path = MODEL_DIR / "best_model.joblib"
    joblib.dump({
        "model_key": champion_key,
        "display_name": champion_info["name"],
        "model": champion_model,
        "best_params": champion_info["best_params"],
        "test_accuracy": champion_info["test_accuracy"],
        "f1_macro": champion_info["f1_macro"],
        "roc_auc_macro": champion_info["roc_auc_macro"],
        "class_names": CLASS_NAMES
    }, champion_save_path)
    print(f"[OK] Production Champion Model saved to: {champion_save_path}")

    # Plot comparison graphs
    if baseline_results:
        plot_tuning_figures(baseline_results, tuned_results)

    # Save Tuning Results JSON
    tuning_output_json = OUTPUT_DIR / "05_hyperparameter_tuning_results.json"
    with open(tuning_output_json, "w", encoding="utf-8") as f:
        json.dump({
            "champion_model": champion_key,
            "champion_details": champion_info,
            "all_tuned_models": tuned_results
        }, f, indent=2)
    print(f"[OK] Tuning Results JSON saved to: {tuning_output_json}")

    # Save Markdown Summary
    tuning_output_md = OUTPUT_DIR / "05_tuning_summary.md"
    with open(tuning_output_md, "w", encoding="utf-8") as f:
        f.write("# SmartPrice — Phase 5: Hyperparameter Tuning & Grid Search Report\n\n")
        f.write(f"## 1. Champion Model: **{champion_info['name']}** 🏆\n\n")
        f.write(f"- **Optimal Parameters:** `{champion_info['best_params']}`\n")
        f.write(f"- **Test Accuracy:** **{champion_info['test_accuracy']*100:.2f}%**\n")
        f.write(f"- **Macro F1-Score:** **{champion_info['f1_macro']*100:.2f}%**\n")
        f.write(f"- **Multi-Class ROC-AUC (OvR):** **{champion_info['roc_auc_macro']:.4f}**\n\n")

        f.write("## 2. Baseline vs. Tuned Performance Benchmark\n\n")
        f.write("| Model Name | Baseline Acc (%) | Tuned Acc (%) | Baseline F1 (%) | Tuned F1 (%) | Tuned ROC-AUC | Optimal Hyperparameters |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for k in tuned_results.keys():
            t_res = tuned_results[k]
            b_acc = f"{baseline_results[k]['test_accuracy']*100:.2f}%" if k in baseline_results else "N/A"
            b_f1 = f"{baseline_results[k]['f1_macro']*100:.2f}%" if k in baseline_results else "N/A"
            f.write(f"| **{t_res['name']}** | {b_acc} | **{t_res['test_accuracy']*100:.2f}%** | {b_f1} | **{t_res['f1_macro']*100:.2f}%** | {t_res['roc_auc_macro']:.4f} | `{t_res['best_params']}` |\n")
        f.write("\n")

        f.write("## 3. Tuned Class-Wise Classification Metrics\n\n")
        for k, r in tuned_results.items():
            f.write(f"### {r['name']} (Tuned)\n")
            f.write("| Category | Precision | Recall | F1-Score | Support |\n")
            f.write("|---|---|---|---|---|\n")
            cr = r['classification_report']
            for c in CLASS_NAMES:
                f.write(f"| **{c}** | {cr[c]['precision']:.4f} | {cr[c]['recall']:.4f} | {cr[c]['f1-score']:.4f} | {int(cr[c]['support'])} |\n")
            f.write(f"| *Macro Avg* | {cr['macro avg']['precision']:.4f} | {cr['macro avg']['recall']:.4f} | {cr['macro avg']['f1-score']:.4f} | {int(cr['macro avg']['support'])} |\n")
            f.write(f"| *Weighted Avg* | {cr['weighted avg']['precision']:.4f} | {cr['weighted avg']['recall']:.4f} | {cr['weighted avg']['f1-score']:.4f} | {int(cr['weighted avg']['support'])} |\n\n")

    print(f"[OK] Tuning Markdown Summary saved to: {tuning_output_md}")
    print("=" * 80)
    print(" Phase 5: Hyperparameter Tuning & Grid Search COMPLETED.")
    print("=" * 80)


if __name__ == "__main__":
    main()
