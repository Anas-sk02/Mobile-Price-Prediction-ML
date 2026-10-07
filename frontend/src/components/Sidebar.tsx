import React from 'react';
import {
  LayoutGrid,
  Smartphone,
  FlaskConical,
  Database,
  BarChart3,
  Info,
  Sparkles
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  apiOnline: boolean | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, apiOnline }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutGrid },
    { id: 'predict', label: 'Predict', icon: Smartphone },
    { id: 'model-lab', label: 'Model Lab', icon: FlaskConical },
    { id: 'dataset', label: 'Dataset', icon: Database },
    { id: 'insights', label: 'Insights', icon: BarChart3 },
    { id: 'about', label: 'About', icon: Info },
  ];

  return (
    <aside className="w-64 bg-[#FAF5ED] border-r border-[#E2D7C8] flex flex-col justify-between shrink-0 min-h-screen sticky top-0 h-screen z-30 shadow-[1px_0_12px_rgba(50,35,20,0.03)]">
      <div>
        {/* Logo & Brand Header */}
        <div className="p-5 border-b border-[#E2D7C8] flex items-center space-x-3 bg-white/70">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-900 via-amber-950 to-slate-900 flex items-center justify-center text-amber-200 shadow-sm font-bold text-lg border border-amber-600/30">
            <Sparkles className="w-5 h-5 text-amber-300" />
          </div>
          <div>
            <div className="font-luxury font-bold text-slate-900 text-lg leading-tight tracking-tight">SmartPrice</div>
            <div className="text-[10px] font-semibold tracking-widest text-amber-800/80 uppercase">Price Intelligence</div>
          </div>
        </div>

        {/* Platform Section */}
        <div className="p-4">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 mb-2">
            Platform
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all text-left cursor-pointer ${
                    isActive
                      ? 'bg-white text-amber-900 font-semibold shadow-xs border border-[#D8CABE]'
                      : 'text-slate-600 hover:text-slate-950 hover:bg-white/70'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-amber-800' : 'text-slate-400'}`} />
                  <span className={isActive ? 'font-semibold' : ''}>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Bottom System Status */}
      <div className="p-4 border-t border-[#E2D7C8] bg-white/80">
        <div className="flex items-center justify-between text-xs mb-1.5">
          <div className="flex items-center space-x-2">
            <span className={`w-2 h-2 rounded-full ${apiOnline ? 'bg-emerald-500 animate-pulse' : apiOnline === false ? 'bg-rose-500' : 'bg-amber-400'}`} />
            <span className="font-medium text-slate-700">ML system online</span>
          </div>
          <span className="text-emerald-700 font-semibold text-xs">{apiOnline ? '100%' : 'Offline'}</span>
        </div>
        <div className="text-[10px] font-mono text-slate-400 flex justify-between">
          <span>BUILD VERSION</span>
          <span className="text-amber-900/70 font-semibold">v1.2.4</span>
        </div>
      </div>
    </aside>
  );
};
