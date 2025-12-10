# server/document_upload.py
"""
Document upload and OCR processing
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
import uuid
import shutil
import json
from datetime import datetime

router = APIRouter(prefix="/documents", tags=["documents"])

# Upload directory
UPLOAD_DIR = "uploads/documents"
METADATA_DIR = "uploads/metadata"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PAN, Aadhar, Bank Statement, etc.)
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_path)
        
        # Extract text if image
        extracted_data = None
        if file_ext in {'.jpg', '.jpeg', '.png'}:
            extracted_data = extract_text_from_image(file_path)
        
        # Save metadata
        metadata = {
            "file_id": file_id,
            "original_filename": file.filename,
            "file_path": file_path,
            "file_extension": file_ext,
            "size": file_size,
            "uploaded_at": datetime.now().isoformat(),
            "verified": False,
            "verification_status": "pending",
            "extracted_data": extracted_data
        }
        
        metadata_path = os.path.join(METADATA_DIR, f"{file_id}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "file_path": file_path,
            "size": file_size,
            "verified": False,
            "verification_status": "pending",
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/list")
async def list_documents():
    """List all uploaded documents with metadata"""
    try:
        documents = []
        for metadata_file in os.listdir(METADATA_DIR):
            if metadata_file.endswith('.json'):
                metadata_path = os.path.join(METADATA_DIR, metadata_file)
                with open(metadata_path, 'r') as f:
                    doc_data = json.load(f)
                    documents.append(doc_data)
        
        # Sort by upload date (newest first)
        documents.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
        
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/view/{file_id}")
async def view_document(file_id: str):
    """View a document (opens in browser)"""
    try:
        metadata_path = os.path.join(METADATA_DIR, f"{file_id}.json")
        
        if not os.path.exists(metadata_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        file_path = metadata['file_path']
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Determine media type
        ext = metadata.get('file_extension', '.pdf')
        media_type = 'application/pdf' if ext == '.pdf' else f'image/{ext[1:]}'
        
        return FileResponse(
            file_path,
            media_type=media_type,
            filename=metadata['original_filename']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_id}")
async def download_document(file_id: str):
    """Download a document"""
    try:
        metadata_path = os.path.join(METADATA_DIR, f"{file_id}.json")
        
        if not os.path.exists(metadata_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        file_path = metadata['file_path']
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        return FileResponse(
            file_path,
            media_type='application/octet-stream',
            filename=metadata['original_filename']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify/{file_id}")
async def verify_document(file_id: str):
    """Mark a document as verified"""
    try:
        metadata_path = os.path.join(METADATA_DIR, f"{file_id}.json")
        
        if not os.path.exists(metadata_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        metadata['verified'] = True
        metadata['verification_status'] = 'verified'
        metadata['verified_at'] = datetime.now().isoformat()
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {"message": "Document verified successfully", "file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def extract_text_from_image(image_path: str) -> dict:
    """
    Extract text from image using OCR (placeholder)
    In production, use pytesseract or cloud OCR
    """
    try:
        # Placeholder - would use pytesseract here
        # import pytesseract
        # from PIL import Image
        # image = Image.open(image_path)
        # text = pytesseract.image_to_string(image)
        
        return {
            "text": "OCR not configured - install pytesseract",
            "confidence": 0
        }
    except Exception as e:
        return {"error": str(e)}
