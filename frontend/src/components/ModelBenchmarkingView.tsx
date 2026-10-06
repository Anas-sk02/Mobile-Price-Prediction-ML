import React, { useState, useEffect } from 'react';
import type { SmartphoneSpecs, ModelComparisonResult, ModelMetricsData } from '../types';
import { fetchModelMetrics, compareAllModels } from '../api';
import { Layers, Award, BarChart3, ShieldCheck, Activity } from 'lucide-react';

interface BenchmarkingProps {
  currentSpecs: SmartphoneSpecs;
}

export const ModelBenchmarkingView: React.FC<BenchmarkingProps> = ({ currentSpecs }) => {
  const [metrics, setMetrics] = useState<ModelMetricsData | null>(null);
  const [comparison, setComparison] = useState<ModelComparisonResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function load() {
      try {
        const [metricsData, compData] = await Promise.all([
          fetchModelMetrics(),
          compareAllModels(currentSpecs)
        ]);
        setMetrics(metricsData);
        setComparison(compData);
      } catch (e) {
        console.error("Benchmarking load error:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [currentSpecs]);

  const getTierColor = (cat: string) => {
    switch (cat) {
      case 'Flagship': return 'text-red-400 bg-red-500/10 border-red-500/30';
      case 'Premium': return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'Mid-Range': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      default: return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
    }
  };

  if (loading || !metrics) {
    return (
      <div className="p-12 text-center text-slate-400 flex items-center justify-center space-x-2">
        <Activity className="w-5 h-5 animate-spin text-indigo-400" />
        <span>Loading 4-model benchmarking metrics...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Layers className="w-5 h-5 text-indigo-400" />
            <h2 className="text-xl font-bold text-white">4-Model Classification Lab & Consensus</h2>
          </div>
          <p className="text-sm text-slate-400 mt-0.5">
            Compare Random Forest, SVM, KNN, and Logistic Regression on identical smartphone hardware.
          </p>
        </div>

        {comparison && (
          <div className="flex items-center space-x-3 px-4 py-2 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
            <ShieldCheck className="w-5 h-5 text-indigo-400" />
            <div>
              <div className="text-xs text-slate-400">Consensus Category</div>
              <div className="text-sm font-bold text-white">
                {comparison.consensus_category} ({comparison.consensus_agreement})
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Model Live Consensus Cards */}
      {comparison && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {comparison.models_comparison.map((item) => {
            const isChampion = item.model_key === 'random_forest';
            const tierStyle = getTierColor(item.predicted_category);
            return (
              <div
                key={item.model_key}
                className={`p-5 rounded-2xl border transition-all ${
                  isChampion
                    ? 'bg-gradient-to-b from-indigo-950/40 to-slate-900/80 border-indigo-500/40 shadow-lg shadow-indigo-500/10'
                    : 'bg-slate-900/40 border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-semibold text-slate-300">{item.model_name}</span>
                  {isChampion && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      CHAMPION
                    </span>
                  )}
                </div>

                <div className={`p-3 rounded-xl border text-center font-bold text-base mb-3 ${tierStyle}`}>
                  {item.predicted_category}
                </div>

                <div className="space-y-1.5 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Confidence:</span>
                    <strong className="text-white">{(item.confidence_score * 100).toFixed(1)}%</strong>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div
                      className="bg-indigo-500 h-full rounded-full"
                      style={{ width: `${item.confidence_score * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Rigorous Metric Benchmarking Table */}
      <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
            <BarChart3 className="w-4 h-4 text-indigo-400" />
            <span>Academic Performance Benchmark Across All 4 Models</span>
          </div>
          <span className="text-xs text-slate-400">5-Fold Stratified CV & Test Set</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Model Architecture</th>
                <th className="py-3 px-4">Test Accuracy</th>
                <th className="py-3 px-4">5-Fold CV Accuracy</th>
                <th className="py-3 px-4">Macro F1-Score</th>
                <th className="py-3 px-4">Weighted F1-Score</th>
                <th className="py-3 px-4">Multi-Class ROC-AUC</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {Object.entries(metrics.all_tuned_models).map(([key, m]) => {
                const isChampion = key === metrics.champion_model;
                return (
                  <tr key={key} className={`hover:bg-slate-800/30 transition-colors ${isChampion ? 'bg-indigo-500/5' : ''}`}>
                    <td className="py-3 px-4 font-semibold text-white flex items-center space-x-2">
                      {isChampion && <Award className="w-4 h-4 text-indigo-400" />}
                      <span>{m.name}</span>
                    </td>
                    <td className="py-3 px-4 font-bold text-emerald-400">
                      {(m.test_accuracy * 100).toFixed(2)}%
                    </td>
                    <td className="py-3 px-4 text-slate-300">
                      {(m.best_cv_score * 100).toFixed(2)}%
                    </td>
                    <td className="py-3 px-4 text-slate-300">
                      {(m.f1_macro * 100).toFixed(2)}%
                    </td>
                    <td className="py-3 px-4 text-slate-300">
                      {(m.f1_weighted * 100).toFixed(2)}%
                    </td>
                    <td className="py-3 px-4 font-bold text-indigo-300 font-mono">
                      {m.roc_auc_macro ? m.roc_auc_macro.toFixed(4) : "N/A"}
                    </td>
                    <td className="py-3 px-4">
                      {isChampion ? (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold">
                          Champion
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 text-[10px]">
                          Tuned
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
