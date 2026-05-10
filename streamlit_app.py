import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------- Custom Design Injector -----------------
def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        /* Global Text Visibility Fix - Dark Navy */
        html, body, [data-testid="stWidgetLabel"], .stText, p, h1, h2, h3, h4, span, label {
            color: #1E1E2E !important; 
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f3ff 0%, #fdf2f8 100%);
        }
        
        /* Hero Section */
        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            text-align: center;
            background: linear-gradient(90deg, #7c3aed 0%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem !important;
        }
        
        /* Feature Cards */
        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #7c3aed !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            border: none !important;
            width: 100%;
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
    return "".join([page.get_text() for page in doc]).strip()

def generate_summary(text, persona, goal):
    # Model List for 2026 Fallback Logic
    model_list = ['gemini-3.1-flash-lite', 'gemini-3-flash-preview', 'gemini-2.5-flash']
    
    last_error = ""
    for model_name in model_list:
        try:
            instructions = f"You are a professional assistant helping a {persona}. Goal: {goal}"
            model = genai.GenerativeModel(model_name=model_name, system_instruction=instructions)
            
            response = model.generate_content(
                f"Please provide a clear summary of this PDF content:\n\n{text[:20000]}",
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
            return response.text
        except Exception as e:
            last_error = str(e)
            if "404" in last_error or "not found" in last_error.lower():
                continue # Try next model
            else:
                return f"❌ AI Error: {last_error}"
                
    return f"❌ Failed to reach any AI model. Last error: {last_error}"

# ----------------- UI Content -----------------
st.markdown('<h1 class="hero-title">Free AI PDF Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4B5563; margin-bottom: 2rem;">Summarize Any PDF Instantly with Gemini 3.1 Flash-Lite</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### ⚙️ Setup")
        persona = st.selectbox("Persona", ["Student", "Professional", "Researcher", "General"])
        goal = st.text_area("Goal", placeholder="What do you want to extract?")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if st.button("Generate Summary", type="primary"):
            if uploaded_file:
                with st.spinner("🤖 AI is processing..."):
                    text = extract_text(uploaded_file)
                    if text:
                        st.session_state['summary'] = generate_summary(text, persona, goal)
                    else:
                        st.error("❌ Could not extract text from PDF.")
            else:
                st.error("Please upload a PDF.")

with col2:
    with st.container(border=True):
        st.markdown("### 📝 AI Analysis")
        if 'summary' in st.session_state:
            st.markdown(st.session_state['summary'])
        else:
            st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; color: #94a3b8;'>Your summary will appear here.</div>", unsafe_allow_html=True)
