# AI Summarizer Pro

A full-stack web application that uses AI to summarize PDF documents into concise, persona-tailored summaries.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI Integration**: Google Gemini API
- **PDF Processing**: PyMuPDF (fitz)
- **PDF Generation**: ReportLab
- **Server**: Uvicorn ASGI
- **File Upload**: python-multipart
- **Environment**: python-dotenv

### Frontend
- **Framework**: React 18.2.0
- **Styling**: Tailwind CSS with @tailwindcss/typography
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Build Tool**: Create React App
- **Desktop App**: Electron

### Infrastructure
- **Language**: Python 3.13 (backend), Node.js (frontend)
- **Deployment**: Render (Web Service + Static Site)
- **Version Control**: Git

## Features

- **Persona-Based Summarization**: Choose from Student, Professional, or Researcher personas
- **Custom Goals**: Provide specific instructions for tailored summaries
- **Drag & Drop Upload**: Intuitive PDF upload with validation (max 10MB)
- **Real-Time Markdown Rendering**: Rich text display with copy functionality
- **PDF Export**: One-click conversion to downloadable PDF
- **Desktop App Support**: Run as native desktop application with Electron
- **Automated Cleanup**: Background task removes old exports after 24 hours

## Local Development

### Prerequisites
- Python 3.13+
- Node.js 16+
- Google Gemini API Key (free at https://makersuite.google.com/app/apikey)

### Setup
1. Clone the repository
2. Backend: `cd backend && pip install -r requirements.txt`
3. Frontend: `cd frontend && npm install`
4. Add your `GEMINI_API_KEY` to `backend/.env`
5. Run: `./start.bat` (Windows) or start servers manually

## Deployment Guide

### Backend (Render Web Service)
- **Root Directory**: `backend`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `GEMINI_API_KEY`: Your Google Gemini API key
  - `FRONTEND_URL`: Your frontend URL (e.g., https://your-frontend.onrender.com)

### Frontend (Render Static Site)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Publish Directory**: `build`
- **Environment Variables**:
  - `REACT_APP_API_URL`: Your backend URL (e.g., https://your-backend.onrender.com)

### Desktop App (Optional)
- Build with: `cd frontend && npm run dist`
- Creates executable in `frontend/dist/`

## Usage

1. Select a persona and enter a goal
2. Upload a PDF file
3. Click "Generate Summary"
4. View, copy, or export the summary

## License

MIT
```bash
cd frontend
npm install
```

### 3. Running the Application
You can run both servers simultaneously using the provided `start.bat` file (Windows) in the root directory:
```bash
.\start.bat
```
Alternatively, run them separately:
- **Backend**: `cd backend && python -m uvicorn main:app --reload --port 8000`
- **Frontend**: `cd frontend && npm start`

The application will be available at `http://localhost:3000`.
