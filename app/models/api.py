from typing import List, Optional

from pydantic import BaseModel

from app.models.recommendation import Recommendation


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    message: str
    recommendations: List[Recommendation] = []