# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from ocr_processor import ocr_pdf

app = FastAPI(title="PDF OCR API", description="Extract Arabic text from PDFs using Tesseract OCR")

@app.post("/ocr/pdf", response_class=JSONResponse)
async def ocr_pdf_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF file and get extracted text via OCR.
    Only Arabic (`ara`) language is supported.
    """

    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No filename in uploaded file")

    if not filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            temp_pdf_path = tmp_file.name

        # Perform OCR
        extracted_text = ocr_pdf(temp_pdf_path)

        # Clean up
        os.unlink(temp_pdf_path)

        return {
            "filename": file.filename,
            "text": extracted_text.strip()
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "PDF OCR API is running. Use POST /ocr/pdf to extract text."}