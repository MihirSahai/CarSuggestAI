from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.services.llm_service import get_llm_service

router = APIRouter()

llm = get_llm_service("gemini")


# -----------------------------
# Request Schemas
# -----------------------------

class ExtractRequest(BaseModel):
    text: str


class ExplanationRequest(BaseModel):
    intent: Dict[str, Any]
    car: Dict[str, Any]


class ClarificationRequest(BaseModel):
    intent: Dict[str, Any]


# -----------------------------
# 1. Test Intent Extraction
# -----------------------------

@router.post("/llm/extract")
def test_extract(req: ExtractRequest):

    result = llm.extract_preferences(req.text)

    return {
        "input": req.text,
        "extracted_intent": result
    }


# -----------------------------
# 2. Test Explanation
# -----------------------------

@router.post("/llm/explain")
def test_explanation(req: ExplanationRequest):

    result = llm.generate_explanation(
        car=req.car,
        intent=req.intent
    )

    return {
        "explanation": result
    }


# -----------------------------
# 3. Test Clarification
# -----------------------------

@router.post("/llm/clarify")
def test_clarification(req: ClarificationRequest):

    result = llm.generate_clarification(req.intent)

    return {
        "question": result
    }