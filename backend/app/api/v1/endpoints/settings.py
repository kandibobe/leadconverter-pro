from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import shutil
from pathlib import Path
from app import crud, schemas
from app.api import deps

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/", response_model=schemas.CompanySettings)
def read_settings(db: Session = Depends(deps.get_db)):
    settings = crud.settings.get(db)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/", response_model=schemas.CompanySettings)
def update_settings(
    *,
    db: Session = Depends(deps.get_db),
    settings_in: schemas.CompanySettingsUpdate,
):
    current_settings = crud.settings.get(db)
    if not current_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    updated_settings = crud.settings.update(db=db, db_obj=current_settings, obj_in=settings_in)
    return updated_settings

@router.post("/upload-logo", response_model=schemas.CompanySettings)
def upload_logo(
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...)
):
    current_settings = crud.settings.get(db)
    if not current_settings:
        raise HTTPException(status_code=404, detail="Settings not found")

    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # В реальном приложении здесь будет загрузка в S3/Cloud Storage
    # Мы же просто сохраняем локально и отдаем путь
    logo_url = f"/uploads/{file.filename}"
    setattr(current_settings, 'logo_url', logo_url)
    db.commit()
    db.refresh(current_settings)
    
    return current_settings