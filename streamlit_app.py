import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
from dotenv import load_dotenv
import base64

load_dotenv()

# ----------------- Configuration -----------------
st.set_page_config(
    page_title="SummarizerPro - AI PDF Summarizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- Styling -----------------
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Navbar */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 5%;
        background: white;
        border-bottom: 1px solid #f1f5f9;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: #64748b;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .btn-try {
        background: #7e34f6;
        color: white !important;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
    }
    
    /* Tool Layout */
    .tool-section {
        padding: 3rem 5%;
    }
    
    .setup-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        # border: 1px solid #e2e8f0;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* Persona Buttons */
    .persona-container {
        display: flex;
        gap: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* Upload Box */
    .upload-box {
        border: 2px dashed #e2e8f0;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f8fafc;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .upload-box:hover {
        border-color: #7e34f6;
        background: #f5f3ff;
    }
    
    /* Custom Streamlit Overrides */
    .stButton>button {
        background: #7e34f6;
        color: white;
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-weight: 600;
        border: none;
    }
    
    .stButton>button:hover {
        background: #6d28d9;
        color: white;
    }
    
    [data-testid="stHeader"] {
        display: none;
    }
    
    /* Result Area */
    .result-placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        min-height: 400px;
        color: #64748b;
        text-align: center;
    }
    
    .result-card {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        min-height: 500px;
        border: 1px solid #f1f5f9;
    }
    
    /* Hide default streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ----------------- Navbar -----------------
st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">
            <span style="background: #7e34f6; color: white; padding: 4px 8px; border-radius: 6px;">S</span>
            SummarizerPro
        </div>
        <div class="nav-links">
            <a href="#" class="nav-link">AI Tools</a>
            <a href="#" class="nav-link">Features</a>
            <a href="#" class="btn-try">Try For Free</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------- Logic -----------------
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def generate_summary(text, persona, goal):
    instructions = {
        "Student": "You are an AI assistant for a student. Focus on study notes and definitions.",
        "Professional": "You are an AI assistant for a professional. Focus on executive summaries and action items.",
        "Researcher": "You are an AI assistant for a researcher. Focus on methodology and findings."
    }.get(persona, "You are a helpful assistant.")
    
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instructions)
    prompt = f"Goal: {goal}\n\nText:\n{text[:15000]}"
    response = model.generate_content(prompt)
    return response.text if response else "Failed to generate summary."

# ----------------- App Content -----------------
st.markdown('<div class="tool-section">', unsafe_allow_html=True)

col_setup, col_result = st.columns([1, 1.2], gap="large")

with col_setup:
    st.markdown("""
        <div class="section-title">
            <span style="color: #7e34f6;">📄</span> Document Setup
        </div>
    """, unsafe_allow_html=True)
    
    # Persona Selection
    st.markdown('<p style="font-weight: 500; color: #475569; margin-bottom: 0.5rem;">Select Persona</p>', unsafe_allow_html=True)
    persona = st.radio("", ["Student", "Professional", "Researcher"], horizontal=True, label_visibility="collapsed")
    
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
    
    # Goal Input
    goal = st.text_area("What is your goal? (Optional)", placeholder="e.g. Extract key methodology...", height=100)
    
    # File Upload
    st.markdown('<p style="font-weight: 500; color: #475569; margin-top: 1.5rem;">Upload PDF Document</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file:
        st.markdown(f"""
            <div style="background: #f1f5f9; padding: 1rem; border-radius: 8px; margin-top: 10px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #7e34f6;">📄</span>
                    <div>
                        <div style="font-weight: 600; font-size: 0.9rem;">{uploaded_file.name}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">{(uploaded_file.size/1024):.2f} KB</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    
    if st.button("Generate Summary"):
        if not uploaded_file:
            st.error("Please upload a PDF first.")
        elif not api_key:
            st.error("API Key not configured.")
        else:
            with st.spinner("Analyzing..."):
                text = extract_text(uploaded_file)
                st.session_state['summary_result'] = generate_summary(text, persona, goal)

with col_result:
    if 'summary_result' in st.session_state:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### AI Summary")
        st.markdown(st.session_state['summary_result'])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="result-placeholder">
                <img src="https://cdn-icons-png.flaticon.com/512/2991/2991112.png" width="80" style="opacity: 0.2; margin-bottom: 20px;">
                <h3 style="color: #1e293b;">No Summary Yet</h3>
                <p>Upload a document and click "Generate Summary" to see the AI-generated results here.</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Footer Sections -----------------
st.divider()

# Features Section
st.markdown("""
    <div style="text-align: center; padding: 4rem 0;">
        <h2 style="font-size: 2rem; color: #1e293b; margin-bottom: 3rem;">What Can the PDF Summarizer Do?</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; padding: 0 5%;">
            <div class="setup-card" style="border: 1px solid #f1f5f9; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📄</div>
                <h4 style="margin-bottom: 1rem;">1. Instant PDF Conversion</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Upload any PDF and get a clean, organized summary in seconds.</p>
            </div>
            <div class="setup-card" style="border: 1px solid #f1f5f9; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
                <h4 style="margin-bottom: 1rem;">2. AI-Powered Extraction</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Our AI detects key topics, arguments, and insights automatically.</p>
            </div>
            <div class="setup-card" style="border: 1px solid #f1f5f9; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
                <h4 style="margin-bottom: 1rem;">3. Smart Understanding</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Works with multi-page or scanned PDFs intelligently.</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
