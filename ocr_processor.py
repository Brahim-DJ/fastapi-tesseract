# ocr_processor.py
import cv2
import pytesseract
import numpy as np
import os
from pdf2image import convert_from_path


def preprocess_image(image_path):
    """Preprocess image for better OCR results"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def rotate_image_for_ocr(image):
    """Auto-rotate image based on text orientation"""
    try:
        osd = pytesseract.image_to_osd(image)
        angle = int(osd.split('\n')[2].split(':')[1].strip())
        if angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    except Exception as e:
        pass
    return image


def ocr_image(image_path):
    """Perform OCR on image with rotation correction"""
    processed = preprocess_image(image_path)
    rotated = rotate_image_for_ocr(processed)
    custom_config = r'--oem 1 --psm 6 -c user_defined_dpi=300'
    text = pytesseract.image_to_string(rotated, config=custom_config, lang='ara')
    return text


def ocr_pdf(pdf_path):
    """Extract text from PDF by converting pages to images"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pages = convert_from_path(pdf_path, dpi=200)
    full_text = ""

    for i, page in enumerate(pages):
        temp_image = f"temp_page_{i}.jpg"
        page.save(temp_image, "JPEG")
        text = ocr_image(temp_image)
        full_text += f"\n--- Page {i+1} ---\n{text}"
        os.remove(temp_image)  # Cleanup

    return full_text