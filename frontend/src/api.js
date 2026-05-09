import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const summarizePDF = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/summarize`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error calling the Summarization API:", error);
    throw error;
  }
};

export const generatePDF = async (text) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate-pdf`, { text }, {
      responseType: 'blob',
    });
    // Create a Blob from the PDF Stream
    const file = new Blob([response.data], { type: 'application/pdf' });
    // Build a URL from the file
    const fileURL = URL.createObjectURL(file);
    // Create a link and click it to trigger download
    const link = document.createElement('a');
    link.href = fileURL;
    link.download = 'summary_output.pdf';
    link.click();
  } catch (error) {
    console.error("Error generating PDF:", error);
    throw error;
  }
};
