"""
resume_parser.py - Handles resume file upload and text extraction.
Supports PDF files with fallback error handling.
"""

import re
import io
from typing import Optional


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from a PDF file object.
    Tries pdfplumber first (better layout handling), falls back to PyPDF2.

    Args:
        file: File-like object (from Streamlit uploader)

    Returns:
        Extracted text string
    """
    text = ""

    # Try pdfplumber first (handles complex layouts better)
    try:
        import pdfplumber
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        import PyPDF2
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # Last fallback: try pypdf
    try:
        from pypdf import PdfReader
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Could not extract text from PDF: {str(e)}")

    return text


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize extracted resume text.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    # Fix common PDF extraction artifacts
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase splits

    return text.strip()

