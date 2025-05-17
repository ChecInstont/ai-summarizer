"""
models/summary_record.py

This module defines the SummaryRecord Pydantic model used for representing
and validating summarized data records stored in the database.

Classes:
    SummaryRecord: A model representing the structure of a summarized entry,
                   including input text, summary result, metadata, and timestamp.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class SummaryRecord(BaseModel):
    """
    Pydantic model representing a summarized text entry stored in the database.

    Attributes:
        id (Optional[str]): Unique identifier (usually MongoDB ObjectId, aliased as '_id').
        input_text (str): The original input text provided by the user.
        summary_text (str): The AI-generated summary of the input text.
        model (str): The name of the model used to generate the summary.
        provider (str): The AI provider used (e.g., OpenAI, Gemini).
        created_at (datetime): Timestamp of when the summary was created.
    """
    id: Optional[str] = Field(None, alias="_id")
    input_text: str
    summary_text: str
    model: str
    provider: str
    created_at: datetime
