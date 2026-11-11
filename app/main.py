from fastapi import FastAPI
from dotenv import load_dotenv

from app.routes.analyse import router as analyse_router

load_dotenv()  # Load environment variables from .env file
app = FastAPI(
    title="NetraVision API",
    description="Crop disease detection using Gemini Vision. Upload plant photos, get disease diagnosis and treatment plans ",
    version="0.1.0",
)

app.include_router(analyse_router)


@app.get("/")
async def root():
    return {"app": "NetraVision API",
            "version":"0.1.0",
            "endpoints":{
                "POST/analyse": "Upload plant photo for disease detection",
                "POST/analyse/batch": "Upload multiple plant photos for disease detection",
                "GET/analysis/": "Get analysis result by ID",
                "GET/analysis/{image_id}": "Get analysis result by ID",
            }
    }