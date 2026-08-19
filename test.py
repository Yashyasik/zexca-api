=-0-op[iop[]\import requests

# உங்க Railway லிங்க் (கடைசில /generate இருக்கு)
URL = "https://zexca-api-production.up.railway.app/generate" 

# AI-கிட்ட நம்ம கேட்குற கேள்வி
payload = {
    "prompt": "Hello AI, you are the brain of ZAXCA AI. Say a short, energetic welcome message!"
}

print("AI-கிட்ட இருந்து பதில் வருது... வெயிட் பண்ணுங்க ⏳\n")

# சர்வருக்கு டேட்டாவை அனுப்புறோம்
response = requests.post(URL, json=payload)

# ரிசல்ட்டை பிரிண்ட் பண்றோம்
if response.status_code == 200:
    print("🤖 ZAXCA AI Badhil:\n", response.json().get("response"))
else:
    print("❌ Error vandhurukku:", response.text)