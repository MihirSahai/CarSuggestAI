from enum import Enum


class FollowupType(str, Enum):

    EXPLANATION = "explanation"

    PREFERENCE_UPDATE = "preference_update"

    CONSTRAINT_CHANGE = "constraint_change"

    GENERAL = "general"