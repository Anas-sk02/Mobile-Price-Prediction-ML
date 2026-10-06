"""
SmartPrice - ML Inference & Prediction Engine
=============================================
Loads the Scikit-learn ColumnTransformer pipeline and trained models,
computes real-time derived features, and generates single/batch predictions.
"""

import re
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "ml" / "models"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

CLASS_MAPPING = {0: "Budget", 1: "Mid-Range", 2: "Premium", 3: "Flagship"}
PRICE_RANGES = {
    "Budget": "₹0 – ₹15,000",
    "Mid-Range": "₹15,001 – ₹30,000",
    "Premium": "₹30,001 – ₹50,000",
    "Flagship": "> ₹50,000"
}


class ModelEngine:
    def __init__(self):
        self.preprocessor_pkg = None
        self.preprocessor = None
        self.numerical_cols = []
        self.categorical_cols = []
        self.champion_meta = None
        self.champion_model = None
        self.all_models = {}
        self._is_loaded = False

    def load(self):
        if self._is_loaded:
            return

        preprocessor_path = MODEL_DIR / "preprocessor.joblib"
        if not preprocessor_path.exists():
            raise FileNotFoundError(f"Preprocessor not found at {preprocessor_path}")

        self.preprocessor_pkg = joblib.load(preprocessor_path)
        self.preprocessor = self.preprocessor_pkg["pipeline"]
        self.numerical_cols = self.preprocessor_pkg["numerical_features"]
        self.categorical_cols = self.preprocessor_pkg["categorical_features"]

        # Load Champion Model
        best_path = MODEL_DIR / "best_model.joblib"
        if not best_path.exists():
            raise FileNotFoundError(f"Champion model not found at {best_path}")
        self.champion_meta = joblib.load(best_path)
        self.champion_model = self.champion_meta["model"]

        # Load all 4 models for side-by-side comparison
        model_files = {
            "random_forest": ("Random Forest", MODEL_DIR / "tuned_random_forest.joblib"),
            "svm": ("Support Vector Machine", MODEL_DIR / "tuned_svm.joblib"),
            "knn": ("K-Nearest Neighbors", MODEL_DIR / "tuned_knn.joblib"),
            "logistic_regression": ("Logistic Regression", MODEL_DIR / "tuned_logistic_regression.joblib")
        }

        for k, (name, path) in model_files.items():
            if path.exists():
                self.all_models[k] = {
                    "name": name,
                    "model": joblib.load(path)
                }

        self._is_loaded = True
        print(f"[ModelEngine] Loaded preprocessor and {len(self.all_models)} models successfully.")

    @staticmethod
    def parse_resolution(res_str: str) -> Tuple[int, int]:
        if not isinstance(res_str, str) or not res_str.strip():
            return 1080, 2400
        cleaned = res_str.replace('\u2009', ' ').replace('&nbsp;', ' ').strip()
        match = re.findall(r'(\d+)', cleaned)
        if len(match) >= 2:
            v1, v2 = int(match[0]), int(match[1])
            return min(v1, v2), max(v1, v2)
        return 1080, 2400

    def preprocess_input(self, raw_input: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Applies domain logic & derived feature calculations matching training pipeline."""
        df = pd.DataFrame([raw_input])

        # 1. Boolean normalization
        for b_col in ['has_5g', 'has_nfc', 'has_ir_blaster']:
            if b_col in df.columns:
                df[b_col] = df[b_col].astype(str).str.strip().str.lower().map({'true': 1, '1': 1, 'false': 0, '0': 0}).fillna(0).astype(int)
            else:
                df[b_col] = 0

        # 2. Categorical grouping
        brand_raw = str(df.get('brand_name', ['samsung'])[0]).strip().lower()
        frequent_brands = ['xiaomi', 'samsung', 'vivo', 'realme', 'oppo', 'poco', 'motorola', 'oneplus', 'apple', 'iqoo', 'honor', 'huawei', 'nokia', 'google', 'techno', 'infinix']
        df['brand_grouped'] = brand_raw if brand_raw in frequent_brands else 'other_brand'

        proc_raw = str(df.get('processor_brand', ['snapdragon'])[0]).strip().lower()
        frequent_procs = ['snapdragon', 'helio', 'dimensity', 'exynos', 'bionic', 'unisoc', 'google', 'kirin', 'tiger']
        df['processor_grouped'] = proc_raw if proc_raw in frequent_procs else 'other_proc'

        os_raw = str(df.get('os', ['android'])[0]).strip().lower()
        df['os_grouped'] = os_raw if os_raw in ['android', 'ios'] else 'other_os'

        # 3. Resolution parsing & geometric features
        res_str = str(df.get('resolution', ['1080 x 2400'])[0])
        w, h = self.parse_resolution(res_str)
        df['resolution_width'] = w
        df['resolution_height'] = h
        df['pixel_count'] = w * h
        df['aspect_ratio'] = round(h / max(w, 1), 2)

        screen_size = float(df.get('screen_size', [6.6])[0])
        diagonal = np.sqrt(w**2 + h**2)
        df['ppi'] = round(diagonal / max(screen_size, 3.0), 1)

        # 4. Domain interaction features
        num_front = float(df.get('num_front_cameras', [1.0])[0]) if pd.notnull(df.get('num_front_cameras', [1.0])[0]) else 1.0
        num_rear = float(df.get('num_rear_cameras', [3])[0])
        df['num_front_cameras'] = num_front
        df['total_cameras'] = num_rear + num_front

        bat_cap = float(df.get('battery_capacity', [5000.0])[0]) if pd.notnull(df.get('battery_capacity', [5000.0])[0]) else 5000.0
        df['screen_to_battery_ratio'] = round(bat_cap / max(screen_size, 3.0), 1)

        ram = float(df.get('ram_capacity', [6.0])[0])
        internal_mem = float(df.get('internal_memory', [128.0])[0])
        df['ram_to_storage_ratio'] = round(ram / max(internal_mem, 8.0), 4)

        cores = float(df.get('num_cores', [8.0])[0]) if pd.notnull(df.get('num_cores', [8.0])[0]) else 8.0
        speed = float(df.get('processor_speed', [2.4])[0]) if pd.notnull(df.get('processor_speed', [2.4])[0]) else 2.4
        df['performance_score'] = round(cores * speed * ram, 2)

        engineered_meta = {
            "resolution_parsed": f"{w} x {h}",
            "pixel_count": int(w * h),
            "aspect_ratio": round(h / max(w, 1), 2),
            "ppi": round(diagonal / max(screen_size, 3.0), 1),
            "total_cameras": int(num_rear + num_front),
            "screen_to_battery_ratio": round(bat_cap / max(screen_size, 3.0), 1),
            "ram_to_storage_ratio": round(ram / max(internal_mem, 8.0), 4),
            "performance_score": round(cores * speed * ram, 2)
        }

        # Select all features expected by ColumnTransformer
        all_cols = self.numerical_cols + self.categorical_cols
        for col in all_cols:
            if col not in df.columns:
                df[col] = np.nan

        return df[all_cols], engineered_meta

    def predict_single(self, input_dict: Dict[str, Any], model_key: str = "champion") -> Dict[str, Any]:
        self.load()
        df_prepared, eng_meta = self.preprocess_input(input_dict)
        X_trans = self.preprocessor.transform(df_prepared)

        if model_key == "champion" or model_key not in self.all_models:
            model = self.champion_model
            model_display_name = self.champion_meta["display_name"]
        else:
            model = self.all_models[model_key]["model"]
            model_display_name = self.all_models[model_key]["name"]

        pred_idx = int(model.predict(X_trans)[0])
        pred_category = CLASS_MAPPING[pred_idx]

        # Probabilities
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_trans)[0]
        elif hasattr(model, "decision_function"):
            decision = model.decision_function(X_trans)[0]
            exp_d = np.exp(decision - np.max(decision))
            proba = exp_d / np.sum(exp_d)
        else:
            proba = np.zeros(4)
            proba[pred_idx] = 1.0

        confidence = float(proba[pred_idx])
        prob_list = []
        for idx in range(4):
            cat_name = CLASS_MAPPING[idx]
            p_val = float(proba[idx])
            prob_list.append({
                "category": cat_name,
                "probability": round(p_val, 4),
                "percentage": f"{p_val * 100:.1f}%",
                "price_range": PRICE_RANGES[cat_name]
            })

        return {
            "model_used": model_display_name,
            "predicted_category": pred_category,
            "predicted_category_index": pred_idx,
            "confidence_score": round(confidence, 4),
            "confidence_percentage": f"{confidence * 100:.1f}%",
            "estimated_price_range": PRICE_RANGES[pred_category],
            "probabilities": prob_list,
            "engineered_features": eng_meta
        }

    def compare_all_models(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        self.load()
        df_prepared, _ = self.preprocess_input(input_dict)
        X_trans = self.preprocessor.transform(df_prepared)

        comparison = []
        votes = []

        for m_key, m_info in self.all_models.items():
            model = m_info["model"]
            pred_idx = int(model.predict(X_trans)[0])
            pred_cat = CLASS_MAPPING[pred_idx]
            votes.append(pred_cat)

            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_trans)[0]
            elif hasattr(model, "decision_function"):
                decision = model.decision_function(X_trans)[0]
                exp_d = np.exp(decision - np.max(decision))
                proba = exp_d / np.sum(exp_d)
            else:
                proba = np.zeros(4)
                proba[pred_idx] = 1.0

            conf = float(proba[pred_idx])
            prob_list = []
            for idx in range(4):
                c_name = CLASS_MAPPING[idx]
                p_val = float(proba[idx])
                prob_list.append({
                    "category": c_name,
                    "probability": round(p_val, 4),
                    "percentage": f"{p_val * 100:.1f}%",
                    "price_range": PRICE_RANGES[c_name]
                })

            comparison.append({
                "model_key": m_key,
                "model_name": m_info["name"],
                "predicted_category": pred_cat,
                "confidence_score": round(conf, 4),
                "probabilities": prob_list
            })

        # Consensus determination
        from collections import Counter
        vote_counts = Counter(votes)
        consensus_cat, max_votes = vote_counts.most_common(1)[0]
        consensus_agreement = f"{max_votes}/{len(self.all_models)} Models Agree ({max_votes/len(self.all_models)*100:.0f}%)"

        return {
            "input_summary": {
                "brand": input_dict.get("brand_name"),
                "ram": f"{input_dict.get('ram_capacity')} GB",
                "storage": f"{input_dict.get('internal_memory')} GB",
                "processor_speed": f"{input_dict.get('processor_speed')} GHz",
                "refresh_rate": f"{input_dict.get('refresh_rate')} Hz"
            },
            "models_comparison": comparison,
            "consensus_category": consensus_cat,
            "consensus_agreement": consensus_agreement
        }


# Singleton engine instance
engine = ModelEngine()
