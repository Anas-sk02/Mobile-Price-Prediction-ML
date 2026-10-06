import React from 'react';
import { BookOpen, CheckCircle2, Cpu, Code2, Server, Award } from 'lucide-react';

export const AboutView: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-6 h-6 text-indigo-400" />
          <h2 className="text-xl font-bold text-white">System Architecture & Methodology</h2>
        </div>
        <p className="text-sm text-slate-400">
          SmartPrice is an end-to-end Machine Learning benchmarking and inference system developed for University ML Lab coursework.
        </p>
      </div>

      {/* 3 Pillar Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* ML Pipeline */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 space-y-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">1. ML Core & Preprocessing</h3>
            <p className="text-xs text-slate-400 mt-1">
              Zero-leakage Scikit-learn ColumnTransformer with median imputation, standard scaling, and one-hot encoding across 62 post-transformed features.
            </p>
          </div>
          <ul className="space-y-2 text-xs text-slate-300">
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>4 Core Models (LR, KNN, RF, SVM)</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>5-Fold Stratified GridSearchCV</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Permutation Feature Importance</span>
            </li>
          </ul>
        </div>

        {/* FastAPI Backend */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 space-y-4">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">2. FastAPI Backend Engine</h3>
            <p className="text-xs text-slate-400 mt-1">
              High-performance asynchronous REST API serving real-time single, batch, and 4-model consensus predictions with sub-10ms latency.
            </p>
          </div>
          <ul className="space-y-2 text-xs text-slate-300">
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>10 Verified Endpoints</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Pydantic Data Validation</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Full TestClient Integration Suite</span>
            </li>
          </ul>
        </div>

        {/* React Frontend */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 space-y-4">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">3. Modern UI Dashboard</h3>
            <p className="text-xs text-slate-400 mt-1">
              Custom React + TypeScript + Tailwind design system featuring real-time hardware calculation HUDs, preset loaders, and interactive charts.
            </p>
          </div>
          <ul className="space-y-2 text-xs text-slate-300">
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Live Spec Sliders & Presets</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Softmax Probability Meters</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Dark Enterprise Theme</span>
            </li>
          </ul>
        </div>

      </div>

      {/* Target Price Boundary Breakdown */}
      <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-4">
        <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200">
          <Award className="w-4 h-4 text-indigo-400" />
          <span>Domain-Standard Classification Boundaries</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1">
            <span className="font-bold text-blue-400">Tier 0: Budget</span>
            <div className="text-slate-300 font-semibold">Price $\le$ ₹15,000</div>
            <p className="text-slate-400 text-[11px]">Utility phones, Helio/Unisoc processors, 3-4GB RAM, 720p displays.</p>
          </div>

          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-1">
            <span className="font-bold text-emerald-400">Tier 1: Mid-Range</span>
            <div className="text-slate-300 font-semibold">₹15,001 – ₹30,000</div>
            <p className="text-slate-400 text-[11px]">Mass-market 5G devices, Snapdragon 6/7 series, 6-8GB RAM, 120Hz AMOLED.</p>
          </div>

          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-1">
            <span className="font-bold text-amber-400">Tier 2: Premium</span>
            <div className="text-slate-300 font-semibold">₹30,001 – ₹50,000</div>
            <p className="text-slate-400 text-[11px]">Flagship killers, Snapdragon 8 Gen 1/Dimensity 8000/9000, 67W-100W charging.</p>
          </div>

          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 space-y-1">
            <span className="font-bold text-red-400">Tier 3: Flagship</span>
            <div className="text-slate-300 font-semibold">Price &gt; ₹50,000</div>
            <p className="text-slate-400 text-[11px]">Ultra flagships, Apple Bionic, 200MP sensors, QHD+ displays, 12GB+ RAM.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
