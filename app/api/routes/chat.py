from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json

from app.services.llm_service import get_llm_service
from app.services.session_service import SessionService
from app.services.recommendation_engine import recommend_cars
from app.services.explanation_service import ExplanationService


router = APIRouter()

llm = get_llm_service("gemini")

session_service = SessionService()
explanation_service = ExplanationService(llm)

with open("app/data/cars.json", "r") as f:
    CARS_DATA = json.load(f)


# -----------------------------
# REQUEST MODEL
# -----------------------------

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str


# -----------------------------
# COMPLETENESS CHECK
# -----------------------------

def is_complete(intent: Dict[str, Any]) -> bool:
    return intent.get("budget") is not None and intent.get("priorities")


# -----------------------------
# MAIN ENDPOINT
# -----------------------------

@router.post("/chat")
def chat(request: ChatRequest):

    message = request.message
    session_id = request.session_id

    # -----------------------------
    # 1. SESSION INIT
    # -----------------------------
    if not session_id:
        session_id = session_service.create_session(message)

    session = session_service.get_session(session_id)

    session_service.add_message(session_id, "user", message)

    # -----------------------------
    # 2. LLM INTENT EXTRACTION
    # -----------------------------
    intent = llm.extract_preferences(message)
    session_service.update_preferences(session_id, intent)

    # -----------------------------
    # 3. CLARIFICATION FLOW
    # -----------------------------
    if not is_complete(intent):

        clarification = llm.generate_clarification(intent)

        session_service.add_message(session_id, "assistant", clarification)

        return {
            "session_id": session_id,
            "type": "CLARIFICATION",
            "data": {
                "question": clarification,
                "missing_fields": intent.get("missing_fields", [])
            }
        }

    # -----------------------------
    # 4. RECOMMENDATION ENGINE
    # -----------------------------
    recommendations = recommend_cars(
        cars=CARS_DATA,
        intent=intent,
        top_k=5
    )

    session_service.update_recommendations(session_id, recommendations)

    # -----------------------------
    # 5. EXPLANATION LAYER (NEW)
    # -----------------------------
    explanation = explanation_service.generate_recommendation_explanation(
        intent=intent,
        recommendations=recommendations
    )

    session_service.update_explanations(session_id, explanation)

    # -----------------------------
    # 6. RESPONSE
    # -----------------------------
    return {
        "session_id": session_id,
        "type": "RECOMMENDATION",
        "data": {
            "recommendations": recommendations,
            "explanation": explanation
        }
    }