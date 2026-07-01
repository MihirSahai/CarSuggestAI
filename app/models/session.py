from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from app.models.intent import Intent
from app.models.recommendation import Recommendation


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    message: str


class Session(BaseModel):
    session_id: str

    # Latest extracted user preferences
    intent: Optional[Intent] = None

    # Latest recommendation snapshot
    recommendations: List[Recommendation] = Field(default_factory=list)

    # Conversation history used for follow-up context
    conversation_history: List[ConversationTurn] = Field(default_factory=list)