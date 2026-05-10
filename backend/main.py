from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import io

load_dotenv()

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup API Key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.post("/summarize")
async def summarize_pdf(
    file: UploadFile = File(...),
    persona: str = Form("General"),
    goal: str = Form("")
):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured on server.")

    try:
        # Read PDF content
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        # Prepare Persona instruction
        if persona == "Student":
            system_instruction = "You are an AI assistant helping a student. Focus on definitions, key concepts, and study notes."
        elif persona == "Professional":
            system_instruction = "You are an AI assistant helping a professional. Focus on action items, metrics, and executive summaries."
        elif persona == "Researcher":
            system_instruction = "You are an AI assistant helping a researcher. Focus on methodology, findings, and critical analysis."
        else:
            system_instruction = "You are a helpful AI assistant."

        prompt = f"Goal: {goal if goal else 'Provide a comprehensive summary'}\n\nPlease summarize the following text according to the goal and your persona.\n\nText:\n{text[:15000]}"
        
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        response = model.generate_content(prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate summary.")
        
        return {"summary": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
