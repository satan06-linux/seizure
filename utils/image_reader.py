"""
Image Reader Utility using OCR
"""
import pytesseract
from PIL import Image


def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise Exception(f"Error reading image: {str(e)}")
