from typing import Dict, Any, List, Literal
from enum import Enum

from services.llm_service import BaseLLMService


# -----------------------------
# Follow-up Categories
# -----------------------------

class FollowUpType(str, Enum):
    WHY_NOT = "WHY_NOT"
    COMPARE = "COMPARE"
    FILTER = "FILTER"
    EXPLAIN = "EXPLAIN"
    GENERAL = "GENERAL"


# -----------------------------
# Follow-up Service
# -----------------------------

class FollowUpService:

    def __init__(self, llm: BaseLLMService):
        self.llm = llm

    # -----------------------------
    # 1. CLASSIFIER
    # -----------------------------

    def classify(self, question: str, context: Dict[str, Any]) -> FollowUpType:

        prompt = f"""
Classify this follow-up question into one of:

- WHY_NOT (why a car was not recommended)
- COMPARE (compare two cars)
- FILTER (change constraints like budget, mileage, fuel)
- EXPLAIN (explain why a recommended car was chosen)
- GENERAL (anything else)

Return ONLY one label.

Question:
{question}

Context:
{context}
"""

        response = self.llm.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip().upper()

        # safe mapping fallback
        for t in FollowUpType:
            if t.value in text:
                return t

        return FollowUpType.GENERAL

    # -----------------------------
    # 2. ROUTER
    # -----------------------------

    def route(self, followup_type: FollowUpType):
        routes = {
            FollowUpType.WHY_NOT: self.handle_why_not,
            FollowUpType.COMPARE: self.handle_compare,
            FollowUpType.FILTER: self.handle_filter,
            FollowUpType.EXPLAIN: self.handle_explain,
            FollowUpType.GENERAL: self.handle_general,
        }

        return routes.get(followup_type, self.handle_general)

    # -----------------------------
    # 3. HANDLERS (deterministic logic only)
    # -----------------------------

    def handle_why_not(self, question: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine why a car is NOT in top results.
        """

        recommendations = session.get("recommendations", [])

        return {
            "type": "WHY_NOT",
            "data": recommendations
        }

    def handle_compare(self, question: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract two cars and compare deterministically later.
        """

        recommendations = session.get("recommendations", [])

        return {
            "type": "COMPARE",
            "data": recommendations
        }

    def handle_filter(self, question: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        This will trigger re-run of recommendation engine later.
        """

        preferences = session.get("preferences", {})

        return {
            "type": "FILTER",
            "data": preferences
        }

    def handle_explain(self, question: str, session: Dict[str, Any]) -> Dict[str, Any]:

        recommendations = session.get("recommendations", [])

        return {
            "type": "EXPLAIN",
            "data": recommendations
        }

    def handle_general(self, question: str, session: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "type": "GENERAL",
            "data": session
        }

    # -----------------------------
    # 4. FINAL RESPONSE GENERATION (LLM ONLY HERE)
    # -----------------------------

    def generate_response(
        self,
        followup_type: FollowUpType,
        handler_output: Dict[str, Any],
        question: str
    ) -> str:

        prompt = f"""
You are a helpful car recommendation assistant.

Follow-up type:
{followup_type}

User question:
{question}

Handler output (structured data):
{handler_output}

Rules:
- Use ONLY the provided data
- Be concise
- No hallucination
"""

        response = self.llm.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()