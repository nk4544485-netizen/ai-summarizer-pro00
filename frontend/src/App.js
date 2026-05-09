import React, { useState } from 'react';
import InputPanel from './components/InputPanel';
import ResultDisplay from './components/ResultDisplay';
import { summarizePDF } from './api';

const Sparkles = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>;
const Layers = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 12 12 17 22 12"/><polyline points="2 17 12 22 22 17"/></svg>;
const CheckCircle = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>;

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [showToast, setShowToast] = useState(false);

  const handleSummarize = async (formData) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await summarizePDF(formData);
      // Assuming the backend returns { summary: "..." }
      if (result && result.summary) {
        setSummary(result.summary);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 4000);
      } else {
        // Fallback if the response format is different
        setSummary(JSON.stringify(result, null, 2));
      }
    } catch (err) {
      if (!err.response) {
        setError("Backend server is offline. Please make sure the FastAPI server is running on port 8000.");
      } else if (err.response.data && err.response.data.detail) {
        const detailRaw = err.response.data.detail;
        const detailString = typeof detailRaw === 'string' ? detailRaw : JSON.stringify(detailRaw);
        const detail = detailString.toLowerCase();
        if (detail.includes("api key")) {
          setError("Invalid Gemini API Key. Please verify your backend/.env file.");
        } else if (detail.includes("safety") || detail.includes("blocked")) {
          setError("Summary blocked by Gemini Safety Filters. The content may be too sensitive.");
        } else {
          setError("Failed to generate summary: " + detailString);
        }
      } else {
        setError("Failed to generate summary: " + err.message);
      }
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen font-sans selection:bg-violet-200 selection:text-violet-900">
      {/* Navbar */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center group cursor-pointer">
              <div className="premium-gradient p-1.5 rounded-xl group-hover:rotate-6 transition-transform">
                <Layers className="h-6 w-6 text-white" />
              </div>
              <span className="ml-3 text-xl font-bold text-gray-900 tracking-tight">Summarizer<span className="text-[#7e34f6]">Pro</span></span>
            </div>
            <div className="flex items-center space-x-8">
              <a href="#" className="text-gray-500 hover:text-[#7e34f6] text-sm font-semibold transition-colors">AI Tools</a>
              <a href="#" className="text-gray-500 hover:text-[#7e34f6] text-sm font-semibold transition-colors">Features</a>
              <button className="premium-gradient text-white px-5 py-2.5 rounded-xl text-sm font-bold shadow-lg shadow-violet-200 hover:scale-105 active:scale-95 transition-all">
                Try For Free
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16 animate-float">
          <div className="inline-flex items-center justify-center px-4 py-1.5 mb-6 rounded-full bg-violet-100 text-[#7e34f6] font-bold text-xs uppercase tracking-wider">
            <Sparkles size={14} className="mr-2" />
            AI-Powered Document Intelligence
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6 tracking-tight">
            Distill Knowledge with <span className="text-[#7e34f6] bg-clip-text text-transparent premium-gradient">Precision</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-gray-600 leading-relaxed">
            Upload any PDF and let our advanced AI generate tailored summaries based on your specific persona and objectives.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="max-w-5xl mx-auto mb-8 bg-red-50 border-l-4 border-red-500 p-5 rounded-r-2xl shadow-xl animate-in fade-in slide-in-from-top-4">
            <div className="flex items-center">
              <div className="bg-red-100 p-2 rounded-full">
                <X className="h-5 w-5 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-bold text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Main Content Grid */}
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
          <div className="glass-card rounded-3xl p-1 hover-lift">
            <InputPanel onSubmit={handleSummarize} isLoading={isLoading} />
          </div>
          
          <div className="glass-card rounded-3xl p-1 h-full min-h-[500px] hover-lift">
            <ResultDisplay summary={summary} />
          </div>
        </div>

        {/* Success Toast */}
        {showToast && (
          <div className="fixed bottom-6 right-6 bg-green-600 text-white px-6 py-4 rounded-xl shadow-2xl flex items-center space-x-3 z-50 transition-all transform scale-100 opacity-100 duration-300">
            <CheckCircle size={24} className="text-green-200" />
            <span className="font-semibold tracking-wide">Summary successfully generated!</span>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;