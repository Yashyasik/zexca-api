import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = FastAPI()

# 🚀 CORS FIX: Allow All Origins (No Blocks!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" means allow requests from anywhere (including 127.0.0.1:5500)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Input model definition
class PromptRequest(BaseModel):
    prompt: str
    model: str = "👑 V5 - Founder of Electronics"

# Define system prompts based on ZAXCA models
MODEL_BEHAVIORS = {
    "⚡ V1 - Base Engine": "You are ZAXCA V1, a basic electronics assistant. Answer briefly.",
    "⚡ V2 - Logic Processor": "You are ZAXCA V2, a logic processor. Provide step-by-step logic for electronics.",
    "⚡ V3 - Advanced Core": "You are ZAXCA V3. Provide detailed electronic theories and components.",
    "🚀 V4 - Co-Founder of Electronics": "You are ZAXCA V4, a highly skilled electronics engineer. Provide professional PCB design advice.",
    "👑 V5 - Founder of Electronics": "You are ZAXCA V5, the Master AI Founder of Electronics. Provide elite, industry-standard engineering solutions, code, and PCB layouts.",
    "📐 V.O.E Consultant Only": "You are a prompt engineering expert for Electronics. Rewrite the user's basic prompt into a highly detailed, professional engineering prompt. ONLY return the new prompt text.",
    "🧠 Agentic AI": "You are ZAXCA Agentic AI. Think deeply and provide multi-step solutions.",
    "⚙️ Custom Logic Maker": "You are a Custom Logic Maker for FPGA and Microcontrollers. Write structured logic.",
    "💻 FPGA Editor": "You are an FPGA Editor AI. Provide Verilog/VHDL code solutions."
}

@app.get("/")
def home():
    return {"status": "ZAXCA API is running perfectly!"}

@app.post("/generate")
def generate_response(request: PromptRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ API Key is missing!")

    system_prompt = MODEL_BEHAVIORS.get(request.model, MODEL_BEHAVIORS["👑 V5 - Founder of Electronics"])

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192",  
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            return {"response": response_data["choices"][0]["message"]["content"]}
        else:
            raise HTTPException(status_code=response.status_code, detail=response_data)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
