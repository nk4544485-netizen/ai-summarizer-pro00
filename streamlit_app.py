import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------- Custom Design -----------------
def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        .stApp { background: linear-gradient(135deg, #f5f3ff 0%, #fdf2f8 100%); font-family: 'Inter', sans-serif; }
        h1, h2, h3, h4 { color: #1e293b !important; font-weight: 800 !important; }
        .stButton>button { background-color: #7c3aed !important; color: white !important; border-radius: 10px !important; border: none !important; width: 100%; font-weight: 600; }
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: white; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #f1f5f9 !important; padding: 20px; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="SummarizerPro AI", page_icon="🧠", layout="wide")
inject_custom_design()

# ----------------- Logic -----------------
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ API Key is missing. Add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

def extract_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        return text.strip()
    except Exception as e:
        return f"ERROR_EXTRACTION: {str(e)}"

def generate_summary(text, persona, goal):
    # Models to try
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    # Safety settings to prevent blocking
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    for model_name in model_names:
        try:
            instructions = f"You are a professional assistant helping a {persona}. Your goal is: {goal}"
            model = genai.GenerativeModel(model_name=model_name, system_instruction=instructions)
            
            # Use a slightly smaller chunk to be safe with tokens
            content_to_send = text[:20000] 
            
            response = model.generate_content(
                f"Summarize the following PDF text professionally:\n\n{content_to_send}",
                safety_settings=safety_settings
            )
            
            if response and response.text:
                return response.text
            else:
                continue
        except Exception as e:
            if model_name == model_names[-1]:
                return f"Final API Error: {str(e)}"
            continue
    return "Failed to generate summary with any model."

# ----------------- UI -----------------
st.markdown("<h1 style='text-align: center;'>🧠 MindMap AI V2</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 🛠️ Configuration")
        persona = st.selectbox("Persona", ["Student", "Professional", "Researcher", "General"])
        goal = st.text_area("Specific Goal", placeholder="e.g. Extract only the financial metrics...")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if st.button("Generate Summary", type="primary"):
            if uploaded_file:
                with st.spinner("Extracting and Summarizing..."):
                    # 1. Extract Text
                    text = extract_text(uploaded_file)
                    
                    if not text:
                        st.error("❌ Could not extract any text from this PDF. It might be an image scan or encrypted.")
                    elif text.startswith("ERROR_EXTRACTION"):
                        st.error(f"❌ PDF Error: {text}")
                    else:
                        st.info(f"✅ Extracted {len(text)} characters. Sending to Gemini...")
                        # 2. Generate Summary
                        summary = generate_summary(text, persona, goal)
                        st.session_state['summary'] = summary
            else:
                st.error("Please upload a PDF file first.")

with col2:
    with st.container(border=True):
        st.markdown("### 📝 Analysis Result")
        if 'summary' in st.session_state:
            st.markdown(st.session_state['summary'])
        else:
            st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; color: #94a3b8; border: 1px dashed #e2e8f0; border-radius: 10px;'>Your summary will appear here...</div>", unsafe_allow_html=True)
