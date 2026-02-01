import os
import uuid
from fastapi import UploadFile,HTTPException

"""
utility for handling file uploads.

why separate?
- Reusable
- Testable
- Keeps endpoints clean

"""

UPLOAD_DIR = "uploads/logos"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_logo(file: UploadFile) -> str:
    """
    Saves uploaded logo to disk and returns public URL.

    In production:
    - This could be S3, GCS, etc.

    """
    # UploadFile.filename can be None,
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must have a filename"
        )

    # Generate unique filename to avoid collisions
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4}.{file_extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file asynchronously
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Return relative path (frontend uses this)
    return f"/{UPLOAD_DIR}/{filename}"
