"""
schemas/models.py

This module defines the data schema for text summarization requests
handled by the summarization API. It uses Pydantic for data validation
and serialization.

Model:
    SummarizeRequest: Request model containing all necessary parameters 
    to invoke a language model from different providers like OpenAI, 
    Azure OpenAI, Anthropic, or Gemini.

Usage:
    This schema is used in the POST `/summarize` endpoint to validate
    and extract the request body fields.
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class SummarizeRequest(BaseModel):

    """
    Schema for summarization request sent to the LLM summarizer endpoint.

    Attributes:
        text (str): The input text to be summarized.
        api_url (str): The base API URL of the LLM provider.
        api_key (str): The API key used to authenticate with the provider.
        model (str): The name or deployment ID of the model to use.
        temperature (float, optional): Sampling temperature (0–1). Defaults to 0.5.
        prompt (str, optional): Optional custom system prompt for context setting.
        provider (str, optional): Name of the AI provider (e.g., "openai", "azureopenai", "anthropic", "gemini"). Defaults to "gemini".
        api_version (str, optional): Optional version identifier for APIs that require it (e.g., Azure OpenAI). Defaults to "".
    """

    text: str
    api_url: str
    api_key: str
    model: str
    temperature: Optional[float] = 0.5
    prompt: Optional[str] = None
    provider: Optional[str] = "gemini"
    api_version: Optional[str] = ""


class ChatMessage(BaseModel):
    """
    Represents a single message in the chat history.

    Attributes:
        role (str): The role of the message sender. Should be "user" or "assistant".
        content (str): The textual content of the message.
    """
    role: Literal["user", "assistant"] = Field(..., description='Role of the sender ("user" or "assistant").')
    content: str = Field(..., description="The actual message text.")


class ChatRequest(BaseModel):
    """
    Schema for AI chat requests sent to the LLM chat endpoint.

    Attributes:
        history (List[ChatMessage]): The complete conversation history as a list of messages.
        api_url (str): The base API URL of the LLM provider.
        api_key (str): The API key used to authenticate with the provider.
        model (str): The name or deployment ID of the model to use.
        temperature (float, optional): Sampling temperature (0–1). Defaults to 0.7.
        provider (str, optional): Name of the AI provider (e.g., "openai", "azureopenai", "anthropic", "gemini"). Defaults to "gemini".
        api_version (str, optional): Optional version identifier for APIs that require it (e.g., Azure OpenAI). Defaults to "".
    """
    message: str = Field(..., description="user inputs to AI.")
    api_url: str = Field(..., description="Base API URL of the LLM provider.")
    api_key: str = Field(..., description="API key to authenticate with the provider.")
    model: str = Field(..., description="Model name or deployment ID.")
    temperature: float = Field(0.7, description="Sampling temperature (0–1).")
    provider: str = Field("gemini", description='AI provider (e.g., "openai", "azureopenai", "anthropic", "gemini").')
    api_version: str = Field("", description="Optional version for some APIs (e.g., Azure).")
    visitor_id: str = Field("", description="Unique ID of user.")
