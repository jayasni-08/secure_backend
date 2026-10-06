import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File as FastAPIFile,
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.file import File
from app.models.user import User
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not uploaded_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    content = uploaded_file.file.read()

    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )

    os.makedirs(
        settings.UPLOAD_DIR,
        exist_ok=True
    )

    extension = os.path.splitext(
        uploaded_file.filename
    )[1]

    stored_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        stored_filename
    )

    with open(file_path, "wb") as f:
        f.write(content)

    db_file = File(
        original_filename=uploaded_file.filename,
        stored_filename=stored_filename,
        owner_id=current_user.id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return {
        "id": db_file.id,
        "filename": db_file.original_filename,
        "message": "File uploaded successfully"
    }


@router.get("/")
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    files = (
        db.query(File)
        .filter(File.owner_id == current_user.id)
        .all()
    )

    return [
        {
            "id": file.id,
            "filename": file.original_filename,
            "uploaded_at": file.uploaded_at
        }
        for file in files
    ]