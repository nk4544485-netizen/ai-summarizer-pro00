# AI Summarizer Pro

An AI-powered PDF summarizer application with a React frontend and Python FastAPI backend.

## Features

- Upload PDF files
- Extract text from PDFs
- Generate AI summaries using OpenAI or HuggingFace
- Download summarized PDFs

## Setup Instructions

### Prerequisites

- Node.js (for frontend)
- Python 3.8+ (for backend)
- OpenAI API key

### Backend Setup

1. Navigate to the `backend` directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env` and add your OpenAI API key

5. Run the server:
   ```
   python main.py
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

### Usage

1. Start both backend and frontend servers.
2. Open the frontend in your browser.
3. Upload a PDF file.
4. Get the summary.

## Troubleshooting

- Ensure API keys are set correctly.
- Check console for errors.
- Make sure ports 3000 (frontend) and 8000 (backend) are available.