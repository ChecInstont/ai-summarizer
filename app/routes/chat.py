from fastapi import APIRouter
from app.schemas.models import ChatRequest
from app.services.chat_instance import chat_with_ai

router = APIRouter()

@router.post("", summary="Chat with AI using contextual memory")
async def chat_endpoint(data: ChatRequest):
    """
    Interact with the AI model using memory of previous messages tied to the visitor.

    Requirements:
    - The visitor must have completed summarization (summary is stored).
    - Model/provider credentials must be included in the request.

    Returns:
        dict: JSON response with the AI's reply.

    Raises:
        400: If the visitor has not summarized yet.
        500: If the LLM call fails.
    """
    return await chat_with_ai(data)
