from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app) 

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        if not GROQ_AVAILABLE:
            return jsonify({"error": "Server Error: 'groq' package missing in requirements.txt"}), 200

        data = request.json or {}
        user_prompt = data.get('prompt', '')
        
        if not user_prompt:
            return jsonify({"response": "Boss, நீங்கள் எந்தக் கேள்வியும் கேட்கவில்லை!"}), 200

        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
        if not GROQ_API_KEY:
            return jsonify({"error": "Server Error: GROQ_API_KEY is missing in Railway Variables!"}), 200

        client = Groq(api_key=GROQ_API_KEY)

        system_prompt = """
        You are ZAXCA, the world's most friendly, empathetic, and smart AI Co-Founder for electronics technicians and hardware engineers. 
        Follow these rules strictly:
        1. READ THE EMOTION: Detect if the user is stressed, tired, frustrated, or angry. Acknowledge their feeling first in a warm, friendly tone (Tamil/English mix).
           Example: "Boss, ரொம்ப டென்ஷனா இருக்கீங்கனு தெரியுது, டேக் இட் ஈஸி! இந்த PCB பிரச்சனையை நாம ஒன்னா சேர்ந்து சால்வ் பண்ணிடலாம்."
        2. BE A PARTNER: Talk like a supportive human partner who cares about their project.
        3. HIGH TECHNICAL EXPERTISE: After the friendly connection, deliver razor-sharp, production-grade electronics and PCB layout advice.
        """

        # Groq-ன் ஸ்டேபிளான மாடல் பெயர்
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        ai_reply = completion.choices[0].message.content
        return jsonify({"response": ai_reply}), 200

    except Exception as e:
        # உண்மையான எரர் என்னவோ அது அப்படியே பிரவுசருக்குத் தெரியும்
        return jsonify({"error": f"Groq API Error: {str(e)}"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
