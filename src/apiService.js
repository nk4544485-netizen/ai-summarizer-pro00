import { GoogleGenerativeAI } from '@google/generative-ai';
import { jsPDF } from 'jspdf';
import * as pdfjsLib from 'pdfjs-dist';

// Configuration
// Synchronizing with installed pdfjs-dist version (5.7.284)
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@5.7.284/build/pdf.worker.min.mjs`;

/**
 * Extracts text from PDF
 */
export const extractTextFromPDF = async (file) => {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  let text = '';
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    text += content.items.map(item => item.str).join(' ') + '\n';
  }
  return text;
};

/**
 * Generates Summary via FastAPI Backend
 */
export const generateSummary = async (file, persona = "student", goal = "") => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('persona', persona);
  formData.append('goal', goal);

  const response = await fetch('http://localhost:8000/summarize', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Failed to generate summary');
  }

  return data.summary;
};

/**
 * Diagnostics: List all models available
 */
export const listAvailableModels = async () => {
  try {
    const response = await fetch('http://localhost:8000/models');
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Failed to fetch models');
    return data.models;
  } catch (error) {
    console.error("List Models Error:", error);
    throw error;
  }
};
/**
 * Exports summary as PDF
 */
export const exportToPDF = (text) => {
  const doc = new jsPDF();
  const margin = 20;
  const pageWidth = doc.internal.pageSize.getWidth();
  const lines = doc.splitTextToSize(text.replace(/[#*]/g, ''), pageWidth - margin * 2);
  
  doc.setFont("helvetica", "bold");
  doc.text("AI Summarizer Pro - Result", margin, 20);
  doc.setFont("helvetica", "normal");
  doc.setFontSize(11);
  
  let y = 30;
  lines.forEach(line => {
    if (y > 280) {
      doc.addPage();
      y = 20;
    }
    doc.text(line, margin, y);
    y += 7;
  });
  
  doc.save('summary_report.pdf');
};
