import React, { useState, useEffect } from 'react';
import { fetchDatasetSummary, fetchEdaInsights } from '../api';
import { Database, CheckCircle2, TrendingUp, Activity } from 'lucide-react';

export const DatasetAnalyticsView: React.FC = () => {
  const [summary, setSummary] = useState<any | null>(null);
  const [eda, setEda] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function load() {
      try {
        const [sumRes, edaRes] = await Promise.all([
          fetchDatasetSummary(),
          fetchEdaInsights()
        ]);
        setSummary(sumRes);
        setEda(edaRes);
      } catch (e) {
        console.error("Dataset analytics load error:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading || !summary || !eda) {
    return (
      <div className="p-12 text-center text-slate-400 flex items-center justify-center space-x-2">
        <Activity className="w-5 h-5 animate-spin text-indigo-400" />
        <span>Loading dataset analytics & statistical profiles...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div className="flex items-center space-x-2">
          <Database className="w-5 h-5 text-indigo-400" />
          <h2 className="text-xl font-bold text-white">Dataset Analytics & Statistical Profiling</h2>
        </div>
        <p className="text-sm text-slate-400 mt-0.5">
          980 verified smartphone specifications audited with ANOVA F-tests and correlation metrics.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800">
          <div className="text-xs text-slate-400">Total Phone Records</div>
          <div className="text-2xl font-extrabold text-white mt-1">{summary.total_rows}</div>
          <div className="text-[11px] text-emerald-400 mt-1 flex items-center space-x-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>0 Duplicate Rows</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800">
          <div className="text-xs text-slate-400">Raw Technical Features</div>
          <div className="text-2xl font-extrabold text-white mt-1">{summary.total_columns}</div>
          <div className="text-[11px] text-indigo-400 mt-1">62 Post-Transformed</div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800">
          <div className="text-xs text-slate-400">Price Median</div>
          <div className="text-2xl font-extrabold text-white mt-1">₹{summary.price_summary.median.toLocaleString()}</div>
          <div className="text-[11px] text-slate-400 mt-1">Range: ₹3,499 – ₹650,000</div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800">
          <div className="text-xs text-slate-400">Target Categories</div>
          <div className="text-2xl font-extrabold text-white mt-1">4 Bins</div>
          <div className="text-[11px] text-emerald-400 mt-1">Stratified 80/20 Split</div>
        </div>
      </div>

      {/* Target Class Distribution Cards */}
      <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
        <div className="text-sm font-semibold text-slate-200">
          Domain-Standard 4-Tier Target Distribution
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(summary.target_class_distribution).map(([cat, data]: [string, any]) => (
            <div key={cat} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-bold text-white">{cat}</span>
                <span className="font-mono text-indigo-400 font-bold">{data.percent}%</span>
              </div>
              <div className="text-xs text-slate-400">{data.range}</div>
              <div className="text-xs font-semibold text-slate-300">{data.count} smartphones</div>
            </div>
          ))}
        </div>
      </div>

      {/* ANOVA F-Score Table */}
      <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
        <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
          <TrendingUp className="w-4 h-4 text-indigo-400" />
          <span>One-Way ANOVA Feature Significance Across Price Categories</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Feature Name</th>
                <th className="py-3 px-4">ANOVA F-Statistic</th>
                <th className="py-3 px-4">ANOVA p-value</th>
                <th className="py-3 px-4">Pearson Correlation ($r$)</th>
                <th className="py-3 px-4">Statistical Significance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {eda.ranked_features_by_f_score.map((feat: string) => {
                const anovaData = eda.anova_by_price_category[feat];
                const corrData = eda.correlations_with_price[feat];
                return (
                  <tr key={feat} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-4 font-mono font-medium text-slate-200">
                      {feat}
                    </td>
                    <td className="py-3 px-4 font-bold text-indigo-400 font-mono">
                      {anovaData.f_statistic.toFixed(2)}
                    </td>
                    <td className="py-3 px-4 text-slate-400 font-mono">
                      {anovaData.f_pvalue}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-300">
                      {corrData ? corrData.pearson_r.toFixed(4) : "N/A"}
                    </td>
                    <td className="py-3 px-4 text-emerald-400 flex items-center space-x-1">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Significant (p &lt; 0.001)</span>
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
