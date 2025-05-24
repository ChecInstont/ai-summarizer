"""
AI Summarization Module using LangChain wrappers for multiple LLM providers.

This module provides an asynchronous function to generate text summaries
using different large language model providers via LangChain abstractions.

Supported providers:
- OpenAI
- Azure OpenAI
- Anthropic
- Gemini (Google Generative AI)

The function `summarize_with_langchain` accepts a `SummarizeRequest` data
model containing text, prompt, provider info, API keys, and model parameters.
It validates input and returns the summarized text from the chosen provider.

Errors in provider selection or API calls raise HTTPException with details.

Logging is included for debugging message formatting and errors.

Usage:
    response_text = await summarize_with_langchain(data)
"""


from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import HTTPException

def llm_provider(data):
    """
    Initialize a LangChain-compatible chat model instance based on the AI provider.

    Args:
        data (SummarizeRequest or ChatRequest): An object containing the following fields:
            - provider (str): Name of the provider ("openai", "azureopenai", "anthropic", or "gemini").
            - model (str): Model name or deployment ID (for Azure).
            - api_key (str): API key for authentication.
            - api_url (str, optional): Base API URL (used by Azure OpenAI).
            - api_version (str, optional): API version for Azure OpenAI (default "2025-01-01").
            - temperature (float): Sampling temperature for model response diversity.

    Returns:
        BaseChatModel: An instance of a LangChain-compatible chat model.

    Raises:
        HTTPException: If the provider name is not recognized.
    """
    provider = data.provider.lower()

    if provider == "openai":
        llm = ChatOpenAI(
            model_name=data.model,
            temperature=data.temperature,
            openai_api_key=data.api_key,
        )
    elif provider in ("azure", "azureopenai"):
        llm = AzureChatOpenAI(
            azure_deployment=data.model,  # Azure uses deployment_name
            temperature=data.temperature,
            api_key=data.api_key,
            azure_endpoint=data.api_url,  # Correct param name
            api_version=getattr(data, "api_version", "2025-01-01"),
        )

    elif provider == "anthropic":
        llm = ChatAnthropic(
            model_name=data.model,
            api_key=data.api_key,
            temperature=data.temperature,
        )
    elif provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=data.model,
            temperature=data.temperature,
            api_key=data.api_key,
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {data.provider}")
    return llm

