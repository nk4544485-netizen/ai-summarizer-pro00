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
        
        /* Global Text Visibility Fix */
        html, body, [data-testid="stWidgetLabel"], .stText, p, h1, h2, h3, h4, span, label {
            color: #1E1E2E !important; /* Dark Navy for visibility */
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
        
        .hero-subtitle {
            text-align: center;
            color: #4B5563 !important;
            font-size: 1.2rem;
            margin-bottom: 3rem;
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
        
        .feature-card p {
            color: #4B5563 !important; /* Professional Grey for descriptions */
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
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #6d28d9 !important;
            box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.4) !important;
        }

        /* Upload Component */
        [data-testid="stFileUploader"] {
            border: 2px dashed #7c3aed;
            border-radius: 15px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.5);
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
    # Model Fix: Using gemini-1.5-flash as requested
    model_name = 'gemini-1.5-flash'
    
    try:
        instructions = f"You are an AI assistant helping a {persona}. Goal: {goal}"
        model = genai.GenerativeModel(model_name=model_name, system_instruction=instructions)
        
        response = model.generate_content(
            f"Please summarize the following PDF text:\n\n{text[:15000]}",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        return response.text
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            return f"❌ Model Error (404): The model '{model_name}' was not found. Please verify your API key supports this model or check the Google AI model list."
        return f"❌ AI Error: {str(e)}"

# ----------------- UI Content -----------------

# Navbar
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 5%;">
        <div style="font-weight: 800; font-size: 1.5rem; color: #1E1E2E;">
            <span style="background: #7c3aed; color: white; padding: 4px 10px; border-radius: 8px;">M</span>
            MindMap AI
        </div>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<h1 class="hero-title">Free AI PDF Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Summarize Any PDF Instantly into a Visual Mind Map.</p>', unsafe_allow_html=True)

# Main Tool
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Document Setup")
    persona = st.selectbox("Select Persona", ["Student", "Professional", "Researcher", "General"])
    goal = st.text_area("What is your goal? (Optional)", placeholder="e.g. Extract key facts...")
    st.markdown("#### Upload PDF Document")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    
    if st.button("Generate Summary"):
        if uploaded_file:
            with st.spinner("Processing..."):
                text = extract_text(uploaded_file)
                if text:
                    st.session_state['summary'] = generate_summary(text, persona, goal)
                else:
                    st.error("❌ Could not extract text from PDF.")
        else:
            st.error("Please upload a PDF.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if 'summary' in st.session_state:
        st.markdown('<div class="feature-card" style="min-height: 450px;">', unsafe_allow_html=True)
        st.markdown("### 📝 AI Result")
        st.markdown(st.session_state['summary'])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="feature-card" style="min-height: 450px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">', unsafe_allow_html=True)
        st.markdown("<div style='font-size: 4rem;'>📄</div>", unsafe_allow_html=True)
        st.markdown("<h4>No Summary Yet</h4>", unsafe_allow_html=True)
        st.markdown("<p>Upload a document and click 'Generate Summary' to see results here.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Who Benefits Section
st.divider()
st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Who Benefits from MindMap AI?</h2>", unsafe_allow_html=True)
b_col1, b_col2 = st.columns(2)
with b_col1:
    st.markdown('<div class="feature-card"><h4>🎓 For Students</h4><p>Convert long textbooks into easy study notes and definitions.</p></div>', unsafe_allow_html=True)
with b_col2:
    st.markdown('<div class="feature-card"><h4>💼 For Professionals</h4><p>Quickly extract action items and metrics from long reports.</p></div>', unsafe_allow_html=True)
