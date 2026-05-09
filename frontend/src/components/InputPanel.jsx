import React, { useState, useRef } from 'react';

const UploadCloud = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m16 16-4-4-4 4"/></svg>;
const FileText = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>;
const X = ({ size = 24, className = "" }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>;

const InputPanel = ({ onSubmit, isLoading }) => {
  const [persona, setPersona] = useState('Student');
  const [objective, setObjective] = useState('');
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type !== 'application/pdf') {
        alert("Invalid format: Please upload a valid PDF file.");
        return;
      }
      if (droppedFile.size > 10 * 1024 * 1024) {
        alert("File too large: Please upload a PDF strictly under 10MB.");
        return;
      }
      setFile(droppedFile);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'application/pdf') {
        alert("Invalid format: Please upload a valid PDF file.");
        return;
      }
      if (selectedFile.size > 10 * 1024 * 1024) {
        alert("File too large: Please upload a PDF strictly under 10MB.");
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload a PDF file.");
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('persona', persona);
    formData.append('goal', objective);
    
    onSubmit(formData);
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h2 className="text-xl font-bold mb-6 text-gray-800 flex items-center">
        <FileText className="mr-2 text-[#7e34f6]" size={24} />
        Document Setup
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Persona Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">Select Persona</label>
          <div className="flex flex-wrap gap-3">
            {['Student', 'Professional', 'Researcher'].map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => setPersona(p)}
                className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 border
                  ${persona === p 
                    ? 'bg-[#7e34f6] text-white border-[#7e34f6] shadow-md shadow-violet-200' 
                    : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100 hover:border-gray-300'
                  }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Objective Input */}
        <div>
          <label htmlFor="objective" className="block text-sm font-semibold text-gray-700 mb-3">
            What is your goal? (Optional)
          </label>
          <textarea
            id="objective"
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            placeholder="e.g. Focus on key definitions and formulas..."
            className="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#7e34f6]/50 focus:border-[#7e34f6] outline-none transition-all resize-none text-gray-700 placeholder-gray-400"
            rows="3"
          />
        </div>

        {/* PDF Upload Zone */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">Upload PDF Document</label>
          
          <div 
            className={`relative border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center transition-all duration-200
              ${dragActive ? 'border-[#7e34f6] bg-violet-50' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".pdf"
              onChange={handleChange}
              className="hidden"
            />
            
            {file ? (
              <div className="flex flex-col items-center text-center">
                <div className="bg-violet-100 p-3 rounded-full mb-3 text-[#7e34f6]">
                  <FileText size={32} />
                </div>
                <p className="text-sm font-medium text-gray-800">{file.name}</p>
                <p className="text-xs text-gray-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                <button 
                  type="button" 
                  onClick={(e) => { e.preventDefault(); setFile(null); }}
                  className="mt-4 text-xs font-semibold text-red-500 hover:text-red-700 flex items-center"
                >
                  <X size={14} className="mr-1" /> Remove File
                </button>
              </div>
            ) : (
              <>
                <div className="bg-white p-4 rounded-full shadow-sm mb-4 text-[#7e34f6]">
                  <UploadCloud size={32} />
                </div>
                <p className="text-base font-semibold text-gray-700 mb-1">
                  Drag & drop your PDF here
                </p>
                <p className="text-sm text-gray-500 mb-4">or click to browse from your computer</p>
                <button
                  type="button"
                  onClick={() => inputRef.current.click()}
                  className="px-5 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors shadow-sm"
                >
                  Browse Files
                </button>
              </>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !file}
          className={`w-full py-3.5 px-6 rounded-xl text-white font-semibold text-base transition-all duration-200 shadow-md flex items-center justify-center
            ${isLoading || !file 
              ? 'bg-gray-300 cursor-not-allowed shadow-none' 
              : 'bg-[#7e34f6] hover:bg-[#6c2ae0] hover:shadow-lg hover:shadow-violet-200'}`}
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              AI is analyzing...
            </>
          ) : (
            'Generate Summary'
          )}
        </button>
      </form>
    </div>
  );
};

export default InputPanel;
