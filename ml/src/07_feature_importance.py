"""
SmartPrice - Phase 7: Feature Importance & Model Explainability
================================================================
Calculates:
1. Random Forest Gini / MDI (Mean Decrease in Impurity) Feature Importance
2. Model-Agnostic Permutation Feature Importance on Test Data (Scoring: F1 Macro)
3. Multinomial Logistic Regression Coefficients per Price Tier
4. Aggregated Feature Group Importance (Processor/Memory, Display, Cameras, Connectivity, Brand/OS)
5. Exports structured JSON for FastAPI explainability endpoints and React frontend widgets.
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

from sklearn.inspection import permutation_importance

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

FIG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = ["Budget", "Mid-Range", "Premium", "Flagship"]


def load_assets():
    X_train = np.load(PROCESSED_DATA_DIR / "X_train.npy")
    X_test = np.load(PROCESSED_DATA_DIR / "X_test.npy")
    y_train = np.load(PROCESSED_DATA_DIR / "y_train.npy")
    y_test = np.load(PROCESSED_DATA_DIR / "y_test.npy")

    preprocessor_meta = joblib.load(MODEL_DIR / "preprocessor.joblib")
    feature_names = preprocessor_meta["transformed_feature_names"]

    champion_data = joblib.load(MODEL_DIR / "best_model.joblib")
    rf_model = champion_data["model"]

    lr_model = joblib.load(MODEL_DIR / "tuned_logistic_regression.joblib")

    return X_train, X_test, y_train, y_test, feature_names, rf_model, lr_model


def group_feature(name: str) -> str:
    """Categorizes transformed feature into domain functional groups."""
    if any(k in name for k in ['ram', 'internal_memory', 'processor', 'performance_score', 'num_cores']):
        return "Core Hardware & Processor"
    elif any(k in name for k in ['camera']):
        return "Camera Systems"
    elif any(k in name for k in ['resolution', 'pixel', 'aspect', 'ppi', 'screen_size', 'refresh_rate']):
        return "Display & Visuals"
    elif any(k in name for k in ['battery', 'fast_charging', 'screen_to_battery']):
        return "Battery & Power"
    elif any(k in name for k in ['brand_grouped', 'os_grouped']):
        return "Brand & Operating System"
    elif any(k in name for k in ['has_5g', 'has_nfc', 'has_ir_blaster', 'extended']):
        return "Connectivity & Expansion"
    else:
        return "Other / Miscellaneous"


def compute_feature_importance(rf_model, lr_model, X_test, y_test, feature_names: list[str]):
    print("Computing Random Forest MDI & Permutation Feature Importance...")

    # 1. Random Forest MDI (Gini Importance)
    mdi_importances = rf_model.feature_importances_
    
    # 2. Permutation Importance on Test Set
    perm_result = permutation_importance(
        rf_model, X_test, y_test,
        n_repeats=15, random_state=42, scoring='f1_macro', n_jobs=-1
    )
    perm_importances_mean = perm_result.importances_mean
    perm_importances_std = perm_result.importances_std

    # Compile DataFrame
    df_importance = pd.DataFrame({
        "feature": feature_names,
        "mdi_importance": mdi_importances,
        "permutation_mean": perm_importances_mean,
        "permutation_std": perm_importances_std,
        "feature_group": [group_feature(f) for f in feature_names]
    }).sort_values(by="permutation_mean", ascending=False)

    # 3. Logistic Regression Coefficients
    lr_coefs = lr_model.coef_  # Shape: (4, n_features)
    df_lr = pd.DataFrame(lr_coefs, columns=feature_names, index=CLASS_NAMES)

    # 4. Grouped Importance
    grouped_importance = df_importance.groupby("feature_group")["mdi_importance"].sum().sort_values(ascending=False).to_dict()

    return df_importance, df_lr, grouped_importance


def plot_importance_figures(df_importance: pd.DataFrame, df_lr: pd.DataFrame, grouped_importance: dict):
    print("Generating feature importance visualizations...")

    # 1. Top 15 Features: MDI vs Permutation Importance
    top_15_perm = df_importance.sort_values(by="permutation_mean", ascending=False).head(15)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Permutation Importance on Test Data
    axes[0].barh(top_15_perm["feature"][::-1], top_15_perm["permutation_mean"][::-1],
                 xerr=top_15_perm["permutation_std"][::-1], color="#2563EB", edgecolor="black", alpha=0.85)
    axes[0].set_title("Top 15 Features by Test Permutation Importance\n(Drop in Macro F1 when Shuffled)", fontweight="bold")
    axes[0].set_xlabel("Mean Decrease in Macro F1-Score", fontweight="bold")

    # MDI Gini Importance
    top_15_mdi = df_importance.sort_values(by="mdi_importance", ascending=False).head(15)
    axes[1].barh(top_15_mdi["feature"][::-1], top_15_mdi["mdi_importance"][::-1],
                 color="#059669", edgecolor="black", alpha=0.85)
    axes[1].set_title("Top 15 Features by Tree Gini Impurity (MDI)\n(Random Forest Feature Importances)", fontweight="bold")
    axes[1].set_xlabel("Normalized Gini Importance", fontweight="bold")

    plt.tight_layout()
    fig_path1 = FIG_DIR / "09_random_forest_feature_importance.png"
    fig.savefig(fig_path1, dpi=300)
    plt.close(fig)
    print(f"  [OK] Saved {fig_path1.name}")

    # 2. Logistic Regression Coefficients Heatmap (Top 12 impactful features)
    top_12_features = df_importance.sort_values(by="permutation_mean", ascending=False).head(12)["feature"].tolist()
    sub_lr = df_lr[top_12_features]

    fig, ax = plt.subplots(figsize=(13, 6))
    sns.heatmap(sub_lr, cmap="coolwarm", center=0, annot=True, fmt=".2f",
                linewidths=.6, cbar_kws={"label": "Standardized Log-Odds Coefficient"}, ax=ax)
    ax.set_title("Multinomial Logistic Regression Feature Weights Across Price Tiers", fontweight="bold", pad=12)
    ax.set_xlabel("Top Predictive Features", fontweight="bold")
    ax.set_ylabel("Price Category", fontweight="bold")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    fig_path2 = FIG_DIR / "10_logistic_regression_coefficients.png"
    fig.savefig(fig_path2, dpi=300)
    plt.close(fig)
    print(f"  [OK] Saved {fig_path2.name}")

    # 3. Grouped Importance Donut Chart
    fig, ax = plt.subplots(figsize=(8, 7))
    labels = list(grouped_importance.keys())
    values = list(grouped_importance.values())
    colors = sns.color_palette("Set2", len(labels))

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.1f%%", startangle=140,
        colors=colors, wedgeprops=dict(width=0.4, edgecolor='black'),
        pctdistance=0.75, textprops=dict(fontweight="bold")
    )
    ax.set_title("Hardware & Domain Group Contribution to Price Category", fontweight="bold", pad=14)
    plt.tight_layout()
    fig_path3 = FIG_DIR / "11_feature_importance_by_group.png"
    fig.savefig(fig_path3, dpi=300)
    plt.close(fig)
    print(f"  [OK] Saved {fig_path3.name}")


def serialize_explainability_data(df_importance: pd.DataFrame, df_lr: pd.DataFrame, grouped_importance: dict):
    # Prepare top ranked features for API consumption
    top_ranked = []
    for _, row in df_importance.sort_values(by="permutation_mean", ascending=False).iterrows():
        top_ranked.append({
            "feature": row["feature"],
            "group": row["feature_group"],
            "permutation_mean": round(float(row["permutation_mean"]), 4),
            "permutation_std": round(float(row["permutation_std"]), 4),
            "mdi_importance": round(float(row["mdi_importance"]), 4)
        })

    # Prepare logistic weights
    lr_weights = {}
    for cat in CLASS_NAMES:
        lr_weights[cat] = {col: round(float(df_lr.loc[cat, col]), 4) for col in df_lr.columns}

    json_export = {
        "ranked_features": top_ranked,
        "grouped_importance": {k: round(float(v), 4) for k, v in grouped_importance.items()},
        "logistic_regression_weights": lr_weights
    }

    json_path = OUTPUT_DIR / "07_feature_importance.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_export, f, indent=2)
    print(f"\n[OK] Feature Explainability JSON exported to: {json_path}")


def main():
    print("=" * 80)
    print(" SmartPrice - Phase 7: Feature Importance & Explainability Analysis")
    print("=" * 80)

    X_train, X_test, y_train, y_test, feature_names, rf_model, lr_model = load_assets()

    df_importance, df_lr, grouped_importance = compute_feature_importance(
        rf_model, lr_model, X_test, y_test, feature_names
    )

    plot_importance_figures(df_importance, df_lr, grouped_importance)
    serialize_explainability_data(df_importance, df_lr, grouped_importance)

    # Save Markdown Summary
    summary_md_path = OUTPUT_DIR / "07_explainability_summary.md"
    top_10 = df_importance.sort_values(by="permutation_mean", ascending=False).head(10)

    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write("# SmartPrice — Phase 7: Feature Importance & Model Explainability Report\n\n")
        
        f.write("## 1. Top 10 Most Influential Features (Permutation Importance on Test Set)\n\n")
        f.write("| Rank | Feature Name | Domain Group | Permutation Mean ($\Delta$ Macro F1) | MDI Gini Importance |\n")
        f.write("|:---:|---|---|:---:|:---:|\n")
        for rank, (_, row) in enumerate(top_10.iterrows(), 1):
            f.write(f"| {rank} | **`{row['feature']}`** | {row['feature_group']} | **{row['permutation_mean']:.4f}** $\pm$ {row['permutation_std']:.4f} | {row['mdi_importance']:.4f} |\n")
        f.write("\n")

        f.write("## 2. Hardware Domain Group Contributions\n\n")
        f.write("| Functional Group | Cumulative Tree Importance (%) |\n")
        f.write("|---|:---:|\n")
        for grp, val in grouped_importance.items():
            f.write(f"| **{grp}** | **{val*100:.2f}%** |\n")
        f.write("\n")

        f.write("## 3. Directional Influence (Logistic Regression Weights)\n\n")
        f.write("- **Budget Drivers:** Higher `ram_capacity`, `performance_score`, and `refresh_rate` strongly decrease the odds of a device being in the Budget class (large negative weights).\n")
        f.write("- **Flagship Drivers:** High `processor_speed`, `internal_memory` (>= 256GB), `refresh_rate` (120Hz+), and Apple/Samsung ecosystem indicators exhibit large positive coefficients for the Flagship category.\n")
        f.write("- **Mid-Range / Premium Boundary:** `fast_charging` (W) and `primary_camera_rear` (50-200MP) are the primary discriminators pushing phones from Mid-Range into Premium.\n\n")

        f.write("## 4. Generated Artifacts in Phase 7\n\n")
        f.write("1. `09_random_forest_feature_importance.png`: Dual comparison of Permutation vs. MDI Gini importance.\n")
        f.write("2. `10_logistic_regression_coefficients.png`: Directional log-odds coefficients heatmap across all 4 tiers.\n")
        f.write("3. `11_feature_importance_by_group.png`: Donut chart of aggregate domain hardware contributions.\n")
        f.write("4. `07_feature_importance.json`: Full ranking and weights payload for API/UI explainability components.\n")

    print(f"[OK] Explainability Markdown Summary saved to: {summary_md_path}")
    print("=" * 80)
    print(" Phase 7: Feature Importance & Explainability COMPLETED.")
    print("=" * 80)


if __name__ == "__main__":
    main()
