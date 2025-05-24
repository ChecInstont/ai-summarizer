"""
Chat Service Module with Memory Support per Visitor

This module enables chatting with AI using LangChain-compatible LLMs
while preserving conversation history for each visitor.

Features:
- Stores chat history using `ChatMessageHistory` keyed by `visitor_id`
- Associates a system prompt based on the visitor’s summary
- Routes the conversation through the appropriate LLM provider using `llm_provider`
- Maintains memory for follow-up questions

Requirements:
- Summarization must occur first to populate `visitor_summaries`

Usage:
    response = await chat_with_ai(data)

Raises:
    HTTPException if summary is missing or AI call fails
"""

from typing import Dict
import logging
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from fastapi import HTTPException
from app.schemas.models import ChatRequest
from app.services.llm_providers import llm_provider

# Stores chat history for each visitor (to enable contextual memory)
chat_histories: Dict[str, ChatMessageHistory] = {}

# Stores pre-generated summaries for each visitor
visitor_summaries: Dict[str, str] = {}


def get_history(visitor_id: str) -> ChatMessageHistory:
    """
    Retrieve or create a chat history object for the visitor.

    If no history exists, a new one is initialized with a system prompt
    embedding the provided summary for context.

    Args:
        visitor_id (str): Unique identifier for the visitor.
        summary (str): Summarized content to use as the system context.

    Returns:
        ChatMessageHistory: In-memory conversation history.
    """
    if visitor_id not in chat_histories:
        history = ChatMessageHistory()
        history.add_message(SystemMessage(
            content="You are a helpful assistant"
        ))
        chat_histories[visitor_id] = history
    return chat_histories[visitor_id]


async def chat_with_ai(data: ChatRequest) -> Dict[str, str]:
    """
    Process a chat request using the specified LLM provider with visitor-specific memory.

    Requires that a summary has already been generated and stored for the visitor.
    The function maintains context by using a stored message history.

    Args:
        data (ChatRequest): Chat request containing:
            - visitor_id (str): Identifier for session continuity.
            - message (str): The latest user message.
            - provider/model/api_key/etc.: Model configuration for the LLM provider.

    Returns:
        dict: A dictionary with a single key `reply` containing the AI-generated response.

    Raises:
        HTTPException: If no summary is found or if the AI call fails.
    """
    visitor_id = data.visitor_id

    history = get_history(visitor_id)

    # Append user message to history
    history.add_message(HumanMessage(content=data.message))

    try:
        # Initialize LLM instance based on provider/model config
        llm = llm_provider(data)

        # Send entire conversation history to LLM
        response = await llm.ainvoke(history.messages)
        reply = response.content

        # Save AI's reply in history
        history.add_message(AIMessage(content=reply))

        return {"answer": reply}

    except Exception as e:
        logging.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get response from AI.")
