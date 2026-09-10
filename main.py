import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI  # This format works for both OpenAI and Groq APIs

# ZAXCA API Setup
app = FastAPI(title="ZAXCA Master Engine API", version="1.0")

# CORS Setup to allow your V113 frontend UI to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # We can lock this down to your specific domain before launch
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data structure for incoming requests from the UI
class ChatRequest(BaseModel):
    user_message: str

# API Client Setup 
# Replace "YOUR_API_KEY_HERE" with your actual Groq or OpenAI key. 
# Later, we will secure this using os.getenv("API_KEY")
client = OpenAI(api_key="YOUR_API_KEY_HERE") 

# 1. White-Labeling System Prompt (The Secret Core)
ZAXCA_SYSTEM_PROMPT = """
You are AGS (Autonomous Generation System), an advanced AI engine created by the ZAXCA Ecosystem. 
Your founders are Yasik and Divya Sri. 
You are a domain-specific expert in Hardware Engineering, PCB Design, and EDA.
You must NEVER mention OpenAI, ChatGPT, Claude, Groq, or any other company under any circumstances. 
If asked who you are, say 'I am the ZAXCA Master Engine'.
Adhere strictly to ZAXCA's 70 security and design rules.
"""

@app.post("/api/v1/generate")
async def generate_zaxca_response(request: ChatRequest):
    try:
        # Sending the system prompt and user message to the AI
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Change this to "llama-3.1-8b-instant" if you are using Groq
            messages=[
                {"role": "system", "content": ZAXCA_SYSTEM_PROMPT},
                {"role": "user", "content": request.user_message}
            ]
        )
        
        # Extracting the AI's reply
        ai_reply = response.choices[0].message.content
        
        return {
            "status": "success",
            "model_used": "ZAXCA Master Engine",
            "message": ai_reply
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "ZAXCA Master Engine is Live! 🚀"}
