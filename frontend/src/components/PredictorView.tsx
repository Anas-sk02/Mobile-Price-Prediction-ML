import React, { useState, useEffect } from 'react';
import type { SmartphoneSpecs, PredictionResult } from '../types';
import { PRESET_SMARTPHONES, predictPriceCategory } from '../api';
import { 
  Sparkles, ShieldCheck, 
  Smartphone, Cpu, Camera, Monitor, BarChart2, AlertCircle
} from 'lucide-react';

interface PredictorViewProps {
  onCompareWithSpecs: (specs: SmartphoneSpecs) => void;
}

export const PredictorView: React.FC<PredictorViewProps> = ({ onCompareWithSpecs }) => {
  const [specs, setSpecs] = useState<SmartphoneSpecs>(PRESET_SMARTPHONES.flagship.specs);
  const [activePreset, setActivePreset] = useState<string>('flagship');
  const [selectedModel, setSelectedModel] = useState<string>('champion');
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePresetSelect = (key: string) => {
    setActivePreset(key);
    setSpecs(PRESET_SMARTPHONES[key].specs);
  };

  const handlePredict = async () => {
    setError(null);
    try {
      const res = await predictPriceCategory(specs, selectedModel);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to generate prediction');
    }
  };

  // Run prediction on initial mount or preset change
  useEffect(() => {
    handlePredict();
  }, [specs, selectedModel]);

  // Real-time derived feature helper calculations
  const parsedWidth = specs.resolution.includes('x') ? parseInt(specs.resolution.split('x')[0]) : 1080;
  const parsedHeight = specs.resolution.includes('x') ? parseInt(specs.resolution.split('x')[1]) : 2400;
  const diagonalPx = Math.sqrt(parsedWidth ** 2 + parsedHeight ** 2);
  const calculatedPpi = Math.round(diagonalPx / Math.max(specs.screen_size, 3.0));
  const calculatedPerfScore = Math.round((specs.num_cores || 8) * (specs.processor_speed || 2.4) * specs.ram_capacity);

  const getCategoryColor = (cat: string) => {
    switch (cat) {
      case 'Flagship': return { bg: 'bg-red-500/15', text: 'text-red-400', border: 'border-red-500/30', bar: 'bg-red-500' };
      case 'Premium': return { bg: 'bg-amber-500/15', text: 'text-amber-400', border: 'border-amber-500/30', bar: 'bg-amber-500' };
      case 'Mid-Range': return { bg: 'bg-emerald-500/15', text: 'text-emerald-400', border: 'border-emerald-500/30', bar: 'bg-emerald-500' };
      default: return { bg: 'bg-blue-500/15', text: 'text-blue-400', border: 'border-blue-500/30', bar: 'bg-blue-500' };
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Preset Selector */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <h2 className="text-xl font-bold text-white">Interactive Price Category Predictor</h2>
          </div>
          <p className="text-sm text-slate-400 mt-0.5">
            Configure technical hardware specifications or load standard benchmark device presets.
          </p>
        </div>

        {/* Quick Presets */}
        <div className="flex flex-wrap gap-2">
          {Object.entries(PRESET_SMARTPHONES).map(([key, item]) => (
            <button
              key={key}
              onClick={() => handlePresetSelect(key)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all flex items-center space-x-1.5 border ${
                activePreset === key
                  ? 'bg-indigo-600/30 border-indigo-500 text-indigo-300 shadow-sm'
                  : 'bg-slate-800/60 border-slate-700/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Smartphone className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Form Inputs (Left) & Live Prediction Card (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Form: 7 Columns */}
        <div className="lg:col-span-7 space-y-5">
          
          {/* Section 1: Core Performance & Memory */}
          <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
                <Cpu className="w-4 h-4 text-indigo-400" />
                <span>Processor & Memory Specs</span>
              </div>
              <span className="text-[11px] font-mono text-indigo-400 px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20">
                Perf Score: {calculatedPerfScore}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* RAM Capacity Slider */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">RAM Capacity</span>
                  <span className="text-indigo-400 font-bold">{specs.ram_capacity} GB</span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="18"
                  step="2"
                  value={specs.ram_capacity}
                  onChange={(e) => setSpecs({ ...specs, ram_capacity: parseFloat(e.target.value) })}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              {/* Internal Storage Slider */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">Internal Storage</span>
                  <span className="text-indigo-400 font-bold">{specs.internal_memory} GB</span>
                </div>
                <input
                  type="range"
                  min="16"
                  max="1024"
                  step="16"
                  value={specs.internal_memory}
                  onChange={(e) => setSpecs({ ...specs, internal_memory: parseFloat(e.target.value) })}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              {/* Processor Brand */}
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Processor Series</label>
                <select
                  value={specs.processor_brand}
                  onChange={(e) => setSpecs({ ...specs, processor_brand: e.target.value })}
                  className="w-full text-xs bg-slate-950 border border-slate-700/80 rounded-xl px-3 py-2 text-slate-200 focus:border-indigo-500 outline-none"
                >
                  <option value="snapdragon">Qualcomm Snapdragon</option>
                  <option value="dimensity">MediaTek Dimensity</option>
                  <option value="bionic">Apple Bionic / Silicon</option>
                  <option value="exynos">Samsung Exynos</option>
                  <option value="helio">MediaTek Helio</option>
                  <option value="google">Google Tensor</option>
                  <option value="unisoc">Unisoc</option>
                </select>
              </div>

              {/* Processor Speed */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">Clock Speed</span>
                  <span className="text-indigo-400 font-bold">{specs.processor_speed} GHz</span>
                </div>
                <input
                  type="range"
                  min="1.4"
                  max="3.4"
                  step="0.1"
                  value={specs.processor_speed}
                  onChange={(e) => setSpecs({ ...specs, processor_speed: parseFloat(e.target.value) })}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>
            </div>
          </div>

          {/* Section 2: Display & Screen */}
          <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
                <Monitor className="w-4 h-4 text-emerald-400" />
                <span>Display & Visuals</span>
              </div>
              <span className="text-[11px] font-mono text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
                Density: {calculatedPpi} PPI
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Screen Size */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">Screen Size</span>
                  <span className="text-emerald-400 font-bold">{specs.screen_size}"</span>
                </div>
                <input
                  type="range"
                  min="4.7"
                  max="7.2"
                  step="0.1"
                  value={specs.screen_size}
                  onChange={(e) => setSpecs({ ...specs, screen_size: parseFloat(e.target.value) })}
                  className="w-full accent-emerald-500 cursor-pointer"
                />
              </div>

              {/* Refresh Rate */}
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Refresh Rate</label>
                <select
                  value={specs.refresh_rate}
                  onChange={(e) => setSpecs({ ...specs, refresh_rate: parseInt(e.target.value) })}
                  className="w-full text-xs bg-slate-950 border border-slate-700/80 rounded-xl px-3 py-2 text-slate-200 focus:border-emerald-500 outline-none"
                >
                  <option value={60}>60 Hz (Standard)</option>
                  <option value={90}>90 Hz (Smooth)</option>
                  <option value={120}>120 Hz (High Refresh)</option>
                  <option value={144}>144 Hz (Gaming)</option>
                </select>
              </div>

              {/* Resolution String */}
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Resolution</label>
                <select
                  value={specs.resolution}
                  onChange={(e) => setSpecs({ ...specs, resolution: e.target.value })}
                  className="w-full text-xs bg-slate-950 border border-slate-700/80 rounded-xl px-3 py-2 text-slate-200 focus:border-emerald-500 outline-none"
                >
                  <option value="720 x 1600">HD+ (720 x 1600)</option>
                  <option value="1080 x 2400">FHD+ (1080 x 2400)</option>
                  <option value="1080 x 2412">FHD+ Curved (1080 x 2412)</option>
                  <option value="1170 x 2532">Super Retina (1170 x 2532)</option>
                  <option value="1440 x 3088">QHD+ (1440 x 3088)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Section 3: Camera, Battery & Connectivity */}
          <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
            <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
              <Camera className="w-4 h-4 text-amber-400" />
              <span>Camera, Power & Connectivity</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Primary Camera Rear */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">Rear Sensor</span>
                  <span className="text-amber-400 font-bold">{specs.primary_camera_rear} MP</span>
                </div>
                <input
                  type="range"
                  min="12"
                  max="200"
                  step="4"
                  value={specs.primary_camera_rear}
                  onChange={(e) => setSpecs({ ...specs, primary_camera_rear: parseFloat(e.target.value) })}
                  className="w-full accent-amber-500 cursor-pointer"
                />
              </div>

              {/* Fast Charging Wattage */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">Charging Speed</span>
                  <span className="text-amber-400 font-bold">{specs.fast_charging} W</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="120"
                  step="5"
                  value={specs.fast_charging}
                  onChange={(e) => setSpecs({ ...specs, fast_charging: parseFloat(e.target.value) })}
                  className="w-full accent-amber-500 cursor-pointer"
                />
              </div>

              {/* Battery Capacity */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">Battery</span>
                  <span className="text-amber-400 font-bold">{specs.battery_capacity} mAh</span>
                </div>
                <input
                  type="range"
                  min="3000"
                  max="6000"
                  step="100"
                  value={specs.battery_capacity}
                  onChange={(e) => setSpecs({ ...specs, battery_capacity: parseFloat(e.target.value) })}
                  className="w-full accent-amber-500 cursor-pointer"
                />
              </div>
            </div>

            {/* Toggle Chips */}
            <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-slate-800">
              <label className="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={specs.has_5g}
                  onChange={(e) => setSpecs({ ...specs, has_5g: e.target.checked })}
                  className="rounded accent-indigo-500"
                />
                <span>5G Network Support</span>
              </label>

              <label className="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={specs.has_nfc}
                  onChange={(e) => setSpecs({ ...specs, has_nfc: e.target.checked })}
                  className="rounded accent-indigo-500"
                />
                <span>NFC Contactless</span>
              </label>

              <label className="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={specs.has_ir_blaster}
                  onChange={(e) => setSpecs({ ...specs, has_ir_blaster: e.target.checked })}
                  className="rounded accent-indigo-500"
                />
                <span>IR Blaster</span>
              </label>
            </div>
          </div>

        </div>

        {/* Right Output: 5 Columns (Live Prediction Dashboard) */}
        <div className="lg:col-span-5 space-y-5">
          
          {/* Active Model Selector */}
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
            <span className="text-xs text-slate-400">Inference Model:</span>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="text-xs font-semibold bg-slate-950 border border-indigo-500/40 rounded-xl px-3 py-1.5 text-indigo-300 outline-none"
            >
              <option value="champion">Random Forest (Champion)</option>
              <option value="svm">Support Vector Machine (RBF)</option>
              <option value="knn">K-Nearest Neighbors</option>
              <option value="logistic_regression">Logistic Regression</option>
            </select>
          </div>

          {/* Main Prediction Result Card */}
          {result && (
            <div className="p-6 rounded-3xl bg-gradient-to-b from-slate-900/90 to-slate-950/90 border border-slate-800 shadow-xl space-y-5">
              
              <div className="flex items-center justify-between">
                <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">
                  Predicted Category
                </span>
                <span className="text-xs font-mono text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded-lg">
                  {result.model_used}
                </span>
              </div>

              {/* Big Tier Badge */}
              {(() => {
                const style = getCategoryColor(result.predicted_category);
                return (
                  <div className={`p-5 rounded-2xl ${style.bg} border ${style.border} text-center space-y-1`}>
                    <div className="flex items-center justify-center space-x-2">
                      <ShieldCheck className={`w-7 h-7 ${style.text}`} />
                      <span className={`text-3xl font-extrabold tracking-tight ${style.text}`}>
                        {result.predicted_category}
                      </span>
                    </div>
                    <p className="text-sm font-semibold text-slate-200">
                      Estimated Market Bracket: {result.estimated_price_range}
                    </p>
                    <p className="text-xs text-slate-400">
                      Model Confidence: <strong className="text-white">{result.confidence_percentage}</strong>
                    </p>
                  </div>
                );
              })()}

              {/* Class Probability Distribution Bars */}
              <div className="space-y-3">
                <span className="text-xs font-semibold text-slate-300">
                  Multi-Class Softmax Probability Distribution:
                </span>

                <div className="space-y-2">
                  {result.probabilities.map((item) => {
                    const style = getCategoryColor(item.category);
                    const isWinner = item.category === result.predicted_category;
                    return (
                      <div key={item.category} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className={isWinner ? "font-bold text-white" : "text-slate-400"}>
                            {item.category} ({item.price_range})
                          </span>
                          <span className={isWinner ? `font-bold ${style.text}` : "text-slate-400"}>
                            {item.percentage}
                          </span>
                        </div>
                        <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all duration-500 ${style.bar}`}
                            style={{ width: item.percentage }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Compare Across All 4 Models Button */}
              <button
                onClick={() => onCompareWithSpecs(specs)}
                className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-lg shadow-indigo-600/30 flex items-center justify-center space-x-2 cursor-pointer"
              >
                <BarChart2 className="w-4 h-4" />
                <span>Compare Specs Across All 4 Models</span>
              </button>

            </div>
          )}

          {error && (
            <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4" />
              <span>{error}</span>
            </div>
          )}

        </div>

      </div>
    </div>
  );
};
