import React from 'react';
import { Cpu, Layers, Database, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  apiOnline: boolean | null;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, apiOnline }) => {
  const navItems = [
    { id: 'predict', label: 'Predictor & Presets', icon: Sparkles },
    { id: 'benchmark', label: 'Model Benchmarking', icon: Layers },
    { id: 'explainability', label: 'Feature Explainability', icon: Cpu },
    { id: 'analytics', label: 'Dataset Insights', icon: Database },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('predict')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-emerald-500 p-0.5 shadow-lg shadow-indigo-500/20 flex items-center justify-center">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Cpu className="w-5 h-5 text-indigo-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-lg font-bold text-white tracking-tight">SmartPrice</span>
                <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  ML Engine
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">Smartphone Price Category Prediction</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-900/60 p-1 rounded-xl border border-slate-800">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* System Status & Champion Badge */}
          <div className="flex items-center space-x-3">
            <div className="hidden lg:flex items-center space-x-2 px-3 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>RF Champion: 82.7% Acc</span>
            </div>

            <div className="flex items-center space-x-1.5 text-xs text-slate-400 border border-slate-800 px-2.5 py-1 rounded-lg bg-slate-900/40">
              {apiOnline ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400 font-mono text-[11px]">API Live</span>
                </>
              ) : (
                <>
                  <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
                  <span className="text-amber-400 font-mono text-[11px]">Connecting...</span>
                </>
              )}
            </div>
          </div>

        </div>

        {/* Mobile Navigation */}
        <div className="flex md:hidden overflow-x-auto py-2 space-x-1 border-t border-slate-800/50">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
                  isActive ? 'bg-indigo-600 text-white' : 'text-slate-400 bg-slate-900/40'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
