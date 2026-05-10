import React, { useState, useRef } from 'react';
import { Upload, FileText, User, Target, X, Loader2 } from 'lucide-react';

const InputPanel = ({ onSummarize, isLoading }) => {
  const [persona, setPersona] = useState('Student');
  const [goal, setGoal] = useState('');
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) setFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) onSummarize({ file, persona, goal });
  };

  return (
    <div className="glass-card rounded-[2.5rem] p-8 h-full">
      <div className="flex items-center space-x-3 mb-8">
        <div className="p-3 bg-violet-500 rounded-2xl text-white shadow-lg shadow-violet-200">
          <FileText size={22} />
        </div>
        <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Configuration</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Persona Selection */}
        <div>
          <label className="flex items-center text-sm font-bold text-slate-600 mb-4 uppercase tracking-widest">
            <User size={14} className="mr-2" /> Target Persona
          </label>
          <div className="grid grid-cols-3 gap-3">
            {['Student', 'Professional', 'Researcher'].map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => setPersona(p)}
                className={`py-3 px-2 rounded-2xl text-xs font-bold transition-all duration-300 border-2
                  ${persona === p 
                    ? 'bg-violet-600 border-violet-600 text-white shadow-lg shadow-violet-200' 
                    : 'bg-slate-50 border-transparent text-slate-500 hover:bg-slate-100'}`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Goal Input */}
        <div>
          <label className="flex items-center text-sm font-bold text-slate-600 mb-4 uppercase tracking-widest">
            <Target size={14} className="mr-2" /> Custom Objective
          </label>
          <textarea
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g. Focus on key findings and methodology..."
            className="input-field min-h-[100px] resize-none"
          />
        </div>

        {/* File Upload */}
        <div>
          <label className="flex items-center text-sm font-bold text-slate-600 mb-4 uppercase tracking-widest">
            <Upload size={14} className="mr-2" /> Document Source
          </label>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`relative group border-2 border-dashed rounded-[2rem] p-8 transition-all duration-300 flex flex-col items-center justify-center cursor-pointer
              ${dragActive ? 'border-violet-500 bg-violet-50' : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-300'}`}
            onClick={() => fileInputRef.current.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="hidden"
            />
            
            {file ? (
              <div className="text-center animate-in zoom-in-95 duration-300">
                <div className="w-16 h-16 bg-green-100 text-green-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <FileText size={32} />
                </div>
                <p className="text-sm font-bold text-slate-700 truncate max-w-[200px]">{file.name}</p>
                <button 
                  onClick={(e) => { e.stopPropagation(); setFile(null); }}
                  className="mt-3 text-xs text-red-500 font-bold flex items-center justify-center hover:text-red-600 mx-auto"
                >
                  <X size={12} className="mr-1" /> Remove
                </button>
              </div>
            ) : (
              <div className="text-center">
                <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto mb-4 text-violet-500 group-hover:scale-110 transition-transform">
                  <Upload size={32} />
                </div>
                <p className="text-sm font-bold text-slate-700">Drop your PDF here</p>
                <p className="text-xs text-slate-400 mt-1">or browse files (Max 40MB)</p>
              </div>
            )}
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !file}
          className="premium-button w-full flex items-center justify-center space-x-3"
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              <span>Analyzing Document...</span>
            </>
          ) : (
            <span>Distill Knowledge</span>
          )}
        </button>
      </form>
    </div>
  );
};

export default InputPanel;
