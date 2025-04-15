from datetime import datetime
import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx

from models import SentimentType


load_dotenv()

api_url = "https://api.apilayer.com/sentiment/analysis"
api_key = os.getenv("api_key")

async def analyze_sentiment(text):
    if not api_key:
        raise HTTPException(status_code=500, detail="api not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "apikey": api_key,
                "Content-Type": "text/plain"
            }
            
            response = await client.post(
                api_url,
                content=text,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            
            return response.json()
        except (httpx.HTTPStatusError, httpx.RequestError, Exception) as e:
            return{
                "sentiment": "unknown"
            }

def datermine_sentiment_type(sentiment_result):
    sentiment = sentiment_result.get("sentiment", "").lower()

    match sentiment:
        case "positive":
            return SentimentType.positive
        case "positive":
            return SentimentType.positive
        case "positive":
            return SentimentType.positive
        case "positive":
            return SentimentType.positive
        

    if sentiment == "positive":
        return SentimentType.positive
    elif sentiment == "negative":
        return SentimentType.negative
    else:
        return SentimentType.neutral

def prepare_complaint_data(text, category, sentiment_result):
    sentiment_type = datermine_sentiment_type(sentiment_result)

    return{
        "text": text,
        "status": "new",
        "timestamp": datetime.now().isoformat(),
        "sentiment": sentiment_type,
        "category": category,
        "raw_result": json.dumps(sentiment_result)
    }