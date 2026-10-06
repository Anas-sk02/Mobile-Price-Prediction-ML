"""
Analytics & Dataset Insights Endpoints
"""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/analytics", tags=["Dataset Analytics"])
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ml" / "outputs"


@router.get("/dataset-summary")
def get_dataset_summary():
    path = OUTPUT_DIR / "01_inspection_report.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Dataset summary not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@router.get("/eda-insights")
def get_eda_insights():
    path = OUTPUT_DIR / "02_eda_summary.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="EDA summary not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
