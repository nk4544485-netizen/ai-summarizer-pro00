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

# ----------------- Configuration -----------------
st.set_page_config(page_title="MindMap AI V2", page_icon="🧠", layout="centered")

st.title("🧠 MindMap AI V2 - PDF Summarizer")
st.markdown("Summarize Any PDF Instantly into a Structured Document")

# Setup API Key securely
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ GEMINI_API_KEY is not set. Please configure it in your Streamlit secrets or .env file.")
    st.stop()
else:
    genai.configure(api_key=api_key)

# ----------------- Functions -----------------
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_summary(text, persona, goal):
    if persona == "Student":
        system_instruction = "You are an AI assistant helping a student. Focus on definitions, key concepts, and study notes."
    elif persona == "Professional":
        system_instruction = "You are an AI assistant helping a professional. Focus on action items, metrics, and executive summaries."
    elif persona == "Researcher":
        system_instruction = "You are an AI assistant helping a researcher. Focus on methodology, findings, and critical analysis."
    else:
        system_instruction = "You are a helpful AI assistant."

    prompt = f"Goal: {goal if goal else 'Provide a comprehensive summary'}\n\nPlease summarize the following text according to the goal and your persona.\n\nText:\n{text[:15000]}"
    
    model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=system_instruction)
    response = model.generate_content(prompt)
    
    if not response.candidates or not response.candidates[0].content.parts:
        st.error("Summary blocked by safety filters or failed to generate.")
        st.stop()
    
    return response.text

def create_pdf(text):
    temp_dir = tempfile.mkdtemp()
    filepath = os.path.join(temp_dir, "summary_output.pdf")
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for p in text.split('\n'):
        if p.strip():
            clean_p = p.replace("**", "").replace("*", "").replace("#", "")
            story.append(Paragraph(clean_p, styles["Normal"]))
            story.append(Spacer(1, 12))

    doc.build(story)
    return filepath

# ----------------- UI -----------------
with st.sidebar:
    st.header("Settings")
    persona = st.selectbox("Select Persona", ["Student", "Professional", "Researcher", "General"])
    goal = st.text_input("Specific Goal (Optional)", placeholder="e.g. Extract main arguments...")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    if st.button("✨ Summarize PDF", type="primary"):
        with st.spinner("Processing Document..."):
            try:
                # 1. Extract Text
                text = extract_text_from_pdf(uploaded_file)
                if not text.strip():
                    st.error("Could not extract text. The PDF might be an image scan or encrypted.")
                    st.stop()
                
                # 2. Generate Summary
                summary = generate_summary(text, persona, goal)
                
                # 3. Display Result
                st.subheader("Summary Result")
                st.markdown(summary)
                
                # 4. Export PDF
                pdf_path = create_pdf(summary)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Summary as PDF",
                        data=f,
                        file_name="AI_Summary.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error: {str(e)}")
