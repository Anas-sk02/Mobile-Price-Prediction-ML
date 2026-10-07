import React from 'react';
import { Search, CheckCircle2, Activity } from 'lucide-react';

interface HeaderProps {
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ searchQuery = '', setSearchQuery }) => {
  return (
    <header className="h-16 bg-[#FAF5ED]/90 backdrop-blur-md border-b border-[#E2D7C8] px-6 flex items-center justify-between sticky top-0 z-20 shadow-[0_1px_6px_rgba(50,35,20,0.02)]">
      {/* Search & Quick Metric */}
      <div className="flex items-center space-x-4 flex-1 max-w-2xl">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-amber-900/40 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search hardware spec, SKU, cluster..."
            value={searchQuery}
            onChange={(e) => setSearchQuery && setSearchQuery(e.target.value)}
            className="w-full pl-9.5 pr-4 py-2 bg-white hover:bg-white focus:bg-white text-xs text-slate-800 placeholder-slate-400 rounded-lg border border-[#DDD1C1] focus:outline-hidden focus:ring-2 focus:ring-amber-700/15 focus:border-amber-800/50 transition-all shadow-2xs"
          />
        </div>
        <div className="hidden sm:flex items-center space-x-1.5 px-3 py-1.5 bg-white border border-[#DDD1C1] rounded-lg text-xs text-amber-900 font-medium shrink-0 shadow-2xs">
          <CheckCircle2 className="w-3.5 h-3.5 text-amber-700" />
          <span><strong className="font-semibold text-slate-900">980</strong> phones evaluated</span>
        </div>
      </div>

      {/* Lab Project Details Badge (No Profile Avatar) */}
      <div className="flex items-center space-x-3 ml-4">
        <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 bg-white border border-[#DDD1C1] rounded-lg text-xs shadow-2xs">
          <Activity className="w-3.5 h-3.5 text-emerald-600" />
          <span className="font-semibold text-slate-800">ML Pricing Research Lab</span>
          <span className="text-slate-300">•</span>
          <span className="text-slate-500 text-[11px]">Academic Milestone</span>
        </div>
      </div>
    </header>
  );
};
