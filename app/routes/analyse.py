from fastapi import APIRouter, UploadFile, File, HTTPException
from services.image import validate_image,resize_image, save_image
import uuid

router = APIRouter(
    prefix="/analyse",
    tags=["Analyse"]
)

async def process_single_file(file:UploadFile):
    """Process a single uploaded image file for disease detection."""
    content = await file.read()

    validation = validate_image(content, file.content_type)
    if not validation ["is_valid"]:
        raise HTTPException(status_code=400, detail=validation["message"])

    # Resize the image
    resized_content = resize_image(content)

    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    # Save the image
    save_image(resized_content,"uploads", unique_name)

@router.post("/")
async def analyse_image(file:UploadFile = File(...)):
    """Endpoint to upload an image for disease detection."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, details ="Invalid file type. Please upload an image.")