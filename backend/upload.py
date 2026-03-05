from fastapi import APIRouter, UploadFile, File
import fitz
import uuid

from embeddings import store_paper

router = APIRouter()


@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):

    try:
        # Read file content
        content = await file.read()

        # Open PDF
        doc = fitz.open(stream=content, filetype="pdf")

        # Extract text properly
        text = ""

        for page in doc:
            text += page.get_text("text")

        doc.close()

        # Validate extracted text
        if not text or len(text.strip()) < 50:
            return {
                "status": "error",
                "message": "PDF text extraction failed or PDF contains no readable text"
            }

        # Generate unique paper ID
        paper_id = str(uuid.uuid4())

        # Store in vector database
        store_paper(paper_id, text)

        return {
            "status": "success",
            "paper_id": paper_id,
            "characters_extracted": len(text),
            "message": "Paper uploaded and embedded successfully"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
