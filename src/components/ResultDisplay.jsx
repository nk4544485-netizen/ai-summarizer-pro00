import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Download, Sparkles, AlertCircle } from 'lucide-react';
import { exportToPDF } from '../api';

const ResultDisplay = ({ summary, error }) => {
  const handleCopy = () => {
    if (summary) navigator.clipboard.writeText(summary);
  };

  if (error) {
    return (
      <div className="glass-card rounded-[2.5rem] p-8 h-full flex flex-col items-center justify-center text-center animate-in fade-in duration-500">
        <div className="w-20 h-20 bg-red-50 text-red-500 rounded-3xl flex items-center justify-center mb-6">
          <AlertCircle size={40} />
        </div>
        <h3 className="text-xl font-bold text-slate-800 mb-2">Something went wrong</h3>
        <p className="text-slate-500 text-sm max-w-xs">{error}</p>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="glass-card rounded-[2.5rem] p-8 h-full flex flex-col items-center justify-center text-center opacity-60">
        <div className="w-20 h-20 bg-slate-50 text-slate-300 rounded-3xl flex items-center justify-center mb-6 animate-pulse-slow">
          <Sparkles size={40} />
        </div>
        <h3 className="text-xl font-bold text-slate-400">Intelligence Awaiting</h3>
        <p className="text-slate-300 text-sm max-w-xs mt-2">
          Your tailored summary will appear here once the analysis is complete.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-[2.5rem] p-8 h-full flex flex-col animate-in slide-in-from-right-8 duration-500">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-2xl font-bold text-slate-800 flex items-center tracking-tight">
          <div className="w-2 h-8 bg-violet-600 rounded-full mr-4"></div>
          Distilled Results
        </h2>
        <div className="flex space-x-3">
          <button
            onClick={handleCopy}
            className="p-3 bg-slate-50 text-slate-600 rounded-2xl hover:bg-slate-100 transition-colors"
            title="Copy to Clipboard"
          >
            <Copy size={18} />
          </button>
          <button
            onClick={() => exportToPDF(summary)}
            className="p-3 bg-violet-50 text-violet-600 rounded-2xl hover:bg-violet-100 transition-colors"
            title="Download PDF"
          >
            <Download size={18} />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar pr-4 -mr-4">
        <div className="prose prose-slate prose-sm md:prose-base max-w-none prose-headings:font-bold prose-p:leading-relaxed prose-violet">
          <ReactMarkdown>{summary}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
