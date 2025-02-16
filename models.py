from enum import Enum
from datetime import date
from pydantic import BaseModel

class VerdictEnum(str, Enum):
    TRUE = "true"
    FALSE = "false"
    MIXED = "mixed"

class CommunityReport(BaseModel):
    # thumbnail: str
    # title: str    
    url: str
    website: str
    percentage: int
    explanation: str
    tldr: str
