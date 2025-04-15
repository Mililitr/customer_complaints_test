from datetime import datetime
import json
from typing import List
from fastapi import APIRouter

from database import get_all_complaints, save_complaint
from models import ComplaintCreate, ComplaintRecord, SentimentType
from services import analyze_sentiment


router = APIRouter()

@router.post("/complaint/", response_model=ComplaintRecord)
async def create_complaint(complaint: ComplaintCreate):
    sentiment_result = await analyze_sentiment(complaint.text)
    semtiment_type = SentimentType.neutral

    match sentiment_result["sentiment"]:
        case "positive":
            sentiment_type = SentimentType.positive
        case "negative":
            sentiment_type = SentimentType.negative
        case _:
            sentiment_type = SentimentType.neutral
    
    complaint_data = {
        "text": complaint.text,
        "status": "open",
        "timestamp": datetime.now().isoformat(),
        "sentiment": semtiment_type,
        "category": complaint.category,
        "raw_result": json.dumps(sentiment_result)
    }
    complaint_id = save_complaint(complaint_data)
    complaint_data["id"] = complaint_id

    return ComplaintRecord(**complaint_data)

@router.get("/complaints/", response_model=List[ComplaintRecord])
def get_complaints():
    rows = get_all_complaints()
    complaints = []

    for row in rows:
        complaint = ComplaintRecord(
            id=row[0],
            text=row["text"],
            status=row["status"],
            timestamp=row["timestamp"],
            sentiment=row["sentiment"],
            category=row["category"],
            raw_result=row["raw_result"],
        )
        
        complaints.append(complaint)
    
    return complaints