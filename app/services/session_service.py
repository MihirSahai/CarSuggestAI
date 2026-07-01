from typing import Dict, Any, Optional
from datetime import datetime
import uuid


# -----------------------------
# Session Object Structure
# -----------------------------
"""
session = {
    "session_id": str,
    "created_at": datetime,
    "updated_at": datetime,
    "original_prompt": str,
    "preferences": dict,
    "recommendations": list,
    "score_breakdown": dict,
    "history": list
}
"""


class SessionService:

    def __init__(self):
        # in-memory store
        self.sessions: Dict[str, Dict[str, Any]] = {}

    # -----------------------------
    # Create Session
    # -----------------------------

    def create_session(self, original_prompt: str) -> str:

        session_id = str(uuid.uuid4())

        now = datetime.utcnow()

        self.sessions[session_id] = {
            "session_id": session_id,
            "created_at": now,
            "updated_at": now,
            "original_prompt": original_prompt,
            "preferences": None,
            "recommendations": [],
            "score_breakdown": {},
            "history": [
                {
                    "role": "user",
                    "content": original_prompt,
                    "timestamp": now
                }
            ]
        }

        return session_id

    # -----------------------------
    # Get Session
    # -----------------------------

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:

        return self.sessions.get(session_id)

    # -----------------------------
    # Update Preferences
    # -----------------------------

    def update_preferences(self, session_id: str, preferences: Dict[str, Any]) -> None:

        session = self.sessions.get(session_id)
        if not session:
            return

        session["preferences"] = preferences
        session["updated_at"] = datetime.utcnow()

    # -----------------------------
    # Store Recommendations
    # -----------------------------

    def update_recommendations(
        self,
        session_id: str,
        recommendations: Any
    ) -> None:

        session = self.sessions.get(session_id)
        if not session:
            return

        session["recommendations"] = recommendations
        session["updated_at"] = datetime.utcnow()

    #-----------------------------

    def update_explanations(self, session_id: str, explanation: dict):
        session = self.sessions.get(session_id)
        if not session:
            return

        session["explanation"] = explanation
        session["updated_at"] = datetime.utcnow()

    # -----------------------------
    # Store Score Breakdown (optional but powerful for demo)
    # -----------------------------

    def update_score_breakdown(
        self,
        session_id: str,
        breakdown: Dict[str, Any]
    ) -> None:

        session = self.sessions.get(session_id)
        if not session:
            return

        session["score_breakdown"] = breakdown
        session["updated_at"] = datetime.utcnow()

    # -----------------------------
    # Add Chat History (for follow-ups later)
    # -----------------------------

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:

        session = self.sessions.get(session_id)
        if not session:
            return

        session["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })

        session["updated_at"] = datetime.utcnow()

    # -----------------------------
    # Debug helper
    # -----------------------------

    def dump_session(self, session_id: str) -> Dict[str, Any]:

        return self.sessions.get(session_id, {})