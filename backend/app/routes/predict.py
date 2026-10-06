"""
Prediction Endpoints (Single, Batch, and Multi-Model Comparison)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..schemas import (
    SmartphoneInput, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse,
    ModelComparisonResponse
)
from ..predictor import engine

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("", response_model=PredictionResponse)
def predict_single(input_data: SmartphoneInput, model: Optional[str] = Query("champion", description="Model key: champion, random_forest, svm, knn, logistic_regression")):
    try:
        raw_dict = input_data.model_dump()
        result = engine.predict_single(raw_dict, model_key=model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/batch", response_model=BatchPredictionResponse)
def predict_batch(batch_request: BatchPredictionRequest, model: Optional[str] = Query("champion")):
    try:
        results = []
        for item in batch_request.smartphones:
            res = engine.predict_single(item.model_dump(), model_key=model)
            results.append(res)
        return {
            "total_samples": len(results),
            "predictions": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")


@router.post("/compare", response_model=ModelComparisonResponse)
def compare_models(input_data: SmartphoneInput):
    try:
        raw_dict = input_data.model_dump()
        result = engine.compare_all_models(raw_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model comparison error: {str(e)}")
