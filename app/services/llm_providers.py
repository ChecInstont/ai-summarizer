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
from langchain.schema import SystemMessage, HumanMessage
from fastapi import HTTPException
from app.schemas.models import SummarizeRequest
import logging

async def summarize_with_langchain(data: SummarizeRequest) -> str:

    """
    Generate a summary of the given text using specified AI provider.

    Args:
        data (SummarizeRequest): Input data containing:
            - text (str): Text to summarize. Must not be empty.
            - prompt (str, optional): Custom system prompt. Defaults to a generic summarizer prompt.
            - provider (str): AI provider name ('openai', 'azureopenai', 'anthropic', 'gemini').
            - model (str): Model name or deployment to use.
            - api_key (str): API key for authentication.
            - api_url (str, optional): API endpoint URL (for Azure).
            - temperature (float): Sampling temperature (0 to 1).
            - api_version (str, optional): API version (for Azure).

    Returns:
        str: Generated summary text.

    Raises:
        HTTPException: If input text is empty, provider is unsupported, or API call fails.
    """

    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty.")

    prompt = data.prompt or "You are a helpful summarizer."
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=text),
    ]

    # Debug: log message types and contents
    logging.debug("Messages sent to LLM:")
    for i, msg in enumerate(messages):
        logging.debug(f"Message {i}: Type={type(msg)}, Content={repr(msg.content)}")

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
            api_version=getattr(data, "api_version", "2023-05-15"),
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

    # Call agenerate once for all providers
    try:
        response = llm.invoke(messages)
        return response.content
    except AttributeError as e:
        logging.error(f"AttributeError: {e}. This usually means message format is wrong.")
        raise HTTPException(status_code=500, detail="Internal Server Error: message format issue.")
    except Exception as e:
        logging.error(f"Unexpected error from LLM: {e}")
        raise HTTPException(status_code=500, detail=f"AI API request failed: {str(e)}")
