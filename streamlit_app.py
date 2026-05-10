import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
from dotenv import load_dotenv

load_dotenv()

# ----------------- Custom Design -----------------
def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f5f3ff 0%, #fdf2f8 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Heading Colors */
        h1, h2, h3, h4 {
            color: #1e293b !important;
            font-weight: 800 !important;
        }
        
        /* Navbar Styling */
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        
        /* Button Styling */
        .stButton>button {
            background-color: #7c3aed !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            width: 100%;
        }
        
        /* Card-like containers using Streamlit native border */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #f1f5f9 !important;
            padding: 10px;
        }
        
        /* File Uploader styling */
        [data-testid="stFileUploader"] {
            border: 2px dashed #7c3aed !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="SummarizerPro AI", page_icon="🧠", layout="wide")
inject_custom_design()

# ----------------- Logic -----------------
# SECRETS CHECK: Very important for Cloud
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ GEMINI_API_KEY is missing. Please add it to your Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def generate_summary(text, persona, goal):
    instructions = f"You are an AI assistant helping a {persona}. Goal: {goal}"
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instructions)
    response = model.generate_content(f"Summarize this PDF content:\n\n{text[:15000]}")
    return response.text if response else "Error generating summary."

# ----------------- UI -----------------

# Navbar
cols = st.columns([2, 3, 1])
with cols[0]:
    st.markdown("### 🧠 MindMap AI")
with cols[2]:
    st.button("Try For Free", key="nav_btn")

# Hero
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>Free AI PDF Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Summarize Any PDF Instantly into a Visual Mind Map.</p>", unsafe_allow_html=True)

st.divider()

# Main Tool
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### ⚙️ Document Setup")
        persona = st.selectbox("Select Persona", ["Student", "Professional", "Researcher", "General"])
        goal = st.text_area("What is your goal? (Optional)", placeholder="e.g. Extract key facts...")
        st.markdown("#### Upload PDF Document")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf"], label_visibility="collapsed")
        
        if st.button("Generate Summary", type="primary"):
            if uploaded_file:
                with st.spinner("Analyzing..."):
                    try:
                        text = extract_text(uploaded_file)
                        st.session_state['summary'] = generate_summary(text, persona, goal)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("Please upload a PDF.")

with col2:
    with st.container(border=True):
        st.markdown("### 📝 AI Result")
        if 'summary' in st.session_state:
            st.markdown(st.session_state['summary'])
        else:
            st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; color: #94a3b8;'>No Summary Yet</div>", unsafe_allow_html=True)

# Benefits
st.divider()
bcols = st.columns(3)
with bcols[0]:
    with st.container(border=True):
        st.markdown("#### 🎓 For Students")
        st.markdown("Convert long textbooks into easy study notes.")
with bcols[1]:
    with st.container(border=True):
        st.markdown("#### 💼 For Professionals")
        st.markdown("Extract action items from long reports.")
with bcols[2]:
    with st.container(border=True):
        st.markdown("#### 🔍 For Researchers")
        st.markdown("Identify methodology and findings instantly.")
