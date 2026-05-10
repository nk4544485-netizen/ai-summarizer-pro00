import os
import asyncio
import time

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
                        if current_time - os.path.getmtime(filepath) > 86400:
                            os.remove(filepath)
                            print(f"Deleted old export: {filename}")
        except Exception as e:
            print(f"Cleanup error: {e}")
        await asyncio.sleep(3600)


@app.on_event("startup")
async def startup_event():
    # API Listing: Show all models available to this key
    print("\n" + "="*50)
    print("Listing available Gemini models for your API key:")
    print("="*50)
    if api_key:
        try:
            [print(m.name) for m in genai.list_models()]
        except Exception as e:
            print(f"Error listing models: {e}")
    else:
        print("No API key configured — skipping model list.")
    print("="*50 + "\n")

    asyncio.create_task(cleanup_old_exports())


@app.post("/summarize")
async def summarize_pdf(
    file: UploadFile = File(...),
    persona: str = Form(...),
    goal: str = Form("")
):
    if not api_key:
        raise HTTPException(status_code=500, detail="Server is not configured with a Gemini API key.")

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
        if persona.lower() == "student":
            system_instruction = "You are an AI assistant helping a student. Focus on definitions, key concepts, and study notes."
        elif persona.lower() == "professional":
            system_instruction = "You are an AI assistant helping a professional. Focus on action items, metrics, and executive summaries."
        elif persona.lower() == "researcher":
            system_instruction = "You are an AI assistant helping a researcher. Focus on methodology, findings, and critical analysis."
        else:
            system_instruction = "You are a helpful AI assistant."

        prompt = f"Goal: {goal if goal else 'Provide a comprehensive summary'}\n\nPlease summarize the following text according to the goal and your persona.\n\nText:\n{text[:15000]}"

        try:
            model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=system_instruction)
            response = model.generate_content(prompt)
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

        # Check if the response was blocked by safety filters
        if not response.candidates or not response.candidates[0].content.parts:
            block_reason = "Unknown reason"
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = f"Safety Block: {response.prompt_feedback.block_reason}"
            elif response.candidates and response.candidates[0].finish_reason:
                block_reason = f"Finish Reason: {response.candidates[0].finish_reason}"
            raise HTTPException(status_code=400, detail=f"Gemini could not generate a summary. Reason: {block_reason}")

        summary = response.text
        return JSONResponse(content={"summary": summary})

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG ERROR: {error_msg}")
        if "API_KEY_INVALID" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid Gemini API Key. Please check your .env file.")
        elif "Safety" in error_msg or "blocked" in error_msg.lower():
            raise HTTPException(status_code=400, detail=f"Content blocked by Gemini safety filters: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


class PDFRequest(BaseModel):
    text: str

@app.get("/models")
async def get_models():
    if not api_key:
        raise HTTPException(status_code=500, detail="Server is not configured with a Gemini API key.")
    try:
        models = [m.name.replace('models/', '') for m in genai.list_models()]
        return JSONResponse(content={"models": models})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    try:
        os.makedirs("exports", exist_ok=True)
        filename = "exports/summary_output.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        for p in request.text.split('\n'):
            if p.strip():
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