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

# ----------------- Custom Design Injector -----------------
def inject_custom_design():
    st.markdown("""
        <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        /* Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f3ff 0%, #fdf2f8 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Typography */
        h1, h2, h3 {
            color: #1e293b !important;
            font-weight: 800 !important;
        }
        
        p, span, label {
            color: #475569;
        }
        
        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 4rem 1rem;
        }
        
        .hero-title {
            font-size: 3.5rem !important;
            margin-bottom: 1rem !important;
            background: linear-gradient(90deg, #7c3aed 0%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #64748b;
            max-width: 700px;
            margin: 0 auto 2rem auto;
        }
        
        /* Feature Cards */
        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border: 1px solid #f1f5f9;
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        /* Upload Component Customization */
        [data-testid="stFileUploader"] {
            border: 2px dashed #7c3aed;
            border-radius: 15px;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.5);
        }
        
        [data-testid="stFileUploader"] section {
            padding: 0;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #7c3aed !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #6d28d9 !important;
            box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.4) !important;
            transform: scale(1.02);
        }
        
        /* Navbar Overlay */
        .nav-overlay {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 5%;
            position: absolute;
            top: 0;
            width: 100%;
            z-index: 100;
        }
        
        .nav-logo {
            font-weight: 800;
            font-size: 1.5rem;
            color: #1e293b;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Hide default header */
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        </style>
    """, unsafe_allow_html=True)

# ----------------- App Configuration -----------------
st.set_page_config(
    page_title="SummarizerPro - AI PDF Summarizer",
    page_icon="🧠",
    layout="wide"
)

inject_custom_design()

# ----------------- Logic -----------------
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def generate_summary(text, persona, goal):
    instructions = f"You are an AI assistant helping a {persona}. Focus on their specific needs. Goal: {goal}"
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instructions)
    prompt = f"Please summarize the following text:\n\n{text[:15000]}"
    response = model.generate_content(prompt)
    return response.text if response else "Failed to generate summary."

# ----------------- UI Content -----------------

# 1. Navbar
st.markdown("""
    <div class="nav-overlay">
        <div class="nav-logo">
            <div style="background: #7c3aed; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white;">M</div>
            MindMap AI
        </div>
        <div style="display: flex; gap: 2rem; align-items: center;">
            <span style="font-weight: 500; cursor: pointer;">AI Tools</span>
            <span style="font-weight: 500; cursor: pointer;">Features</span>
            <span style="font-weight: 500; cursor: pointer;">Pricing</span>
            <div style="background: #7c3aed; color: white; padding: 0.5rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer;">Try For Free</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. Hero Section
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Free AI PDF Summarizer</h1>
        <p class="hero-subtitle">Summarize Any PDF Instantly into a Visual Mind Map and comprehensive notes using advanced Gemini AI.</p>
    </div>
""", unsafe_allow_html=True)

# 3. Main Tool Interface
tool_col1, tool_col2 = st.columns([1, 1.2], gap="large")

with tool_col1:
    st.markdown("### ⚙️ Document Setup")
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    persona = st.selectbox("Select Persona", ["Student", "Professional", "Researcher", "General"])
    goal = st.text_area("What is your goal? (Optional)", placeholder="e.g. Check for spelling mistakes or extract key facts...", height=100)
    
    st.markdown("#### Upload PDF Document")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    
    if st.button("Generate Summary"):
        if uploaded_file:
            with st.spinner("Processing..."):
                text = extract_text(uploaded_file)
                st.session_state['summary'] = generate_summary(text, persona, goal)
        else:
            st.error("Please upload a file.")
    st.markdown('</div>', unsafe_allow_html=True)

with tool_col2:
    if 'summary' in st.session_state:
        st.markdown("### 📝 AI Result")
        st.markdown(f"""
            <div class="feature-card" style="min-height: 450px;">
                {st.session_state['summary']}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 📝 AI Result")
        st.markdown("""
            <div class="feature-card" style="min-height: 450px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: #94a3b8;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
                <h4>No Summary Yet</h4>
                <p>Upload a document and click "Generate Summary" to see the results here.</p>
            </div>
        """, unsafe_allow_html=True)

# 4. "Who Benefits" Section
st.divider()
st.markdown("<h2 style='text-align: center; margin-bottom: 3rem;'>Who Benefits from MindMap AI?</h2>", unsafe_allow_html=True)

ben_col1, ben_col2 = st.columns(2, gap="medium")

with ben_col1:
    st.markdown("""
        <div class="feature-card">
            <h4>🎓 For Students</h4>
            <p>Convert long textbooks and research papers into easy-to-digest study notes and definitions. Save hours of manual reading.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-card">
            <h4>💼 For Professionals</h4>
            <p>Quickly extract action items, metrics, and executive summaries from long reports, contracts, and meeting transcripts.</p>
        </div>
    """, unsafe_allow_html=True)

with ben_col2:
    st.markdown("""
        <div class="feature-card">
            <h4>🔍 For Researchers</h4>
            <p>Identify methodology, key findings, and critical analysis across multiple papers in minutes. Keep your research organized.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-card">
            <h4>✍️ For Content Creators</h4>
            <p>Turn complex documents into structured outlines for scripts, blog posts, and educational content effortlessly.</p>
        </div>
    """, unsafe_allow_html=True)

# 5. Features Section (Grid style)
st.divider()
st.markdown("<h2 style='text-align: center; margin-bottom: 3rem;'>What Can the PDF Summarizer Do?</h2>", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📄</div>
            <h4>Instant Conversion</h4>
            <p>Get a clean, organized summary in seconds.</p>
        </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧠</div>
            <h4>AI-Powered Extraction</h4>
            <p>Detects key topics and arguments automatically.</p>
        </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
            <h4>Smart Understanding</h4>
            <p>Intelligently analyzes complex visual structures.</p>
        </div>
    """, unsafe_allow_html=True)
