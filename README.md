# MindMap AI V2 - Streamlit Edition

A simple, fast, and powerful PDF summarizer powered by Google Gemini and Streamlit.

## Features
- **PDF Text Extraction**: Securely extracts text from PDFs locally using PyMuPDF.
- **Gemini AI Integration**: Uses Gemini 3.1 Flash Preview for high-quality summaries.
- **Persona-based Summaries**: Tailors the summary to Students, Professionals, or Researchers.
- **Export to PDF**: Instantly download the generated summary as a formatted PDF.

## Setup & Installation

### Prerequisites
- Python 3.10+
- A Google Gemini API Key

### Installation

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Setup your API Key:
Create a `.streamlit/secrets.toml` file in the root directory:
```toml
GEMINI_API_KEY = "your_google_gemini_api_key_here"
```

### Running the App
```bash
streamlit run app.py
```

## Deployment
This application is fully prepared for **Streamlit Community Cloud**:
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Select your repository, set the main file path to `app.py`.
4. In the Advanced Settings, paste your `GEMINI_API_KEY` into the Secrets box.
5. Click Deploy!
