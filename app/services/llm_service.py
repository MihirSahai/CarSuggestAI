from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from google import genai
from google.genai import types
import os
import json
import re


# -----------------------------
# Abstract Interface (for swapability)
# -----------------------------

class BaseLLMService(ABC):

    @abstractmethod
    def extract_preferences(self, user_input: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_explanation(self, car: Dict[str, Any], intent: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def generate_clarification(self, intent: Dict[str, Any]) -> str:
        pass


# -----------------------------
# Gemini Implementation
# -----------------------------

class GeminiLLMService(BaseLLMService):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    # -------------------------
    # 1. Intent Extraction
    # -------------------------

    def extract_preferences(self, user_input: str) -> Dict[str, Any]:

        prompt = f"""
Extract structured JSON from this car requirement:

{{
  "budget": number or null,
  "fuel_type": string or null,
  "seating": number or null,
  "priorities": list of strings,
  "use_case": string or null,
  "missing_fields": list of strings
}}

Rules:
- priorities must be: safety, mileage, comfort, performance, features, reliability
- output ONLY valid JSON

User:
{user_input}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )

        return self._safe_parse_json(response.text)

    # -------------------------
    # 2. Explanation Generator
    # -------------------------

    def generate_explanation(self, car: Dict[str, Any], intent: Dict[str, Any]) -> str:

        prompt = f"""
You are a car expert.

Explain why this car is recommended.

Intent:
{intent}

Car:
{car}

Rules:
- 3-5 lines
- simple language
- no marketing tone
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4
            )
        )

        return response.text.strip()
    # -------------------------
    # 3. Clarification Generator
    # -------------------------

    def generate_clarification(self, intent: Dict[str, Any]) -> str:

        prompt = f"""
User intent is incomplete:
{intent}

Ask ONE short follow-up question to clarify car preference.
Only return the question.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            )
        )

        return response.text.strip()

    # -------------------------
    # Utility
    # -------------------------

    def _safe_parse_json(self, text: str) -> Dict[str, Any]:
        """
        Gemini sometimes wraps JSON in markdown or text.
        This cleans it safely.
        """

        import json
        import re

        try:
            # remove markdown code blocks if present
            cleaned = re.sub(r"```json|```", "", text).strip()
            return json.loads(cleaned)
        except Exception:
            # fallback safe structure
            return {
                "budget": None,
                "fuel_type": None,
                "seating": None,
                "priorities": [],
                "use_case": None,
                "missing_fields": []
            }


# -----------------------------
# Factory (future-proofing)
# -----------------------------

def get_llm_service(provider: str = "gemini") -> BaseLLMService:

    if provider == "gemini":
        return GeminiLLMService()

    raise ValueError(f"Unsupported LLM provider: {provider}")