from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import re

app = FastAPI(title="Agentic Scam Honeypot API")

SCAM_KEYWORDS = [
    "win", "winner", "won", "urgent", "click",
    "otp", "kyc", "lottery", "refund", "prize"
]

@app.get("/")
def root():
    return {
        "service": "Agentic Scam Honeypot API",
        "status": "running"
    }

@app.post("/analyze")
async def analyze_message(request: Request):
    try:
        body = await request.json()
        message = body.get("message", "")
    except:
        message = ""

    message = message.strip().lower()

    # If no message provided, still respond (tester case)
    if not message:
        message = "test message"

    # Scam detection
    keyword_hits = sum(1 for word in SCAM_KEYWORDS if word in message)
    confidence_score = min(keyword_hits / 5, 1.0)
    is_scam = confidence_score >= 0.3

    # Extraction
    links = re.findall(r"https?://\S+", message)
    upi_ids = re.findall(r"\b[\w.-]+@(upi|paytm|phonepe|ybl)\b", message)
    bank_accounts = re.findall(r"\b\d{9,18}\b", message)

    return {
        "is_scam": is_scam,
        "confidence_score": round(confidence_score, 2),
        "persona_used": "Non-technical UPI user",
        "extracted_intelligence": {
            "links": links,
            "upi_ids": upi_ids,
            "bank_accounts": bank_accounts
        }
    }
