"""
SmartPrice — Automated Full Pipeline Retraining Script
Run this script whenever `data/raw/smartphone_cleaned_v5.csv` is modified (rows added or removed).
"""

import sys
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PIPELINE_STEPS = [
    ("ml/src/01_inspect_dataset.py", "1. Dataset Inspection & Audit"),
    ("ml/src/02_exploratory_data_analysis.py", "2. EDA & Distribution Analytics"),
    ("ml/src/03_data_preprocessing.py", "3. Zero-Leakage Preprocessing & Splits"),
    ("ml/src/04_train_baseline_models.py", "4. Baseline Model Training (4 Models)"),
    ("ml/src/05_hyperparameter_tuning.py", "5. 5-Fold Stratified GridSearchCV Tuning"),
    ("ml/src/06_evaluate_and_curves.py", "6. Multi-Class ROC Curves & Error Analysis"),
    ("ml/src/07_feature_importance.py", "7. Permutation & Tree Feature Importance")
]


def run_full_pipeline():
    print("=" * 80)
    print(" SmartPrice — End-to-End Automated Pipeline Retraining")
    print("=" * 80)
    start_total = time.time()

    for script_rel, desc in PIPELINE_STEPS:
        script_path = PROJECT_ROOT / script_rel
        print(f"\n[RUNNING] {desc} ({script_rel})...")
        t0 = time.time()
        res = subprocess.run([sys.executable, str(script_path)], cwd=str(PROJECT_ROOT))
        if res.returncode != 0:
            print(f"\n❌ ERROR: Step failed at {script_rel} (Exit code: {res.returncode})")
            sys.exit(res.returncode)
        elapsed = time.time() - t0
        print(f"[COMPLETED] {desc} in {elapsed:.2f}s ✔")

    total_time = time.time() - start_total
    print("\n" + "=" * 80)
    print(f" ALL PIPELINE ARTIFACTS & MODELS RETRAINED SUCCESSFULLY IN {total_time:.2f}s!")
    print(" The FastAPI backend will immediately serve the updated model weights and metrics.")
    print("=" * 80)


if __name__ == "__main__":
    run_full_pipeline()
