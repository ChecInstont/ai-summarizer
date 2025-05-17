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

from typing import Optional
from pydantic import BaseModel

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
