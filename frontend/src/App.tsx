import { useState, useEffect } from 'react';
import type { SmartphoneSpecs } from './types';
import { PRESET_SMARTPHONES, checkApiHealth } from './api';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardView } from './components/DashboardView';
import { PredictorView } from './components/PredictorView';
import { ModelBenchmarkingView } from './components/ModelBenchmarkingView';
import { DatasetAnalyticsView } from './components/DatasetAnalyticsView';
import { ExplainabilityView } from './components/ExplainabilityView';
import { AboutView } from './components/AboutView';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [activeSpecs, setActiveSpecs] = useState<SmartphoneSpecs>(PRESET_SMARTPHONES.flagship.specs);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await checkApiHealth();
        setApiOnline(res.status === 'healthy');
      } catch (e) {
        setApiOnline(false);
      }
    }
    checkHealth();
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  const handleCompareWithSpecs = (specs: SmartphoneSpecs) => {
    setActiveSpecs(specs);
    setActiveTab('model-lab');
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex font-sans antialiased selection:bg-blue-600 selection:text-white">
      {/* Fixed Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiOnline={apiOnline}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header */}
        <Header
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />

        {/* Dynamic Workspace Views */}
        <main className="flex-1 px-6 py-7 max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && (
            <DashboardView onNavigate={(tab) => setActiveTab(tab)} />
          )}

          {activeTab === 'predict' && (
            <PredictorView onCompareWithSpecs={handleCompareWithSpecs} />
          )}

          {activeTab === 'model-lab' && (
            <ModelBenchmarkingView currentSpecs={activeSpecs} />
          )}

          {activeTab === 'dataset' && (
            <DatasetAnalyticsView />
          )}

          {activeTab === 'insights' && (
            <ExplainabilityView />
          )}

          {activeTab === 'about' && (
            <AboutView />
          )}
        </main>

        {/* Clean Enterprise Footer */}
        <footer className="border-t border-slate-200 bg-white py-4 px-6 mt-auto">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-800">SmartPrice Intelligence Platform</span>
              <span>•</span>
              <span>Milestone 2.4 Production Release</span>
            </div>
            <div className="text-slate-400 font-mono text-[11px]">
              FastAPI Server (Port 8000) • Scikit-Learn 1.8.0 • React 19 + TypeScript
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
