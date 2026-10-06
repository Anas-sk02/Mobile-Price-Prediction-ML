export interface SmartphoneSpecs {
  brand_name: string;
  rating: number;
  has_5g: boolean;
  has_nfc: boolean;
  has_ir_blaster: boolean;
  processor_brand: string;
  num_cores: number;
  processor_speed: number;
  battery_capacity: number;
  fast_charging_available: number;
  fast_charging: number;
  ram_capacity: number;
  internal_memory: number;
  screen_size: number;
  refresh_rate: number;
  resolution: string;
  num_rear_cameras: number;
  num_front_cameras: number;
  os: string;
  primary_camera_rear: number;
  primary_camera_front: number;
  extended_memory_available: number;
  extended_upto: number;
}

export interface ClassProbability {
  category: "Budget" | "Mid-Range" | "Premium" | "Flagship";
  probability: number;
  percentage: string;
  price_range: string;
}

export interface PredictionResult {
  model_used: string;
  predicted_category: "Budget" | "Mid-Range" | "Premium" | "Flagship";
  predicted_category_index: number;
  confidence_score: number;
  confidence_percentage: string;
  estimated_price_range: string;
  probabilities: ClassProbability[];
  engineered_features: {
    resolution_parsed: string;
    pixel_count: number;
    aspect_ratio: number;
    ppi: number;
    total_cameras: number;
    screen_to_battery_ratio: number;
    ram_to_storage_ratio: number;
    performance_score: number;
  };
}

export interface ModelComparisonResult {
  input_summary: Record<string, string>;
  models_comparison: {
    model_key: string;
    model_name: string;
    predicted_category: "Budget" | "Mid-Range" | "Premium" | "Flagship";
    confidence_score: number;
    probabilities: ClassProbability[];
  }[];
  consensus_category: string;
  consensus_agreement: string;
}

export interface ModelMetricsData {
  champion_model: string;
  champion_details: {
    name: string;
    test_accuracy: number;
    f1_macro: number;
    roc_auc_macro: number;
    best_params: Record<string, any>;
  };
  all_tuned_models: Record<string, {
    name: string;
    best_params: Record<string, any>;
    best_cv_score: number;
    test_accuracy: number;
    f1_macro: number;
    f1_weighted: number;
    precision_macro: number;
    recall_macro: number;
    roc_auc_macro: number;
    classification_report: Record<string, any>;
    confusion_matrix: number[][];
  }>;
}

export interface FeatureImportanceData {
  ranked_features: {
    feature: string;
    group: string;
    permutation_mean: number;
    permutation_std: number;
    mdi_importance: number;
  }[];
  grouped_importance: Record<string, number>;
  logistic_regression_weights: Record<string, Record<string, number>>;
}
