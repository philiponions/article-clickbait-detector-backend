from enum import Enum
from datetime import date
from pydantic import BaseModel

class VerdictEnum(str, Enum):
    TRUE = "true"
    FALSE = "false"
    MIXED = "mixed"

class CommunityReport(BaseModel):
    url: str
    thumbnail: str
    website: str
    title: str    
    verdict: VerdictEnum
    meter: int
    summary: str
    explanation: str
