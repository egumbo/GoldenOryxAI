from fastapi import APIRouter, UploadFile, File
from app.services.vision_service import analyze_image_stub

router = APIRouter(prefix="/vision", tags=["Vision"])

@router.post("/analyze")
def analyze_image(file: UploadFile = File(...)):
    description = analyze_image_stub()
    return {"description": description}
