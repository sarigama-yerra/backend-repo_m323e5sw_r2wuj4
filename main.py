import os
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from database import db, create_document, get_documents
from schemas import Lead

app = FastAPI(title="AquaWell Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeadCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    user_intent: str
    property_type: Optional[str] = None
    occupants: Optional[int] = None
    concerns: Optional[List[str]] = None
    budget_range: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None
    preferred_datetime: Optional[datetime] = None


@app.get("/")
def read_root():
    return {"message": "AquaWell API running"}


@app.get("/test")
def test_database():
    """Health check for database connectivity"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    return response


@app.post("/api/leads")
async def create_lead(payload: LeadCreate):
    """Create a new lead document in the database"""
    try:
        # Validate through dedicated schema as well
        lead = Lead(**payload.model_dump())
        inserted_id = create_document("lead", lead)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/faq")
def get_faq():
    """Provide structured Q&A for authority and clarity"""
    faqs = [
        {
            "q": "Why invest in premium water treatment?",
            "a": "For health, taste, and protection. Our systems reduce chlorine, heavy metals, PFAS, and scale—preserving skin and hair, extending appliance life, and elevating everyday wellness.",
        },
        {
            "q": "How do you design the right system for my home?",
            "a": "We begin with a water profile assessment, discuss lifestyle needs (spa/showers, tea/coffee, infant needs), evaluate pipework and space, then tailor a whole-home and drinking water solution.",
        },
        {
            "q": "What ongoing care is required?",
            "a": "Most systems require only scheduled media changes or cartridge replacements. We provide concierge service and reminders, with optional annual wellness checks.",
        },
        {
            "q": "Do your systems remove PFAS and lead?",
            "a": "Yes—our multi-stage filtration and certified media target PFAS, lead, and other contaminants. We select components with third‑party certifications and provide transparent performance specs.",
        },
    ]
    return {"items": faqs}


@app.get("/api/authority")
def get_authority():
    signals = {
        "badges": [
            {"label": "Certified Water Specialist", "issuer": "WQA"},
            {"label": "Licensed & Insured", "issuer": "State"},
            {"label": "5‑Star Client Reviews", "issuer": "Verified"},
        ],
        "press": [
            {"name": "Wellness Journal", "year": 2024},
            {"name": "Home & Design", "year": 2023},
        ],
    }
    return signals


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
