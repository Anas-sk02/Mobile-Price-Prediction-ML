import { useState, useEffect } from 'react';
import type { SmartphoneSpecs } from './types';
import { PRESET_SMARTPHONES, checkApiHealth } from './api';
import { Navbar } from './components/Navbar';
import { PredictorView } from './components/PredictorView';
import { ModelBenchmarkingView } from './components/ModelBenchmarkingView';
import { ExplainabilityView } from './components/ExplainabilityView';
import { DatasetAnalyticsView } from './components/DatasetAnalyticsView';
import { AboutView } from './components/AboutView';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('predict');
  const [activeSpecs, setActiveSpecs] = useState<SmartphoneSpecs>(PRESET_SMARTPHONES.flagship.specs);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

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
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleCompareWithSpecs = (specs: SmartphoneSpecs) => {
    setActiveSpecs(specs);
    setActiveTab('benchmark');
  };

  return (
    <div className="min-h-screen bg-[#0B0F17] text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiOnline={apiOnline}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'predict' && (
          <PredictorView onCompareWithSpecs={handleCompareWithSpecs} />
        )}

        {activeTab === 'benchmark' && (
          <ModelBenchmarkingView currentSpecs={activeSpecs} />
        )}

        {activeTab === 'explainability' && (
          <ExplainabilityView />
        )}

        {activeTab === 'analytics' && (
          <DatasetAnalyticsView />
        )}

        {activeTab === 'about' && (
          <AboutView />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950/80 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-slate-300">SmartPrice ML System</span>
            <span>•</span>
            <span>University Machine Learning Lab Project</span>
          </div>
          <div>
            Built with FastAPI, Scikit-Learn, Vite, React & TypeScript
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
