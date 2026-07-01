from typing import List, Optional

from pydantic import BaseModel, Field


class Constraints(BaseModel):
    budget_max: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    body_types: List[str] = []
    seating_min: Optional[int] = None


class UsageProfile(BaseModel):
    city: float = 0.5
    highway: float = 0.5


class Intent(BaseModel):
    constraints: Constraints
    usage: UsageProfile

    priorities: List[str] = Field(default_factory=list)

    missing_fields: List[str] = Field(default_factory=list)

    clarification_question: Optional[str] = None