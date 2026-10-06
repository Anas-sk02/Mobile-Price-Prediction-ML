import React, { useState } from 'react';
import { BookOpen, CheckCircle2, Cpu, Code2, Server, Award, ChevronDown, ChevronUp, HelpCircle } from 'lucide-react';

export const AboutView: React.FC = () => {
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  const faqs = [
    {
      q: "Why formulate smartphone pricing as a 4-class classification problem rather than continuous regression?",
      a: "Commercial consumer markets evaluate smartphones by distinct economic segments (Budget, Mid-Range, Premium, Flagship). Continuous regression is skewed by high-end luxury foldables and niche variants (e.g. ₹650k), whereas multi-class classification establishes robust decision boundaries and actionable category probabilities."
    },
    {
      q: "How was zero data leakage guaranteed across the ML pipeline?",
      a: "The dataset was split using an 80/20 Stratified Train-Test partition before computing any transformation statistics. All imputation medians, standard scaling means/variances, and one-hot categorical dictionaries were fitted strictly on the training partition (784 samples) and transformed on the test partition (196 samples). The continuous price column was completely excluded from feature matrices."
    },
    {
      q: "Why did Random Forest outperform Support Vector Machines and Logistic Regression?",
      a: "Random Forest constructs an ensemble of decorrelated decision trees that naturally capture non-linear feature interactions (such as the combination of 120Hz display, 12GB RAM, and Snapdragon 8 series) without requiring manual polynomial basis expansions or assumptions of linear class separation."
    },
    {
      q: "What explains the negative linear correlation between battery capacity and price?",
      a: "Ultra-flagship phones prioritize slim, lightweight ergonomics, wireless charging coils, and high-wattage fast charging (65W-120W) over bulky 6,000+ mAh battery packs, which are predominantly engineered into budget utility devices."
    },
    {
      q: "What is the distinction between Gini Importance (MDI) and Permutation Feature Importance?",
      a: "Gini Impurity (MDI) is calculated during tree training and can exhibit cardinality bias toward continuous numerical features. Permutation Importance evaluates the actual empirical loss in Macro F1 score on the unseen test dataset when a feature column is randomly shuffled, providing an unbiased model-agnostic measurement of feature predictive power."
    }
  ];

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-2">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-5 h-5 text-indigo-600" />
          <h1 className="text-lg font-bold text-slate-900">System Architecture & Viva Voce Guide</h1>
        </div>
        <p className="text-xs text-slate-500">
          Comprehensive project methodology, mathematical formulations, and frequently asked Viva Voce examination questions.
        </p>
      </div>

      {/* 3 Architecture Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* ML Core */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">1. ML Core & Preprocessing</h3>
            <p className="text-xs text-slate-500 mt-1">
              Zero-leakage Scikit-learn ColumnTransformer with median imputation, standard scaling, and one-hot encoding across 62 dimensions.
            </p>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>4 Models (Random Forest, SVM, KNN, LR)</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>5-Fold Stratified GridSearchCV</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Permutation Importance Analysis</span>
            </li>
          </ul>
        </div>

        {/* FastAPI Backend */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">2. FastAPI Backend Engine</h3>
            <p className="text-xs text-slate-500 mt-1">
              High-performance asynchronous REST API serving real-time single, batch, and 4-model consensus predictions with sub-10ms latency.
            </p>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>10 Verified REST Endpoints</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Strict Pydantic Validation</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>100% Integration Test Coverage</span>
            </li>
          </ul>
        </div>

        {/* React UI */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">3. Modern Web Dashboard</h3>
            <p className="text-xs text-slate-500 mt-1">
              Clean React 19 + TypeScript + Tailwind design system featuring real-time hardware calculation HUDs and interactive lab views.
            </p>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Live Spec Sliders & Presets</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Softmax Probability Meters</span>
            </li>
            <li className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Enterprise Light Theme</span>
            </li>
          </ul>
        </div>

      </div>

      {/* Target Price Boundary Breakdown */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
          <Award className="w-4 h-4 text-indigo-600" />
          <span>Domain Classification Boundaries</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 space-y-1">
            <span className="font-bold text-blue-800">Tier 0: Budget</span>
            <div className="text-slate-900 font-bold">Price $\le$ ₹15,000</div>
            <p className="text-slate-600 text-[11px]">Utility phones, Helio/Unisoc processors, 3-4GB RAM, 720p HD+ displays.</p>
          </div>

          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 space-y-1">
            <span className="font-bold text-emerald-800">Tier 1: Mid-Range</span>
            <div className="text-slate-900 font-bold">₹15,001 – ₹30,000</div>
            <p className="text-slate-600 text-[11px]">Mass-market 5G devices, Snapdragon 6/7 series, 6-8GB RAM, 120Hz FHD+.</p>
          </div>

          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 space-y-1">
            <span className="font-bold text-amber-800">Tier 2: Premium</span>
            <div className="text-slate-900 font-bold">₹30,001 – ₹50,000</div>
            <p className="text-slate-600 text-[11px]">Flagship killers, Dimensity 8000/9000, 67W-100W fast charging.</p>
          </div>

          <div className="p-4 rounded-xl bg-red-50 border border-red-200 space-y-1">
            <span className="font-bold text-red-800">Tier 3: Flagship</span>
            <div className="text-slate-900 font-bold">Price &gt; ₹50,000</div>
            <p className="text-slate-600 text-[11px]">Ultra flagships, Apple Bionic, 200MP sensors, QHD+ displays, 12GB+ RAM.</p>
          </div>
        </div>
      </div>

      {/* Frequently Asked Viva Voce Questions */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
          <HelpCircle className="w-4 h-4 text-indigo-600" />
          <span>Frequently Asked Viva Voce Questions & Answers</span>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, index) => {
            const isOpen = openFaq === index;
            return (
              <div 
                key={index} 
                className="border border-slate-200 rounded-xl overflow-hidden transition-all"
              >
                <button
                  onClick={() => setOpenFaq(isOpen ? null : index)}
                  className="w-full text-left p-4 bg-slate-50 hover:bg-slate-100/80 flex items-center justify-between font-bold text-xs text-slate-800 cursor-pointer"
                >
                  <span className="flex items-center space-x-2">
                    <span className="text-indigo-600 font-mono">Q{index + 1}:</span>
                    <span>{faq.q}</span>
                  </span>
                  {isOpen ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
                </button>
                {isOpen && (
                  <div className="p-4 bg-white text-xs text-slate-600 leading-relaxed border-t border-slate-100">
                    <strong className="text-indigo-900 font-semibold">Answer: </strong>
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
};
