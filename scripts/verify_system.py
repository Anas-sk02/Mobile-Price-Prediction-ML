"""
SmartPrice - End-to-End System Verification Script
===================================================
Verifies all project artifacts, data files, trained ML models,
FastAPI endpoints, and frontend build readiness.
"""

import sys
from pathlib import Path

# Fix path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def verify_system():
    print("=" * 80)
    print(" SmartPrice — End-to-End System Integrity & Artifacts Verification")
    print("=" * 80)

    # 1. Verify Dataset Files
    raw_data = PROJECT_ROOT / "data" / "raw" / "smartphone_cleaned_v5.csv"
    processed_data = PROJECT_ROOT / "data" / "processed" / "smartphones_cleaned.csv"
    x_train_arr = PROJECT_ROOT / "data" / "processed" / "X_train.npy"
    assert raw_data.exists(), "Raw dataset missing"
    assert processed_data.exists(), "Processed dataset missing"
    assert x_train_arr.exists(), "X_train numpy array missing"
    print("[1] Dataset & Processed Partitions:     [OK]")

    # 2. Verify Models Checkpoints
    models = [
        "preprocessor.joblib",
        "best_model.joblib",
        "tuned_random_forest.joblib",
        "tuned_svm.joblib",
        "tuned_knn.joblib",
        "tuned_logistic_regression.joblib"
    ]
    for m in models:
        m_path = PROJECT_ROOT / "ml" / "models" / m
        assert m_path.exists(), f"Model {m} missing"
    print(f"[2] All 6 Serialized Model Pipelines:   [OK]")

    # 3. Verify Generated Figures
    figs = [
        "01_price_distribution.png",
        "02_price_by_category.png",
        "05_correlation_heatmap.png",
        "01_baseline_confusion_matrices.png",
        "02_baseline_model_comparison.png",
        "03_hyperparameter_tuning_comparison.png",
        "04_tuned_confusion_matrices.png",
        "05_multiclass_roc_curves.png",
        "06_precision_recall_curves.png",
        "09_random_forest_feature_importance.png",
        "10_logistic_regression_coefficients.png"
    ]
    for f in figs:
        f_path = PROJECT_ROOT / "ml" / "outputs" / "model_figures" / f
        if not f_path.exists():
            f_path = PROJECT_ROOT / "ml" / "outputs" / "eda_figures" / f
        assert f_path.exists(), f"Figure {f} missing"
    print(f"[3] Publication-Grade Visual Assets:    [OK]")

    # 4. Verify Backend API Functionality
    from fastapi.testclient import TestClient
    from backend.app.main import app
    client = TestClient(app)
    health = client.get("/api/health")
    assert health.status_code == 200 and health.json()["status"] == "healthy"
    
    predict_res = client.post("/api/predict", json={
        "brand_name": "samsung",
        "rating": 85.0,
        "has_5g": True,
        "has_nfc": True,
        "has_ir_blaster": False,
        "processor_brand": "snapdragon",
        "num_cores": 8.0,
        "processor_speed": 3.2,
        "battery_capacity": 5000.0,
        "fast_charging_available": 1,
        "fast_charging": 45.0,
        "ram_capacity": 12.0,
        "internal_memory": 256.0,
        "screen_size": 6.8,
        "refresh_rate": 120,
        "resolution": "1440 x 3088",
        "num_rear_cameras": 4,
        "num_front_cameras": 1.0,
        "os": "android",
        "primary_camera_rear": 200.0,
        "primary_camera_front": 12.0,
        "extended_memory_available": 0,
        "extended_upto": 0.0
    })
    assert predict_res.status_code == 200
    assert predict_res.json()["predicted_category"] == "Flagship"
    print(f"[4] FastAPI Backend Engine Live Tests:  [OK]")

    # 5. Verify Frontend Production Build
    dist_index = PROJECT_ROOT / "frontend" / "dist" / "index.html"
    assert dist_index.exists(), "Frontend build missing"
    print(f"[5] React / TypeScript UI Production:   [OK]")

    print("=" * 80)
    print(" ALL 5 SUBSYSTEMS VERIFIED AND OPERATIONAL AT 100% HEALTH!")
    print("=" * 80)

if __name__ == "__main__":
    verify_system()
