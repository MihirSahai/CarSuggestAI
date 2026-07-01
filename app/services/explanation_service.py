from typing import Dict, Any, List
from app.services.llm_service import BaseLLMService


class ExplanationService:

    def __init__(self, llm: BaseLLMService):
        self.llm = llm

    # -----------------------------
    # MAIN ENTRY
    # -----------------------------

    def generate_recommendation_explanation(
        self,
        intent: Dict[str, Any],
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        prompt = f"""
You are an expert car advisor.

Your job is to make the user CONFIDENT about the recommendations.

USER INTENT:
{intent}

TOP RECOMMENDATIONS:
{recommendations}

TASK:
1. Write a short overall explanation (why these cars were selected)
2. For EACH car, explain in 1-2 lines why it matches user needs
3. Highlight tradeoffs honestly (no marketing tone)
4. Be simple and reassuring

FORMAT:
Return JSON:
{{
  "overall_summary": "...",
  "cars": [
    {{
      "car": "...",
      "reason": "..."
    }}
  ]
}}
"""

        response = self.llm.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return self._safe_parse(response.text)

    # -----------------------------
    # SAFE PARSER
    # -----------------------------

    def _safe_parse(self, text: str):
        import json
        import re

        try:
            cleaned = re.sub(r"```json|```", "", text).strip()
            return json.loads(cleaned)
        except:
            return {
                "overall_summary": "Top recommendations based on your requirements.",
                "cars": []
            }