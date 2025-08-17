# fastapi-tesseract

🌐 Use the API

Open a new terminal window (don’t close the server!) and run:
bash
1
2
curl -X POST <http://localhost:8000/ocr/pdf> \
     -F "file=@C:/Users/YourName/Downloads/your_arabic_document.pdf"

📌 Note:

    Use forward slashes / in the path
    Include the @ before the file path
    Replace with your actual PDF path
     

You’ll get back the extracted Arabic text!
