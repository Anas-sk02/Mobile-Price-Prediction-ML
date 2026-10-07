import React from 'react';
import { Search, CheckCircle2, Activity, Menu } from 'lucide-react';

interface HeaderProps {
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
  onOpenMobileMenu?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  searchQuery = '',
  setSearchQuery,
  onOpenMobileMenu
}) => {
  return (
    <header className="h-16 bg-[#FAF5ED]/90 backdrop-blur-md border-b border-[#E2D7C8] px-4 sm:px-6 flex items-center justify-between sticky top-0 z-20 shadow-[0_1px_6px_rgba(50,35,20,0.02)]">
      {/* Mobile Menu Button & Search */}
      <div className="flex items-center space-x-2 sm:space-x-4 flex-1 max-w-2xl">
        {/* Mobile Hamburger Button */}
        <button
          onClick={onOpenMobileMenu}
          className="lg:hidden p-2 rounded-lg bg-white border border-[#DDD1C1] text-amber-900 hover:bg-[#FAF5ED] active:scale-95 transition-all cursor-pointer shrink-0 shadow-2xs"
          aria-label="Open Mobile Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="relative flex-1">
          <Search className="w-4 h-4 text-amber-900/40 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search spec, SKU..."
            value={searchQuery}
            onChange={(e) => setSearchQuery && setSearchQuery(e.target.value)}
            className="w-full pl-9.5 pr-4 py-2 bg-white hover:bg-white focus:bg-white text-xs text-slate-800 placeholder-slate-400 rounded-lg border border-[#DDD1C1] focus:outline-hidden focus:ring-2 focus:ring-amber-700/15 focus:border-amber-800/50 transition-all shadow-2xs"
          />
        </div>

        <div className="hidden sm:flex items-center space-x-1.5 px-3 py-1.5 bg-white border border-[#DDD1C1] rounded-lg text-xs text-amber-900 font-medium shrink-0 shadow-2xs">
          <CheckCircle2 className="w-3.5 h-3.5 text-amber-700" />
          <span><strong className="font-semibold text-slate-900">980</strong> phones</span>
        </div>
      </div>

      {/* Lab Project Details Badge */}
      <div className="flex items-center space-x-2 sm:space-x-3 ml-2 sm:ml-4">
        <div className="flex items-center space-x-2 px-2.5 sm:px-3 py-1.5 bg-white border border-[#DDD1C1] rounded-lg text-xs shadow-2xs">
          <Activity className="w-3.5 h-3.5 text-emerald-600" />
          <span className="font-semibold text-slate-800 text-[11px] sm:text-xs">SmartPrice Lab</span>
          <span className="hidden md:inline text-slate-300">•</span>
          <span className="hidden md:inline text-slate-500 text-[11px]">Academic</span>
        </div>
      </div>
    </header>
  );
};
