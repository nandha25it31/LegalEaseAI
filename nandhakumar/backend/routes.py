from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


generator = GeminiDocumentGenerator()


@router.get("/api/status")
def api_status():
    return {
        "status": "online",
        "message": "LegalEase API is working"
    }


@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        generated_document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )

        return {
            "success": True,
            "document": generated_document
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(e)}"
        )