import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { generatePDF } from '../api';

const Copy = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>;
const CheckCircle = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>;
const Download = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>;
const FileText = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>;
const Loader = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><line x1="12" x2="12" y1="2" y2="6"/><line x1="12" x2="12" y1="18" y2="22"/><line x1="4.93" x2="7.76" y1="4.93" y2="7.76"/><line x1="16.24" x2="19.07" y1="16.24" y2="19.07"/><line x1="2" x2="6" y1="12" y2="12"/><line x1="18" x2="22" y1="12" y2="12"/><line x1="4.93" x2="7.76" y1="19.07" y2="16.24"/><line x1="16.24" x2="19.07" y1="7.76" y2="4.93"/></svg>;

const ResultDisplay = ({ summary }) => {
  const [copied, setCopied] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  const handleCopy = () => {
    if (!summary) return;
    navigator.clipboard.writeText(summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = async () => {
    if (!summary) return;
    setIsDownloading(true);
    try {
      await generatePDF(summary);
    } catch (error) {
      alert("Failed to download PDF. Please try again.");
    } finally {
      setIsDownloading(false);
    }
  };

  if (!summary) {
    return (
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 h-full flex flex-col items-center justify-center text-center">
        <div className="bg-gray-50 p-6 rounded-full mb-4">
          <FileText className="text-gray-300" size={48} />
        </div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">No Summary Yet</h3>
        <p className="text-gray-500 max-w-sm">
          Upload a document and click "Generate Summary" to see the AI-generated results here.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 h-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-800 flex items-center">
          <div className="w-2 h-6 bg-[#7e34f6] rounded-full mr-3"></div>
          Summarized Output
        </h2>
        
        <div className="flex space-x-2">
          <button
            onClick={handleCopy}
            className="flex items-center px-3 py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200"
          >
            {copied ? <CheckCircle size={16} className="mr-1.5 text-green-500" /> : <Copy size={16} className="mr-1.5" />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button
            onClick={handleDownload}
            disabled={isDownloading}
            className={`flex items-center px-3 py-1.5 rounded-lg text-sm font-medium transition-colors border ${isDownloading ? 'bg-violet-100 text-violet-400 border-violet-200 cursor-not-allowed' : 'bg-violet-50 hover:bg-violet-100 text-[#7e34f6] border-violet-200'}`}
          >
            {isDownloading ? <Loader size={16} className="mr-1.5 animate-spin" /> : <Download size={16} className="mr-1.5" />}
            Download PDF
          </button>
        </div>
      </div>

      <div className="flex-1 bg-gray-50 rounded-xl p-6 overflow-y-auto border border-gray-100 max-h-[600px]">
        <div className="prose prose-sm md:prose-base prose-violet max-w-none text-gray-700 leading-relaxed">
          <ReactMarkdown>{summary}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
