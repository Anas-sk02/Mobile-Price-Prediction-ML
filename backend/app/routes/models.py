"""
Model Benchmarks, Metrics, ROC Curves & Feature Importance Endpoints
"""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/models", tags=["Model Evaluation & Explainability"])
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ml" / "outputs"


@router.get("/list")
def list_models():
    return {
        "models": [
            {"key": "random_forest", "name": "Random Forest", "status": "Champion Model", "accuracy": "82.65%", "f1": "79.96%"},
            {"key": "svm", "name": "Support Vector Machine (RBF)", "status": "Tuned", "accuracy": "80.10%", "f1": "78.07%"},
            {"key": "knn", "name": "K-Nearest Neighbors", "status": "Tuned", "accuracy": "79.59%", "f1": "76.38%"},
            {"key": "logistic_regression", "name": "Logistic Regression", "status": "Tuned", "accuracy": "78.57%", "f1": "76.39%"}
        ],
        "champion": "random_forest"
    }


@router.get("/metrics")
def get_model_metrics():
    path = OUTPUT_DIR / "05_hyperparameter_tuning_results.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Model metrics file not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@router.get("/roc-curves")
def get_roc_curves():
    path = OUTPUT_DIR / "06_evaluation_and_curves_data.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Evaluation curves file not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@router.get("/feature-importance")
def get_feature_importance():
    path = OUTPUT_DIR / "07_feature_importance.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Feature importance file not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
