"""
Analytics & Dataset Insights Endpoints
"""

import json
from pathlib import Path
from typing import Optional
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/analytics", tags=["Dataset Analytics"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
OUTPUT_DIR = BASE_DIR / "ml" / "outputs"
DATA_PATH = BASE_DIR / "data" / "raw" / "smartphone_cleaned_v5.csv"


def assign_price_tier(price: float) -> str:
    if price <= 15000:
        return "Budget"
    elif price <= 30000:
        return "Mid-Range"
    elif price <= 50000:
        return "Premium"
    else:
        return "Flagship"


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


@router.get("/records")
def get_dataset_records(
    search: Optional[str] = Query(None, description="Search query across model, brand, processor"),
    tier: Optional[str] = Query(None, description="Filter by price tier: Budget, Mid-Range, Premium, Flagship"),
    brand: Optional[str] = Query(None, description="Filter by brand name"),
    sort_by: Optional[str] = Query("price_asc", description="Sort criteria: price_asc, price_desc, ram_desc, rating_desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(15, ge=1, le=100, description="Items per page")
):
    if not DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="Dataset file not found")
    
    df = pd.read_csv(DATA_PATH)
    
    # Assign price tier
    df["tier"] = df["price"].apply(assign_price_tier)
    
    # Filter by search
    if search:
        s = search.lower().strip()
        mask = (
            df["model"].astype(str).str.lower().str.contains(s, na=False) |
            df["brand_name"].astype(str).str.lower().str.contains(s, na=False) |
            df["processor_brand"].astype(str).str.lower().str.contains(s, na=False)
        )
        df = df[mask]
        
    # Filter by tier
    if tier and tier.lower() != "all":
        df = df[df["tier"].str.lower() == tier.lower()]
        
    # Filter by brand
    if brand and brand.lower() != "all":
        df = df[df["brand_name"].str.lower() == brand.lower()]
        
    # Sorting
    if sort_by == "price_asc":
        df = df.sort_values(by="price", ascending=True)
    elif sort_by == "price_desc":
        df = df.sort_values(by="price", ascending=False)
    elif sort_by == "ram_desc":
        df = df.sort_values(by="ram_capacity", ascending=False)
    elif sort_by == "rating_desc":
        df = df.sort_values(by="rating", ascending=False)
        
    total_count = len(df)
    total_pages = max(1, (total_count + limit - 1) // limit)
    
    start_idx = (page - 1) * limit
    page_df = df.iloc[start_idx : start_idx + limit]
    
    records = []
    for _, row in page_df.iterrows():
        records.append({
            "model": str(row["model"]),
            "brand": str(row["brand_name"]).title(),
            "price_inr": int(row["price"]),
            "price_usd": round(float(row["price"]) / 83.0, 1),
            "tier": str(row["tier"]),
            "rating": float(row["rating"]) if pd.notna(row["rating"]) else 78.0,
            "has_5g": bool(row["has_5g"]) if pd.notna(row["has_5g"]) else False,
            "has_nfc": bool(row["has_nfc"]) if pd.notna(row["has_nfc"]) else False,
            "processor_brand": str(row["processor_brand"]).title() if pd.notna(row["processor_brand"]) else "Octa-Core",
            "processor_speed": float(row["processor_speed"]) if pd.notna(row["processor_speed"]) else 2.4,
            "ram_gb": int(row["ram_capacity"]) if pd.notna(row["ram_capacity"]) else 6,
            "storage_gb": int(row["internal_memory"]) if pd.notna(row["internal_memory"]) else 128,
            "battery_mah": int(row["battery_capacity"]) if pd.notna(row["battery_capacity"]) else 5000,
            "screen_size": float(row["screen_size"]) if pd.notna(row["screen_size"]) else 6.5,
            "refresh_rate": int(row["refresh_rate"]) if pd.notna(row["refresh_rate"]) else 60,
            "camera_rear": float(row["primary_camera_rear"]) if pd.notna(row["primary_camera_rear"]) else 50.0,
            "camera_front": float(row["primary_camera_front"]) if pd.notna(row["primary_camera_front"]) else 16.0
        })
        
    return {
        "total_records": total_count,
        "page": page,
        "total_pages": total_pages,
        "limit": limit,
        "records": records
    }
