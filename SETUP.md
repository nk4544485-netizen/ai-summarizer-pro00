# Setup Guide for AI Summarizer Pro

## Prerequisites

- Python 3.13+
- Node.js 16+ and npm
- A Google Gemini API Key (free tier available at https://makersuite.google.com/app/apikey)

## Local Development Setup

### 1. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env  # Windows
# or
cp .env.example .env    # Mac/Linux

# Edit .env and add your GEMINI_API_KEY
# GEMINI_API_KEY=your_actual_key_here
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

### 3. Running the Application

#### Option A: Using the Start Script (Windows)
```bash
# From project root
./start.bat
```

#### Option B: Manual - Run Both Servers

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend (from project root)
cd frontend
npm start
```

The app will be available at `http://localhost:3000`

#### Option C: Electron Desktop App

```bash
cd frontend
npm run electron-dev
```

## Project Structure

- **backend/**: FastAPI server with Gemini integration
  - `main.py`: Core API endpoints
  - `requirements.txt`: Python dependencies
  - `.env`: API keys and configuration
  
- **frontend/**: React application
  - `src/`: React components and pages
  - `public/electron.js`: Electron main process
  - `package.json`: Dependencies and scripts

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Make sure you've added your API key to `backend/.env`

### Issue: Backend server won't start
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Frontend shows "Backend server is offline"
**Solution**: 
1. Check if backend is running on http://localhost:8000
2. Check CORS settings in `backend/main.py`
3. Verify `FRONTEND_URL` in `.env` matches your frontend URL

### Issue: node_modules conflicts
**Solution**: 
```bash
cd frontend
rm -r node_modules
npm install
```

## Deployment

See [README.md](README.md) for deployment instructions to Render.

## Environment Variables Reference

### Backend (`backend/.env`)
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FRONTEND_URL`: Frontend URL (defaults to http://localhost:3000)
- `PORT`: Server port (defaults to 8000)

### Frontend (`frontend/.env`)
- `REACT_APP_API_URL`: Backend API URL (defaults to http://localhost:8000)