"""
summary_route.py

This module defines the API route for text summarization using various AI providers.

It exposes a POST endpoint that accepts text input along with AI configuration parameters
and returns a generated summary.

The endpoint also stores the summarization request and response metadata in the database,
including the input text, summary, model used, provider, and creation timestamp.

Dependencies:
- FastAPI for routing and dependency injection.
- A database dependency injected via Depends(get_db).
- An external summarization service implemented in summarize_with_langchain().

Usage:
- POST requests to the root path ('') with JSON body conforming to SummarizeRequest schema.
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

from datetime import datetime
from fastapi import APIRouter, Depends
from app.schemas.models import SummarizeRequest
from app.dependencies import get_db
from app.services.llm_providers import summarize_with_langchain


router = APIRouter()

@router.post("")
async def summarize(data: SummarizeRequest, db=Depends(get_db)):

    """
    Endpoint to generate a summary from given text using specified AI provider.

    Args:
        data (SummarizeRequest): The request body containing:
            - text (str): Text to be summarized.
            - prompt (str, optional): Custom prompt for the AI.
            - provider (str): AI provider name.
            - model (str): Model or deployment name.
            - api_key (str): API key for authentication.
            - api_url (str, optional): API endpoint URL (for Azure).
            - temperature (float): Sampling temperature for generation.

        db: Async database session dependency.

    Returns:
        JSON response containing the generated summary text.

    Raises:
        HTTPException: Propagated from the summarize_with_langchain function on errors.
    """


    summary_text = await summarize_with_langchain(data)

    await db.summaries.insert_one({
        "input_text": data.text,
        "summary_text": summary_text,
        "model": data.model,
        "provider": data.provider,
        "created_at": datetime.utcnow(),
    })

    return {"summary": summary_text}
