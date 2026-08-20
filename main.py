import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

# ZAXCA Server Setup
app = FastAPI(title="ZAXCA AI Engine", version="2.0")

# CORS Settings - இதுதான் அந்த "Unknown Server Error" வராம தடுக்கும் Security Pass!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontend websites
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend-ல் இருந்து வரும் டேட்டாவுக்கான மாடல்
class ChatRequest(BaseModel):
    prompt: str
    model: str

# சர்வர் ஒர்க் ஆகுதான்னு செக் பண்றதுக்கான டெஸ்ட் லிங்க்
@app.get("/")
def read_root():
    return {"status": "ZAXCA Engine is Active & Running! 🚀"}

# மெயின் AI Chat லாஜிக்
@app.post("/generate")
async def generate_response(request: ChatRequest):
    # Railway-ல் நாம் செட் செய்த Groq API Key-ஐ எடுக்கிறோம்
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return {"error": "Server Error: API Key missing in Railway."}
    
    try:
        # Groq Client Setup
        client = Groq(api_key=api_key)
        
        # ZAXCA-க்கான சிஸ்டம் பிராம்ப்ட் (இதுதான் அதை PCB/Electronics எக்ஸ்பெர்ட்டாக மாற்றுவது)
        system_prompt = """You are ZAXCA, an elite AI Co-Founder and PCB/Electronics Engineering expert. 
        You help with PCB design, routing, electronics, and coding. 
        Be professional, highly intelligent, and conversational."""

        # Groq-ஐ கூப்பிட்டு பதில் கேட்கிறோம் (Super fast LLaMA3 70B model)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.prompt}
            ],
            model="llama3-70b-8192", 
        )
        
        # AI-ன் பதிலை frontend-க்கு அனுப்புகிறோம்
        ai_reply = chat_completion.choices[0].message.content
        return {"response": ai_reply}
        
    except Exception as e:
        return {"error": str(e)}