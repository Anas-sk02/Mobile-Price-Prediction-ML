"""
Health & System Status Router
"""

from fastapi import APIRouter
from ..schemas import HealthResponse
from ..predictor import engine

router = APIRouter(tags=["System & Health"])


@router.get("/health", response_model=HealthResponse)
def get_health():
    engine.load()
    return {
        "status": "healthy",
        "service": "SmartPrice ML Prediction & Benchmarking API",
        "version": "1.0.0",
        "champion_model": engine.champion_meta["display_name"] if engine.champion_meta else "Random Forest",
        "loaded_models": list(engine.all_models.keys())
    }


@router.get("/docs-info")
def get_docs_info():
    return {
        "project": "SmartPrice",
        "author": "Anas-sk02",
        "endpoints": [
            {"path": "/api/predict", "method": "POST", "desc": "Single smartphone price category prediction"},
            {"path": "/api/predict/batch", "method": "POST", "desc": "Batch predictions for multiple smartphones"},
            {"path": "/api/predict/compare", "method": "POST", "desc": "Side-by-side prediction across all 4 ML models"},
            {"path": "/api/models/metrics", "method": "GET", "desc": "Benchmarking metrics, accuracy, F1, and CV scores"},
            {"path": "/api/models/roc-curves", "method": "GET", "desc": "Interactive ROC & PR curve coordinates"},
            {"path": "/api/models/feature-importance", "method": "GET", "desc": "Permutation & MDI feature importance rankings"},
            {"path": "/api/analytics/dataset-summary", "method": "GET", "desc": "Dataset distribution & hardware statistics"}
        ]
    }
