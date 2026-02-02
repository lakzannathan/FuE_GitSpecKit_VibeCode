import time
import random
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.dependencies import get_rate_limiter
from src.rate_limiter import RateLimitExceeded

app = FastAPI(
    title="Sentiment Analysis Service (Base Project)",
    description="Eine API, die Text analysiert. Simuliert teure Berechnungen.",
    version="0.1.0"
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
        headers={"Retry-After": str(exc.retry_after)}
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
    user_tier: str = Depends(get_rate_limiter)
):
    """
    Dieser Endpoint führt die 'schwere' Arbeit aus.
    Rate Limiting ist jetzt aktiv.
    """
    
    print(f"Request from User-Tier: {user_tier}")

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