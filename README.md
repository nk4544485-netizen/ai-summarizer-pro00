# AI Summarizer Pro

AI Summarizer Pro is a full-stack application that leverages Google's Gemini AI to summarize large PDF documents quickly and accurately. It features a modern React frontend and a robust FastAPI backend.

## Features
- **PDF Text Extraction**: Securely extracts text from PDFs.
- **Gemini AI Integration**: Uses the latest Gemini 3.1 Flash Preview models.
- **Persona-based Summaries**: Tailors the summary to Students, Professionals, or Researchers.
- **Export to PDF**: Download the generated summary as a clean, formatted PDF.

## Tech Stack
- **Frontend**: React, Vite, TailwindCSS, jsPDF
- **Backend**: Python, FastAPI, Uvicorn, Google Generative AI SDK, PyMuPDF

## Prerequisites
- Node.js (v18 or higher)
- Python (3.10 or higher)
- A Google Gemini API Key

## Setup & Installation

### 1. Backend Setup
Navigate to the `backend` directory and set up the environment:
```bash
cd backend
python -m venv .venv
# Activate the virtual environment:
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory (you can copy `.env.example`):
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
PORT=8000
FRONTEND_URL=http://localhost:5555
```

### 2. Frontend Setup
Navigate back to the project root and install the dependencies:
```bash
cd ..
npm install
```

## Running the Application

### Start the Backend
Open a terminal, activate your virtual environment, and run:
```bash
cd backend
python main.py
```
The backend will run on `http://localhost:8000`.

### Start the Frontend
In a new terminal, run:
```bash
npm run dev
# OR use the provided batch script on Windows:
.\start.bat
```
The frontend will start on `http://localhost:5555/`.

## Contributing
Feel free to open issues or submit pull requests for any improvements or bug fixes.
