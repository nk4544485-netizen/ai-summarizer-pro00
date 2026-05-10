import React, { useState, useRef } from 'react';
import { jsPDF } from 'jspdf';
import { extractTextFromPDF, generateSummary, exportToPDF, listAvailableModels } from './apiService';
import { 
  Upload, Sparkles, Download, CheckCircle2, Globe, FileText, 
  MessageSquare, Maximize, FileOutput, PenTool, Edit3, Briefcase, GraduationCap, Users, ShieldAlert
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [summary, setSummary] = useState('');
  const fileInputRef = useRef(null);

  const handleScan = async () => {
    try {
      const models = await listAvailableModels();
      alert(`Available Models for your key:\n\n${models.join('\n')}`);
    } catch (e) {
      alert(`Scan Failed: ${e.message}`);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') setIsDragging(true);
    else if (e.type === 'dragleave') setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const processFile = async () => {
    if (!file) return;
    setIsProcessing(true);
    try {
      const result = await generateSummary(file, "student", "");
      setSummary(result);
    } catch (error) {
      console.error("Processing Error:", error);
      alert(`Error: ${error.message || 'Unknown processing error'}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (summary) exportToPDF(summary);
  };

  return (
    <div className="min-h-screen bg-[#fafafc] text-slate-900 font-sans">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-100 px-6 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-violet-600 text-white rounded flex items-center justify-center font-bold italic text-xl">M</div>
          <span className="text-xl font-bold text-slate-800">MindMap AI V2</span>
        </div>
        
        <div className="hidden md:flex items-center space-x-8 text-sm font-semibold text-slate-600">
          <a href="#" className="hover:text-violet-600">AI Tools</a>
          <a href="#" className="hover:text-violet-600">Features</a>
          <a href="#" className="hover:text-violet-600">Pricing</a>
          <a href="#" className="hover:text-violet-600">Use Cases</a>
          <a href="#" className="hover:text-violet-600">Resources</a>
          <Globe size={18} className="text-slate-400" />
        </div>

        <div className="flex items-center space-x-4">
          <button className="px-5 py-2 text-violet-600 text-sm font-semibold border border-violet-200 rounded-lg hover:bg-violet-50 transition">
            Sign In
          </button>
          <button className="px-5 py-2 bg-violet-600 text-white text-sm font-semibold rounded-lg hover:bg-violet-700 transition shadow-md shadow-violet-200">
            Try For Free
          </button>
        </div>
      </nav>

      {/* Hero / Upload Section */}
      <header className="pt-20 pb-16 px-4 text-center max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold text-violet-700 mb-4 tracking-tight">
          Free AI PDF Summarizer
        </h1>
        <p className="text-lg text-slate-500 mb-10">
          Summarize Any PDF Instantly into a Structured Document
        </p>

        <div className="bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 p-8 max-w-3xl mx-auto">
          {!summary ? (
            <div className="space-y-6">
              {/* Dropzone */}
              <div 
                className={`border-2 border-dashed rounded-xl p-12 transition-all cursor-pointer flex flex-col items-center justify-center
                  ${isDragging ? 'border-violet-500 bg-violet-50' : 'border-violet-200 bg-[#fbfbfe] hover:bg-violet-50/50'}
                  ${file ? 'border-solid border-violet-400 bg-violet-50' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current.click()}
              >
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  className="hidden" 
                  accept=".pdf" 
                  onChange={handleFileChange}
                />
                
                {file ? (
                  <>
                    <CheckCircle2 size={48} className="text-green-500 mb-4" />
                    <p className="text-lg font-semibold text-slate-800">{file.name}</p>
                    <p className="text-sm text-slate-500 mt-2">Ready to summarize</p>
                  </>
                ) : (
                  <>
                    <Upload size={40} className="text-violet-500 mb-4" />
                    <p className="text-slate-700 font-medium mb-2">Click to upload or drag and drop PDF here</p>
                    <p className="text-violet-500 text-sm mb-6">Supported format: PDF</p>
                    <div className="bg-violet-100 text-violet-600 text-xs px-3 py-1 rounded-full font-medium">
                      PDF files only (MAX. 10MB or 50 pages)
                    </div>
                  </>
                )}
              </div>

              {/* Action Button */}
              <button 
                onClick={processFile}
                disabled={!file || isProcessing}
                className={`w-full py-4 rounded-xl flex items-center justify-center space-x-2 text-white font-bold text-lg transition-all
                  ${!file || isProcessing ? 'bg-violet-400 cursor-not-allowed' : 'bg-violet-600 hover:bg-violet-700 shadow-lg shadow-violet-200'}`}
              >
                {isProcessing ? (
                  <span className="animate-pulse">Processing Document...</span>
                ) : (
                  <>
                    <Sparkles size={20} />
                    <span>Summarize PDF</span>
                  </>
                )}
              </button>

              {/* Debug Links */}
              <div className="flex flex-col space-y-2 mt-6">
                <button 
                  type="button"
                  onClick={async () => {
                    setIsProcessing(true);
                    try {
                      const doc = new jsPDF();
                      doc.text("This is a test document about artificial intelligence. AI is transforming the world.", 10, 10);
                      const pdfBlob = doc.output('blob');
                      const testFile = new File([pdfBlob], "test.pdf", { type: "application/pdf" });
                      const result = await generateSummary(testFile, "student", "");
                      setSummary(result);
                    } catch (e) { alert(e.message); }
                    finally { setIsProcessing(false); }
                  }}
                  className="text-xs text-violet-400 hover:text-violet-600 underline"
                >
                  Test AI with Sample Text
                </button>
                
                <button 
                  type="button"
                  onClick={handleScan}
                  className="text-xs text-red-400 hover:text-red-600 flex items-center justify-center"
                >
                  <ShieldAlert size={12} className="mr-1" />
                  Diagnostic: Scan API Key for Available Models
                </button>
              </div>
            </div>
          ) : (
            /* Result View */
            <div className="text-left animate-in fade-in zoom-in duration-500">
              <div className="flex items-center justify-between border-b border-gray-100 pb-4 mb-6">
                <h3 className="text-xl font-bold text-slate-800">Summary Generated</h3>
                <div className="flex space-x-3">
                  <button 
                    onClick={() => { setSummary(''); setFile(null); }}
                    className="text-sm text-slate-500 hover:text-violet-600 font-medium"
                  >
                    Start Over
                  </button>
                  <button 
                    onClick={handleDownload}
                    className="bg-violet-600 text-white px-4 py-2 rounded-lg text-sm font-semibold flex items-center hover:bg-violet-700 transition"
                  >
                    <Download size={16} className="mr-2" />
                    Download PDF
                  </button>
                </div>
              </div>
              <div className="max-h-[500px] overflow-y-auto pr-4 custom-scrollbar prose prose-violet max-w-none">
                <ReactMarkdown>{summary}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* What Can It Do Section */}
      <section className="bg-white py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-violet-700 text-center mb-12">
            What Can the PDF Summarizer Do?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<FileText size={40} className="text-violet-500" />}
              title="1. Instant PDF to Summary Conversion"
              desc="Upload any PDF, and get a clean, organized summary instantly, no manual work needed."
            />
            <FeatureCard 
              icon={<MessageSquare size={40} className="text-violet-500" />}
              title="2. AI-Powered Key Section Extraction"
              desc="The AI summarize PDF feature detects key topics, arguments, and insights from large documents."
            />
            <FeatureCard 
              icon={<Maximize size={40} className="text-violet-500" />}
              title="3. Smart Document Understanding"
              desc="Works even with multi-page or scanned PDFs, analyzing headings, paragraphs, and structure intelligently."
            />
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="bg-[#fafafc] py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="space-y-4">
              <div className="aspect-[4/3] bg-white rounded-xl border border-violet-100 shadow-sm flex items-center justify-center mb-6 overflow-hidden relative group">
                 <div className="w-3/4 h-3/4 border-2 border-dashed border-violet-200 rounded-lg flex items-center justify-center bg-violet-50/50">
                    <Upload className="text-violet-400" size={32} />
                 </div>
              </div>
              <h3 className="text-xl font-bold text-violet-700">1. Upload Your PDF File</h3>
              <p className="text-slate-500 text-sm">Drag and drop or upload your PDF directly into the PDF Summarizer AI tool.</p>
            </div>
            <div className="space-y-4">
              <div className="aspect-[4/3] bg-white rounded-xl border border-violet-100 shadow-sm flex items-center justify-center mb-6">
                 <div className="bg-violet-600 text-white px-6 py-2 rounded-lg flex items-center space-x-2">
                   <Sparkles size={16} /> <span>Summarize</span>
                 </div>
              </div>
              <h3 className="text-xl font-bold text-violet-700">2. Generate the Summary</h3>
              <p className="text-slate-500 text-sm">Click "Summarize," and the AI PDF Summarizer will instantly extract main ideas.</p>
            </div>
            <div className="space-y-4">
              <div className="aspect-[4/3] bg-violet-50 rounded-xl border border-violet-100 shadow-sm flex items-center justify-center mb-6">
                 <FileOutput className="text-violet-500" size={48} />
              </div>
              <h3 className="text-xl font-bold text-violet-700">3. Customize & Share</h3>
              <p className="text-slate-500 text-sm">Refine your summary, export as a new PDF, or share it with your team.</p>
            </div>
          </div>
          <div className="text-center mt-12">
            <button className="bg-violet-600 text-white px-8 py-4 rounded-lg font-bold text-lg shadow-lg shadow-violet-200 hover:bg-violet-700 transition">
              Try PDF Summarizer for Free
            </button>
          </div>
        </div>
      </section>

      {/* Personas Section */}
      <section className="bg-white py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-violet-700 text-center mb-12">
            Who Can Benefit from the PDF Summarizer?
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
             <PersonaCard 
               icon={<GraduationCap size={20} className="text-violet-600" />}
               title="Students & Researchers"
               desc="Summarize research papers, theses, and textbooks into clear visual outlines."
             />
             <PersonaCard 
               icon={<Briefcase size={20} className="text-violet-600" />}
               title="Professionals & Analysts"
               desc="Convert long reports or policy documents into quick, shareable summaries."
             />
             <PersonaCard 
               icon={<PenTool size={20} className="text-violet-600" />}
               title="Writers & Journalists"
               desc="Review reference PDFs and extract key insights instantly."
             />
             <PersonaCard 
               icon={<Users size={20} className="text-violet-600" />}
               title="Educators & Trainers"
               desc="Create teaching summaries and class-ready visuals from academic PDFs."
             />
          </div>
        </div>
      </section>
    </div>
  );
}

const FeatureCard = ({ icon, title, desc }) => (
  <div className="bg-white rounded-2xl shadow-[0_4px_20px_rgb(0,0,0,0.05)] border border-gray-100 p-8 text-center hover:-translate-y-1 transition duration-300">
    <div className="flex justify-center mb-6">{icon}</div>
    <h3 className="text-lg font-bold text-slate-800 mb-3">{title}</h3>
    <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
  </div>
);

const PersonaCard = ({ icon, title, desc }) => (
  <div className="bg-white rounded-xl shadow-[0_2px_15px_rgb(0,0,0,0.03)] border border-gray-100 p-6 flex space-x-4 hover:shadow-md transition duration-300">
    <div className="w-12 h-12 bg-violet-100 rounded-full flex items-center justify-center shrink-0">
      {icon}
    </div>
    <div>
      <h3 className="text-lg font-bold text-slate-800 mb-2">{title}</h3>
      <p className="text-slate-500 text-sm">{desc}</p>
    </div>
  </div>
);

export default App;
