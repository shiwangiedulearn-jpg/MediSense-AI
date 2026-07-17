import pdfplumber
import fitz
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

import platform
import pytesseract

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_pdf_text(uploaded_file)
    else:
        return extract_image_text(uploaded_file)

def extract_pdf_text(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_image_text(uploaded_file):

    image = Image.open(uploaded_file)

    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.Resampling.LANCZOS
    )


    image = image.convert("L")

    image = ImageEnhance.Contrast(image).enhance(2.5)

    image = image.filter(ImageFilter.SHARPEN)

    text = pytesseract.image_to_string(
        image,
        config="--oem 3 --psm 4"
    )

    return text