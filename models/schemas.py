from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class TonePreference(str, Enum):
    PLAYFUL = "playful"
    CONFIDENT = "confident"
    MYSTERIOUS = "mysterious"
    DIRECT = "direct"


class RiskLevel(str, Enum):
    SAFE = "safe"
    MEDIUM = "medium"
    BOLD = "bold"


class AnalyzeRequest(BaseModel):
    """Request model for conversation screenshot analysis"""
    image_base64: str = Field(..., description="Base64-encoded screenshot image")
    tone: TonePreference = Field(default=TonePreference.PLAYFUL, description="Desired reply tone")
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM, description="How bold the replies should be")
    platform: Optional[str] = Field(default=None, description="Platform: instagram, hinge, whatsapp, etc.")


class SuggestedReply(BaseModel):
    """A suggested reply with explanation"""
    text: str = Field(..., description="The suggested reply text")
    why_it_works: str = Field(..., description="Explanation of why this reply is effective")


class AnalyzeResponse(BaseModel):
    """Response model for conversation analysis"""
    interest_score: int = Field(..., ge=0, le=100, description="Interest level 0-100")
    interest_status: str = Field(..., description="Cold, Warming, or Engaged")
    situation_analysis: str = Field(..., description="What's happening in the conversation")
    why_last_didnt_work: Optional[str] = Field(None, description="Why the last message didn't work")
    diagnosis: str = Field(..., description="Primary label: Dry replies, Over-investing, etc.")
    suggested_replies: List[SuggestedReply] = Field(..., min_length=3, max_length=3)
    texting_principle: str = Field(..., description="General texting rule to learn")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
