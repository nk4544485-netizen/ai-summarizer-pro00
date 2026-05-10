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
        
        h1, h2, h3, h4 {
            color: #1e293b !important;
            font-weight: 800 !important;
        }
        
        .stButton>button {
            background-color: #7c3aed !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            width: 100%;
        }
        
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #f1f5f9 !important;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="SummarizerPro AI", page_icon="🧠", layout="wide")
inject_custom_design()

# ----------------- Logic -----------------
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ GEMINI_API_KEY is missing in Secrets.")
    st.stop()

genai.configure(api_key=api_key)

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def generate_summary(text, persona, goal):
    # Try multiple model variants to ensure compatibility
    model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
    
    for model_name in model_names:
        try:
            instructions = f"You are an AI assistant helping a {persona}. Goal: {goal}"
            model = genai.GenerativeModel(model_name, system_instruction=instructions)
            response = model.generate_content(f"Summarize this content:\n\n{text[:15000]}")
            return response.text
        except Exception as e:
            if model_name == model_names[-1]: # If last model also fails
                return f"Error with all models: {str(e)}"
            continue

# ----------------- UI -----------------
st.markdown("<h1 style='text-align: center;'>MindMap AI Summarizer</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### ⚙️ Setup")
        persona = st.selectbox("Persona", ["Student", "Professional", "Researcher", "General"])
        goal = st.text_area("Goal", placeholder="What do you need?")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if st.button("Generate Summary", type="primary"):
            if uploaded_file:
                with st.spinner("🧠 AI is thinking..."):
                    text = extract_text(uploaded_file)
                    st.session_state['summary'] = generate_summary(text, persona, goal)
            else:
                st.error("Please upload a file.")

with col2:
    with st.container(border=True):
        st.markdown("### 📝 Result")
        if 'summary' in st.session_state:
            st.markdown(st.session_state['summary'])
        else:
            st.markdown("Result will appear here.")
