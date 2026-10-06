import React, { useState, useEffect } from 'react';
import type { FeatureImportanceData } from '../types';
import { fetchFeatureImportance } from '../api';
import { Cpu, Activity, PieChart, TrendingUp } from 'lucide-react';

export const ExplainabilityView: React.FC = () => {
  const [data, setData] = useState<FeatureImportanceData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedTier, setSelectedTier] = useState<string>("Flagship");

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchFeatureImportance();
        setData(res);
      } catch (e) {
        console.error("Explainability load error:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading || !data) {
    return (
      <div className="p-12 text-center text-slate-400 flex items-center justify-center space-x-2">
        <Activity className="w-5 h-5 animate-spin text-indigo-400" />
        <span>Loading model explainability & feature importance...</span>
      </div>
    );
  }

  const top15 = data.ranked_features.slice(0, 15);
  const maxPerm = Math.max(...top15.map(f => f.permutation_mean));

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-indigo-400" />
          <h2 className="text-xl font-bold text-white">Model Explainability & Feature Importance</h2>
        </div>
        <p className="text-sm text-slate-400 mt-0.5">
          Permutation importance on test set (Macro F1 drop) & Multinomial Logistic log-odds directional weights.
        </p>
      </div>

      {/* Top 15 Permutation Importance Bar List */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: 7 Cols */}
        <div className="lg:col-span-7 p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
              <TrendingUp className="w-4 h-4 text-indigo-400" />
              <span>Top 15 Most Discriminative Features (Test Permutation)</span>
            </div>
            <span className="text-[11px] text-slate-400">Δ Test Macro F1</span>
          </div>

          <div className="space-y-2.5">
            {top15.map((item, idx) => {
              const barWidth = Math.max(8, (item.permutation_mean / maxPerm) * 100);
              return (
                <div key={item.feature} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-mono font-medium text-slate-200 flex items-center space-x-1.5">
                      <span className="text-slate-500 text-[10px]">#{idx + 1}</span>
                      <span>{item.feature}</span>
                      <span className="text-[10px] text-slate-400 bg-slate-800/60 px-1.5 py-0.2 rounded font-sans">
                        {item.group}
                      </span>
                    </span>
                    <span className="font-mono text-indigo-400 font-bold">
                      +{(item.permutation_mean * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="w-full bg-slate-800/60 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full"
                      style={{ width: `${barWidth}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: 5 Cols (Hardware Group Contribution & Logistic Weights) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Functional Group Breakdown */}
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
            <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
              <PieChart className="w-4 h-4 text-emerald-400" />
              <span>Functional Domain Contributions</span>
            </div>

            <div className="space-y-3">
              {Object.entries(data.grouped_importance).map(([group, val]) => (
                <div key={group} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-medium">{group}</span>
                    <span className="font-mono text-emerald-400 font-bold">{(val * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-emerald-500 h-full rounded-full"
                      style={{ width: `${val * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Directional Log-Odds Weights for Selected Category */}
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-slate-200">
                Directional Impact by Category
              </div>
              <select
                value={selectedTier}
                onChange={(e) => setSelectedTier(e.target.value)}
                className="text-xs bg-slate-950 border border-slate-700 rounded-lg px-2 py-1 text-slate-200 outline-none"
              >
                <option value="Budget">Budget</option>
                <option value="Mid-Range">Mid-Range</option>
                <option value="Premium">Premium</option>
                <option value="Flagship">Flagship</option>
              </select>
            </div>

            <div className="space-y-2">
              {Object.entries(data.logistic_regression_weights[selectedTier] || {})
                .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
                .slice(0, 6)
                .map(([feat, weight]) => {
                  const isPositive = weight > 0;
                  return (
                    <div key={feat} className="flex items-center justify-between text-xs p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                      <span className="font-mono text-slate-300 truncate max-w-[180px]">{feat}</span>
                      <span className={`font-mono font-bold ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
                        {isPositive ? `+${weight.toFixed(2)}` : weight.toFixed(2)}
                      </span>
                    </div>
                  );
                })}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
