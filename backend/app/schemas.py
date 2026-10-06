"""
SmartPrice - API Request & Response Schemas
===========================================
Defines Pydantic models for single prediction, batch prediction,
model benchmarking, and feature importance explainability.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SmartphoneInput(BaseModel):
    brand_name: str = Field(..., example="samsung", description="Brand name (e.g. samsung, apple, xiaomi, oneplus, realme)")
    rating: Optional[float] = Field(80.0, ge=0.0, le=100.0, description="Overall user/reviewer rating")
    has_5g: bool = Field(True, description="Whether 5G connectivity is supported")
    has_nfc: bool = Field(False, description="Whether NFC is supported")
    has_ir_blaster: bool = Field(False, description="Whether IR blaster is available")
    processor_brand: Optional[str] = Field("snapdragon", description="Processor manufacturer (snapdragon, dimensity, helio, bionic, exynos, etc.)")
    num_cores: Optional[float] = Field(8.0, ge=1.0, le=16.0, description="Number of CPU cores")
    processor_speed: Optional[float] = Field(2.4, ge=0.5, le=5.0, description="Processor clock speed in GHz")
    battery_capacity: Optional[float] = Field(5000.0, ge=500.0, le=25000.0, description="Battery capacity in mAh")
    fast_charging_available: int = Field(1, ge=0, le=1, description="1 if fast charging supported, else 0")
    fast_charging: Optional[float] = Field(33.0, ge=0.0, le=300.0, description="Charging wattage in Watts")
    ram_capacity: float = Field(..., ge=1.0, le=64.0, description="RAM capacity in GB")
    internal_memory: float = Field(..., ge=8.0, le=2048.0, description="Internal storage in GB")
    screen_size: float = Field(6.6, ge=3.0, le=12.0, description="Display screen diagonal size in inches")
    refresh_rate: int = Field(120, ge=30, le=360, description="Display refresh rate in Hz")
    resolution: Optional[str] = Field("1080 x 2400", description="Display resolution string (e.g., '1080 x 2400' or '1440 x 3200')")
    num_rear_cameras: int = Field(3, ge=1, le=6, description="Number of rear camera sensors")
    num_front_cameras: Optional[float] = Field(1.0, ge=1.0, le=4.0, description="Number of front selfie camera sensors")
    os: Optional[str] = Field("android", description="Operating system (android, ios, other)")
    primary_camera_rear: float = Field(50.0, ge=2.0, le=300.0, description="Primary rear camera megapixel resolution")
    primary_camera_front: Optional[float] = Field(16.0, ge=0.3, le=100.0, description="Primary front selfie camera megapixel resolution")
    extended_memory_available: int = Field(1, ge=0, le=1, description="1 if expandable memory slot exists, else 0")
    extended_upto: Optional[float] = Field(1024.0, ge=0.0, le=4096.0, description="Maximum expandable storage capacity in GB")


class ClassProbability(BaseModel):
    category: str
    probability: float
    percentage: str
    price_range: str


class PredictionResponse(BaseModel):
    model_used: str
    predicted_category: str
    predicted_category_index: int
    confidence_score: float
    confidence_percentage: str
    estimated_price_range: str
    probabilities: List[ClassProbability]
    engineered_features: Dict[str, Any]


class BatchPredictionRequest(BaseModel):
    smartphones: List[SmartphoneInput]


class BatchPredictionResponse(BaseModel):
    total_samples: int
    predictions: List[PredictionResponse]


class ModelComparisonPrediction(BaseModel):
    model_key: str
    model_name: str
    predicted_category: str
    confidence_score: float
    probabilities: List[ClassProbability]


class ModelComparisonResponse(BaseModel):
    input_summary: Dict[str, Any]
    models_comparison: List[ModelComparisonPrediction]
    consensus_category: str
    consensus_agreement: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    champion_model: str
    loaded_models: List[str]
