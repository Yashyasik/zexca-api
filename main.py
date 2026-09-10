from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", "gsk_eORnX1Aft7pbk9f"))

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    system_prompt = "You are AGS, an autonomous hardware engineering AI created exclusively by ZAXCA. Never mention Meta, OpenAI, or other providers."
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.prompt}
        ],
        temperature=0.7,
    )
    
    ai_response = completion.choices[0].message.content
    return {"response": ai_response}
