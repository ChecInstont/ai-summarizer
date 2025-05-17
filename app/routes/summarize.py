"""
summarize.py

This module defines the API route for text summarization using various AI providers.

It exposes a POST endpoint that accepts text input along with AI configuration parameters
and returns a generated summary.

The endpoint also stores the summarization request and response metadata in the database,
including the input text, summary, model used, provider, timestamp, and the visitor ID.

Dependencies:
- FastAPI for routing and dependency injection.
- A database dependency injected via Depends(get_db).
- An external summarization service implemented in summarize_with_langchain().

Usage:
- POST requests to the root path ('') with JSON body conforming to SummarizeRequest schema.
- Requires 'X-Visitor-ID' header to track visitor-specific summaries.
- Returns JSON with generated summary text.

Example request body:
{
    "text": "Your input text here",
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
    "api_key": "your_api_key",
    "api_url": "https://api.openai.com/v1/chat/completions",
    "prompt": "Optional system prompt"
}
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header, HTTPException
from app.schemas.models import SummarizeRequest
from app.dependencies import get_db
from app.services.llm_providers import summarize_with_langchain

router = APIRouter()

@router.post("")
async def summarize(
    data: SummarizeRequest,
    db=Depends(get_db),
    visitor_id: str = Header(None, alias="X-Visitor-ID")
):
    """
    Endpoint to generate a summary from given text using specified AI provider.

    Args:
        data (SummarizeRequest): The request body containing summarization input and config.
        db: MongoDB async database session dependency.
        visitor_id (str): ID from the 'X-Visitor-ID' header to associate with the summary.

    Returns:
        dict: JSON response containing the generated summary text.

    Raises:
        HTTPException: If the visitor ID is missing or summarization fails.
    """
    if not visitor_id:
        raise HTTPException(status_code=400, detail="Missing X-Visitor-ID header")

    summary_text = await summarize_with_langchain(data)

    await db.summaries.insert_one({
        "visitor_id": visitor_id,
        "input_text": data.text,
        "summary_text": summary_text,
        "model": data.model,
        "provider": data.provider,
        "created_at": datetime.now(timezone.utc),
    })

    return {"summary": summary_text}
