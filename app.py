from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

class CalculationRequest(BaseModel):
    amount: float
    rate: float

class CalculationResponse(BaseModel):
    monthly: float

class HealthResponse(BaseModel):
    status: str
    timestamp: str

@app.post("/calculate")
def calculate(request: CalculationRequest) -> CalculationResponse:
    """Calculate monthly payment amount"""
    monthly = (request.amount * request.rate) / 12
    return CalculationResponse(monthly=monthly)

@app.get("/health")
def health() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
