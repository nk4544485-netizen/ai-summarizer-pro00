import React, { useState } from 'react';
import { Upload, FileText, User, Target, Loader2, Download, CheckCircle, Brain, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { jsPDF } from 'jspdf';

function App() {
  const [file, setFile] = useState(null);
  const [persona, setPersona] = useState('General');
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a PDF file first.');
      return;
    }

    setLoading(true);
    setError('');
    setSummary('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('persona', persona);
    formData.append('goal', goal);

    try {
      const response = await fetch('http://localhost:8000/summarize', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to summarize');
      }

      const data = await response.json();
      setSummary(data.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 20;
    const maxWidth = pageWidth - margin * 2;
    
    doc.setFontSize(18);
    doc.text('MindMap AI Summary', margin, 20);
    doc.setFontSize(12);
    doc.text(`Persona: ${persona}`, margin, 30);
    doc.text(`Goal: ${goal || 'General Summary'}`, margin, 38);
    
    doc.setFontSize(10);
    const splitText = doc.splitTextToSize(summary.replace(/[#*]/g, ''), maxWidth);
    doc.text(splitText, margin, 50);
    
    doc.save('MindMap_AI_Summary.pdf');
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200">
      {/* Header */}
      <header className="border-b border-white/5 py-4 px-6 md:px-12 flex justify-between items-center glass sticky top-0 z-50">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="bg-brand p-2 rounded-lg group-hover:rotate-12 transition-transform">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl md:text-2xl font-bold tracking-tight">
            MindMap <span className="gradient-text">AI Pro</span>
          </h1>
        </div>
        <div className="hidden md:flex gap-6 text-sm font-medium text-slate-400">
          <a href="#" className="hover:text-white transition-colors">Tools</a>
          <a href="#" className="hover:text-white transition-colors">History</a>
          <a href="#" className="hover:text-white transition-colors">Pricing</a>
        </div>
        <button className="bg-white/5 hover:bg-white/10 text-white px-4 py-2 rounded-lg text-sm border border-white/10 transition-all">
          Connect Account
        </button>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12 grid lg:grid-cols-5 gap-12">
        {/* Left Panel: Inputs */}
        <div className="lg:col-span-2 space-y-8">
          <section className="space-y-4">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-400" />
              Configure AI
            </h2>
            
            <div className="space-y-6 bg-slate-900/50 p-6 rounded-2xl border border-white/5 glass">
              <div className="space-y-2">
                <label className="text-sm text-slate-400 flex items-center gap-2">
                  <User className="w-4 h-4" /> Select Persona
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {['Student', 'Professional', 'Researcher', 'General'].map((p) => (
                    <button
                      key={p}
                      onClick={() => setPersona(p)}
                      className={`px-4 py-3 rounded-xl text-sm font-medium transition-all border ${
                        persona === p 
                        ? 'bg-brand/20 border-brand text-brand-400 shadow-lg shadow-brand/10' 
                        : 'bg-white/5 border-white/5 text-slate-400 hover:bg-white/10'
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm text-slate-400 flex items-center gap-2">
                  <Target className="w-4 h-4" /> Summarization Goal
                </label>
                <input
                  type="text"
                  placeholder="e.g. Extract key methodology and data..."
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand/50 transition-all"
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm text-slate-400 flex items-center gap-2">
                  <FileText className="w-4 h-4" /> Upload Document
                </label>
                <div className="relative group">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                  />
                  <div className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all ${
                    file ? 'border-brand/50 bg-brand/5' : 'border-white/10 group-hover:border-white/20'
                  }`}>
                    <div className="bg-white/5 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Upload className={`w-6 h-6 ${file ? 'text-brand' : 'text-slate-400'}`} />
                    </div>
                    {file ? (
                      <div>
                        <p className="text-sm font-medium text-slate-200 truncate max-w-[200px] mx-auto">{file.name}</p>
                        <p className="text-xs text-slate-500 mt-1">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                      </div>
                    ) : (
                      <p className="text-sm text-slate-400">Click or drag PDF to upload</p>
                    )}
                  </div>
                </div>
              </div>

              <button
                onClick={handleSubmit}
                disabled={loading || !file}
                className="w-full btn-primary flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing Document...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate Summary
                  </>
                )}
              </button>

              {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm p-4 rounded-xl">
                  {error}
                </div>
              )}
            </div>
          </section>
        </div>

        {/* Right Panel: Result */}
        <div className="lg:col-span-3">
          <section className="h-full min-h-[500px] flex flex-col space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-emerald-400" />
                AI Analysis
              </h2>
              {summary && (
                <button
                  onClick={downloadPDF}
                  className="flex items-center gap-2 text-sm text-brand-400 hover:text-brand-300 transition-colors bg-brand/10 px-4 py-2 rounded-lg"
                >
                  <Download className="w-4 h-4" /> Export PDF
                </button>
              )}
            </div>

            <div className="flex-grow bg-slate-900/50 rounded-2xl border border-white/5 glass p-8 overflow-y-auto max-h-[700px] relative">
              {summary ? (
                <div className="prose prose-invert prose-purple max-w-none prose-p:text-slate-400 prose-headings:text-white prose-strong:text-brand-400">
                  <ReactMarkdown>{summary}</ReactMarkdown>
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-center space-y-4 text-slate-500">
                  <div className="bg-white/5 p-6 rounded-full">
                    <FileText className="w-12 h-12" />
                  </div>
                  <div className="max-w-xs">
                    <p className="text-lg font-medium text-slate-300">No summary yet</p>
                    <p className="text-sm mt-2">Upload a PDF and click generate to see the AI magic happen here.</p>
                  </div>
                </div>
              )}
            </div>
          </section>
        </div>
      </main>

      <footer className="mt-12 py-8 border-t border-white/5 text-center text-slate-500 text-xs">
        <p>© 2026 MindMap AI Pro. Powered by Google Gemini 1.5 Flash.</p>
      </footer>
    </div>
  );
}

export default App;
