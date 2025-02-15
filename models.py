from enum import Enum
from datetime import date
from pydantic import BaseModel

class VerdictEnum(str, Enum):
    TRUE = "true"
    FALSE = "false"
    MIXED = "mixed"

class CommunityReport(BaseModel):
    url: str
    title: str
    date_posted: date = date.today()
    verdict: VerdictEnum
    meter: int
    summary: str
    explanation: str
