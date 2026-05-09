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
        const detail = err.response.data.detail.toLowerCase();
        if (detail.includes("api key")) {
          setError("Invalid Gemini API Key. Please verify your backend/.env file.");
        } else if (detail.includes("safety") || detail.includes("blocked")) {
          setError("Summary blocked by Gemini Safety Filters. The content may be too sensitive.");
        } else {
          setError("Failed to generate summary: " + err.response.data.detail);
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
    <div className="min-h-screen bg-[#fdfdff] text-gray-800 font-sans selection:bg-violet-200 selection:text-violet-900">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Layers className="h-8 w-8 text-[#7e34f6]" />
              <span className="ml-2 text-xl font-bold text-gray-900 tracking-tight">Summarizer<span className="text-[#7e34f6]">Pro</span></span>
            </div>
            <div className="flex items-center space-x-6">
              <a href="#" className="text-gray-500 hover:text-gray-900 text-sm font-medium transition-colors">AI Tools</a>
              <a href="#" className="text-gray-500 hover:text-gray-900 text-sm font-medium transition-colors">Features</a>
              <button className="bg-[#7e34f6] hover:bg-violet-700 text-white px-4 py-2 rounded-lg text-sm font-semibold shadow-sm transition-colors">
                Try For Free
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center px-4 py-1.5 mb-6 rounded-full bg-violet-100 text-[#7e34f6] font-semibold text-sm">
            <Sparkles size={16} className="mr-2" />
            AI-Powered Document Intelligence
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6 tracking-tight">
            Distill Knowledge with <span className="text-[#7e34f6]">Precision</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-gray-600">
            Upload any PDF and let our advanced AI generate tailored summaries based on your specific persona and objectives.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="max-w-5xl mx-auto mb-8 bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg shadow-sm">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Main Content Grid */}
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          <InputPanel onSubmit={handleSummarize} isLoading={isLoading} />
          
          <div className="h-full min-h-[500px]">
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