from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI(title="Agentic Scam Honeypot API")

# -----------------------------
# Request Model
# -----------------------------
class MessageRequest(BaseModel):
    message: str

# -----------------------------
# Scam Keywords
# -----------------------------
SCAM_KEYWORDS = [
    "win", "winner", "won", "urgent", "click",
    "otp", "kyc", "lottery", "refund", "prize"
]

# -----------------------------
# Root Health Check (FIXES /)
# -----------------------------
@app.get("/")
def root():
    return {
        "service": "Agentic Scam Honeypot API",
        "status": "running"
    }

# -----------------------------
# Analyze Endpoint
# -----------------------------
@app.post("/analyze")
def analyze_message(payload: MessageRequest):
    message = payload.message.strip().lower()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

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
