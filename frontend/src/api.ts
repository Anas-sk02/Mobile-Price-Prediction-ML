import type { SmartphoneSpecs, PredictionResult, ModelComparisonResult, ModelMetricsData, FeatureImportanceData } from './types';

const API_BASE = '/api';

export const PRESET_SMARTPHONES: Record<string, { label: string; tag: string; specs: SmartphoneSpecs }> = {
  flagship: {
    label: "Samsung Galaxy S23 Ultra",
    tag: "Flagship (> ₹50k)",
    specs: {
      brand_name: "samsung",
      rating: 88.0,
      has_5g: true,
      has_nfc: true,
      has_ir_blaster: false,
      processor_brand: "snapdragon",
      num_cores: 8.0,
      processor_speed: 3.2,
      battery_capacity: 5000.0,
      fast_charging_available: 1,
      fast_charging: 45.0,
      ram_capacity: 12.0,
      internal_memory: 256.0,
      screen_size: 6.8,
      refresh_rate: 120,
      resolution: "1440 x 3088",
      num_rear_cameras: 4,
      num_front_cameras: 1.0,
      os: "android",
      primary_camera_rear: 200.0,
      primary_camera_front: 12.0,
      extended_memory_available: 0,
      extended_upto: 0.0
    }
  },
  premium: {
    label: "OnePlus 11R 5G",
    tag: "Premium (₹30k–₹50k)",
    specs: {
      brand_name: "oneplus",
      rating: 85.0,
      has_5g: true,
      has_nfc: true,
      has_ir_blaster: false,
      processor_brand: "snapdragon",
      num_cores: 8.0,
      processor_speed: 3.2,
      battery_capacity: 5000.0,
      fast_charging_available: 1,
      fast_charging: 100.0,
      ram_capacity: 8.0,
      internal_memory: 128.0,
      screen_size: 6.7,
      refresh_rate: 120,
      resolution: "1080 x 2412",
      num_rear_cameras: 3,
      num_front_cameras: 1.0,
      os: "android",
      primary_camera_rear: 50.0,
      primary_camera_front: 16.0,
      extended_memory_available: 0,
      extended_upto: 0.0
    }
  },
  midrange: {
    label: "Xiaomi Redmi Note 12 Pro",
    tag: "Mid-Range (₹15k–₹30k)",
    specs: {
      brand_name: "xiaomi",
      rating: 82.0,
      has_5g: true,
      has_nfc: false,
      has_ir_blaster: true,
      processor_brand: "dimensity",
      num_cores: 8.0,
      processor_speed: 2.6,
      battery_capacity: 5000.0,
      fast_charging_available: 1,
      fast_charging: 67.0,
      ram_capacity: 6.0,
      internal_memory: 128.0,
      screen_size: 6.67,
      refresh_rate: 120,
      resolution: "1080 x 2400",
      num_rear_cameras: 3,
      num_front_cameras: 1.0,
      os: "android",
      primary_camera_rear: 50.0,
      primary_camera_front: 16.0,
      extended_memory_available: 0,
      extended_upto: 0.0
    }
  },
  budget: {
    label: "Vivo Y16 (Budget Entry)",
    tag: "Budget (<= ₹15k)",
    specs: {
      brand_name: "vivo",
      rating: 65.0,
      has_5g: false,
      has_nfc: false,
      has_ir_blaster: false,
      processor_brand: "helio",
      num_cores: 8.0,
      processor_speed: 2.3,
      battery_capacity: 5000.0,
      fast_charging_available: 1,
      fast_charging: 10.0,
      ram_capacity: 3.0,
      internal_memory: 32.0,
      screen_size: 6.51,
      refresh_rate: 60,
      resolution: "720 x 1600",
      num_rear_cameras: 2,
      num_front_cameras: 1.0,
      os: "android",
      primary_camera_rear: 13.0,
      primary_camera_front: 5.0,
      extended_memory_available: 1,
      extended_upto: 1024.0
    }
  }
};

export async function checkApiHealth(): Promise<{ status: string; champion_model: string }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('API server unavailable');
  return res.json();
}

export async function predictPriceCategory(specs: SmartphoneSpecs, model = "champion"): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE}/predict?model=${model}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(specs)
  });
  if (!res.ok) throw new Error('Prediction request failed');
  return res.json();
}

export async function compareAllModels(specs: SmartphoneSpecs): Promise<ModelComparisonResult> {
  const res = await fetch(`${API_BASE}/predict/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(specs)
  });
  if (!res.ok) throw new Error('Model comparison request failed');
  return res.json();
}

export async function fetchModelMetrics(): Promise<ModelMetricsData> {
  const res = await fetch(`${API_BASE}/models/metrics`);
  if (!res.ok) throw new Error('Failed to fetch model metrics');
  return res.json();
}

export async function fetchRocCurves(): Promise<any> {
  const res = await fetch(`${API_BASE}/models/roc-curves`);
  if (!res.ok) throw new Error('Failed to fetch ROC curves');
  return res.json();
}

export async function fetchFeatureImportance(): Promise<FeatureImportanceData> {
  const res = await fetch(`${API_BASE}/models/feature-importance`);
  if (!res.ok) throw new Error('Failed to fetch feature importance');
  return res.json();
}

export async function fetchDatasetSummary(): Promise<any> {
  const res = await fetch(`${API_BASE}/analytics/dataset-summary`);
  if (!res.ok) throw new Error('Failed to fetch dataset summary');
  return res.json();
}

export async function fetchEdaInsights(): Promise<any> {
  const res = await fetch(`${API_BASE}/analytics/eda-insights`);
  if (!res.ok) throw new Error('Failed to fetch EDA insights');
  return res.json();
}
