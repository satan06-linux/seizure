"""
Utility functions
"""
from .pdf_reader import extract_text_from_pdf
from .image_reader import extract_text_from_image
from .edf_reader import read_edf_file

__all__ = [
    'extract_text_from_pdf',
    'extract_text_from_image',
    'read_edf_file'
]
