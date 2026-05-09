import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import fitz  # PyMuPDF
import asyncio
import time
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in .env file. Please add it.")
else:
    genai.configure(api_key=api_key)

async def cleanup_old_exports():
    """Background task to delete PDF files in exports/ older than 24 hours."""
    while True:
        try:
            exports_dir = "exports"
            if os.path.exists(exports_dir):
                current_time = time.time()
                for filename in os.listdir(exports_dir):
                    filepath = os.path.join(exports_dir, filename)
                    if os.path.isfile(filepath):
                        # Delete if older than 24 hours (86400 seconds)
                        if current_time - os.path.getmtime(filepath) > 86400:
                            os.remove(filepath)
                            print(f"Deleted old export: {filename}")
        except Exception as e:
            print(f"Cleanup error: {e}")
        # Sleep for 1 hour before checking again
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_old_exports())

@app.post("/summarize")
async def summarize_pdf(
    file: UploadFile = File(...),
    persona: str = Form(...),
    goal: str = Form("")
):
    try:
        # Extract text from PDF
        pdf_content = await file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
            
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")

        # Persona-Driven Prompting Logic
        # This section dynamically changes the system instruction based on the user's selected persona.
        # It ensures the LLM's output format, tone, and focus area are tailored to the specific needs of the user.
        if persona.lower() == "student":
            # The Student persona forces the LLM to act as a tutor, prioritizing clear definitions, 
            # essential concepts, and easily digestible study notes.
            system_instruction = "You are an AI assistant helping a student. Focus on definitions, key concepts, and study notes."
        elif persona.lower() == "professional":
            # The Professional persona instructs the LLM to generate an executive-style summary,
            # highlighting actionable items, critical metrics, and business impact.
            system_instruction = "You are an AI assistant helping a professional. Focus on action items, metrics, and executive summaries."
        elif persona.lower() == "researcher":
            # The Researcher persona shifts the focus to academic rigor, requiring the LLM to extract
            # underlying methodologies, core findings, and provide critical analysis of the text.
            system_instruction = "You are an AI assistant helping a researcher. Focus on methodology, findings, and critical analysis."
        else:
            system_instruction = "You are a helpful AI assistant."

        prompt = f"Goal: {goal if goal else 'Provide a comprehensive summary'}\n\nPlease summarize the following text according to the goal and your persona.\n\nText:\n{text[:15000]}"

        try:
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
            response = model.generate_content(prompt)
        except Exception as api_err:
            print(f"Gemini API Error: {api_err}")
            raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(api_err)}")
        
        # Check if the response was blocked by safety filters
        if not response.candidates or not response.candidates[0].content.parts:
            # Check the block reason if available
            block_reason = "Unknown reason"
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                block_reason = f"Safety Block: {response.prompt_feedback.block_reason}"
            elif response.candidates and response.candidates[0].finish_reason:
                block_reason = f"Finish Reason: {response.candidates[0].finish_reason}"
            
            raise HTTPException(status_code=400, detail=f"Gemini API could not generate a summary. Reason: {block_reason}")

        summary = response.text

        return JSONResponse(content={"summary": summary})

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid Gemini API Key. Please check your .env file.")
        elif "Safety" in error_msg or "blocked" in error_msg.lower():
            raise HTTPException(status_code=400, detail=f"Content blocked by Gemini safety filters: {error_msg}")
        
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=error_msg)

from pydantic import BaseModel
class PDFRequest(BaseModel):
    text: str

@app.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    try:
        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)
        filename = "exports/summary_output.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Split text by newlines and add to story
        for p in request.text.split('\n'):
            if p.strip():
                # Replace common markdown chars to prevent ReportLab errors
                clean_p = p.replace("**", "").replace("*", "").replace("#", "")
                story.append(Paragraph(clean_p, styles["Normal"]))
                story.append(Spacer(1, 12))
                
        doc.build(story)
        return FileResponse(filename, media_type='application/pdf', filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)