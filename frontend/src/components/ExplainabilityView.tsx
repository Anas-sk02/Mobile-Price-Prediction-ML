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
      <div className="p-16 text-center text-slate-500 flex items-center justify-center space-x-2">
        <Activity className="w-5 h-5 animate-spin text-amber-700" />
        <span className="font-semibold text-sm">Loading model explainability & feature rankings...</span>
      </div>
    );
  }

  const top15 = data.ranked_features.slice(0, 15);
  const maxPerm = Math.max(...top15.map(f => f.permutation_mean));

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="luxury-card p-5">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-amber-800" />
          <h1 className="text-lg font-bold font-luxury text-slate-900">Feature Importance & Model Explainability</h1>
        </div>
        <p className="text-xs text-slate-500 mt-0.5">
          Empirical feature importance on unseen test data via model-agnostic Permutation Shuffling & Logistic log-odds weights.
        </p>
      </div>

      {/* Grid: Permutation Ranking (Left) & Domain Group Contribution (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: 7 Cols (Permutation Importance List) */}
        <div className="lg:col-span-7 luxury-card p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC]">
            <div className="flex items-center space-x-2 text-sm font-bold font-luxury text-slate-900">
              <TrendingUp className="w-4 h-4 text-amber-800" />
              <span>Top 15 Most Discriminative Features</span>
            </div>
            <span className="text-[11px] font-mono text-slate-500 font-semibold">Mean Δ Macro F1 Drop</span>
          </div>

          <div className="space-y-3">
            {top15.map((item, idx) => {
              const barWidth = Math.max(6, (item.permutation_mean / maxPerm) * 100);
              return (
                <div key={item.feature} className="space-y-1">
                  <div className="flex justify-between text-xs items-center">
                    <span className="font-mono font-bold text-slate-800 flex items-center space-x-2">
                      <span className="text-slate-400 text-[10px] w-4">#{idx + 1}</span>
                      <span className="font-semibold">{item.feature}</span>
                      <span className="text-[10px] text-slate-600 bg-[#FAF8F5] border border-[#EAE4DC] px-2 py-0.5 rounded font-sans font-medium">
                        {item.group}
                      </span>
                    </span>
                    <span className="font-mono text-amber-900 font-bold text-xs">
                      +{(item.permutation_mean * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="w-full bg-[#F5F0E8] h-2.5 rounded-full overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-amber-700 to-amber-900 h-full rounded-full transition-all duration-300"
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
          
          {/* Functional Domain Group Contribution */}
          <div className="luxury-card p-6 space-y-4">
            <div className="flex items-center space-x-2 text-sm font-bold font-luxury text-slate-900 pb-3 border-b border-[#EAE4DC]">
              <PieChart className="w-4 h-4 text-amber-800" />
              <span>Functional Domain Contribution</span>
            </div>

            <div className="space-y-3">
              {Object.entries(data.grouped_importance).map(([group, val]) => (
                <div key={group} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-700 font-semibold">{group}</span>
                    <span className="font-mono text-slate-900 font-bold">{(val * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-[#F5F0E8] h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-amber-600 to-amber-800 h-full rounded-full"
                      style={{ width: `${val * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Directional Log-Odds Impact */}
          <div className="luxury-card p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC]">
              <div className="text-sm font-bold font-luxury text-slate-900">
                Directional Impact by Tier
              </div>
              <select
                value={selectedTier}
                onChange={(e) => setSelectedTier(e.target.value)}
                className="text-xs bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg px-2.5 py-1 text-slate-800 font-semibold outline-none cursor-pointer focus:border-amber-700"
              >
                <option value="Budget">Budget Tier</option>
                <option value="Mid-Range">Mid-Range Tier</option>
                <option value="Premium">Premium Tier</option>
                <option value="Flagship">Flagship Tier</option>
              </select>
            </div>

            <div className="space-y-2">
              {Object.entries(data.logistic_regression_weights[selectedTier] || {})
                .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
                .slice(0, 6)
                .map(([feat, weight]) => {
                  const isPositive = weight > 0;
                  return (
                    <div key={feat} className="flex items-center justify-between text-xs p-2.5 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC]">
                      <span className="font-mono font-medium text-slate-800 truncate max-w-[180px]">{feat}</span>
                      <span className={`font-mono font-bold ${isPositive ? 'text-emerald-700' : 'text-rose-700'}`}>
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
