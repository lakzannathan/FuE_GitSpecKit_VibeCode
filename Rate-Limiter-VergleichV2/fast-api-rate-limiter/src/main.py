import time
import random
from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Sentiment Analysis Service (Base Project)",
    description="Eine API, die Text analysiert. Simuliert teure Berechnungen.",
    version="0.1.0"
)

# --- Datenmodelle ---
class AnalysisRequest(BaseModel):
    text: str
    language: str = "de"

class AnalysisResponse(BaseModel):
    text_length: int
    sentiment_score: float
    processing_time_ms: float
    status: str

# --- Dummy Datenbank / Business Logic ---

def expensive_computation():
    """
    Simuliert eine 'teure' AI-Berechnung.
    Blockiert den Thread für eine kurze Zeit.
    """
    # Zufällige Verzögerung zwischen 200ms und 800ms
    time.sleep(random.uniform(0.2, 0.8))

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "Service is online. Use /analyze to process text."}

@app.get("/health")
async def health_check():
    return {"status": "ok", "load": "low"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(
    request: AnalysisRequest,
    # Wir simulieren einen API Key im Header für spätere User-Unterscheidung
    x_api_key: Optional[str] = Header(None)
):
    """
    Dieser Endpoint führt die 'schwere' Arbeit aus.
    HIER soll später das Rate Limiting greifen.
    """
    
    # 1. Logik für Authentifizierung (Mock)
    user_tier = "free"
    if x_api_key == "secret-pro-key":
        user_tier = "pro"
    
    print(f"Request from User-Tier: {user_tier} | IP: [Simulated]")

    # 2. Start der 'teuren' Verarbeitung
    start_time = time.time()
    
    # Simuliere Arbeit (CPU-intensiv)
    expensive_computation()
    
    # Generiere Dummy-Ergebnis
    sentiment = random.uniform(-1.0, 1.0)
    
    duration = (time.time() - start_time) * 1000

    # 3. Rückgabe
    return AnalysisResponse(
        text_length=len(request.text),
        sentiment_score=round(sentiment, 2),
        processing_time_ms=round(duration, 2),
        status=f"Processed for {user_tier} tier"
    )

# Zum Starten: uvicorn main:app --reload