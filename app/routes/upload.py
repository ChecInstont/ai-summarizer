"""
upload_route.py

This module provides an API endpoint to handle file uploads for text extraction.

Supported file types:
- Plain text files (.txt)
- PDF files (.pdf)

The uploaded file is temporarily saved on the server, text is extracted from it,
and then the temporary file is deleted.

Features:
- Validates file content type before processing.
- Uses utility function `extract_text_from_pdf` for PDF text extraction.
- Returns the extracted text as JSON.

Dependencies:
- FastAPI for routing and request handling.
- Utility functions from app.utils.file_utils.
- Standard libraries os and shutil for file operations.

Usage:
- Send a POST request with a file under the key "file".
- Receives a JSON response containing the extracted text.
"""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_utils import extract_text_from_pdf

router = APIRouter()

@router.post("")
async def upload_file(file: UploadFile = File(...)):

    """
    Upload a text or PDF file and extract its textual content.

    Args:
        file (UploadFile): The uploaded file, required. Must be either plain text or PDF.

    Raises:
        HTTPException: If the uploaded file type is not supported.

    Returns:
        dict: JSON object with the key "text" containing the extracted textual content.
    """

    if file.content_type not in ["text/plain", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Only txt and pdf files are supported.")

    temp_path = f"{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    extracted_text = ""
    if file.content_type == "text/plain":
        with open(temp_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()
    else:
        extracted_text = await extract_text_from_pdf(temp_path)

    os.remove(temp_path)
    return {"text": extracted_text}
