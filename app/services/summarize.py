import logging
from langchain.schema import SystemMessage, HumanMessage
from fastapi import HTTPException
from app.schemas.models import SummarizeRequest
from app.services.llm_providers import llm_provider

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
    logging.info("Messages sent to LLM:")
    for i, msg in enumerate(messages):
        logging.info(f"Message {i}: Type={type(msg)}, Content={repr(msg.content)}")

    llm = llm_provider(data)

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
