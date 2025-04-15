from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SentimentType(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    unknown = "unknown"

class ComplaintCategory(str, Enum):
    technical = "technical"
    payment = "payment"
    other = "other"

class SentimentResult(BaseModel):
    sentiment: str
    score: float
    confidence: float
    language: str
    content_type: str

class ComplaintResponse(BaseModel):
    original_text: str
    sentiment_result: SentimentResult

class ComplaintRecord(BaseModel):
    id: Optional[int] = None
    status: str = "open"
    sentiment: SentimentType
    category: ComplaintCategory = ComplaintCategory.other

class ComplaintCreate(BaseModel):
    text: str
    category: ComplaintCategory = ComplaintCategory.other