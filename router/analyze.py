from fastapi import APIRouter, UploadFile, File
from core.engine import analyze_chart
from core.image_loader import load_image

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("/")
async def analyze_endpoint(file: UploadFile = File(...)):
    try:
        # Load the uploaded image
        image = load_image(await file.read())

        # Run analysis engine
        result = analyze_chart(image)

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
  }
