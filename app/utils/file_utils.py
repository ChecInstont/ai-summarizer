"""
file_utils.py

This module provides utility functions for handling file processing tasks
such as extracting text content from PDF documents.

Functions:
    extract_text_from_pdf(path: str) -> str:
        Extracts and returns all text from a PDF file located at the specified path.
"""

from PyPDF2 import PdfReader

async def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a PDF file using PyPDF2.

    Args:
        path (str): The file system path to the PDF file.

    Returns:
        str: The extracted text from all pages of the PDF, joined by newlines.
             Returns an empty string for pages without extractable text.

    Note:
        PyPDF2 does not support scanned image PDFs; it works on text-based PDFs only.
    """
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)
