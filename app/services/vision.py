import base64
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(
)

# Defining the system prompt for AI Model

CROP_ANALYSIS_PROMPT = """ You are an expert agricultural scientist specializing in plant disease detection. Analyze the image and provide a detailed report on any diseases or abnormalities present, including their severity and potential impact on crop yield. Additionally, suggest possible treatments or interventions to mitigate the identified issues. 

Provide your analysis as a JSON object with exactly this structure:
{
    "crop_detected":"Name of the crop or plant visible in the image.",
    "severity":"Healthy" or "mild" or "moderate" or "crtitical",
    "diseases":[
        {
            "name":"Name of the disease detected",
            "confidence":0.0 to 1.0,
            "description":"Brief description of the disease and abnormality"
        }
    ],
    treatments":[
        {
            "treatment_name":"Name of the treatment",
            "treatment_type":"organic" or "chemical" or "preventive",
            "urgency":"immediage" or "within weeks" or "seasonal"
        }
    ],
    overall_health:"one sentence summary of the overall health of the crop based on the analysis",
    "additional_notes:"Any additional notes or recommendations for the farmer."

} """

async def analyse_image(image_content:bytes, content_type:str):
    """Analyse the image content using Google GenAI Vision API for disease detection."""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {"type": "text", "text": CROP_ANALYSIS_PROMPT},
            {
                "type": "image",
                "data": base64.b64encode(image_content).decode("utf-8"),
                "mime_type": content_type
            }
        ]
    )
    return json.loads(interaction.output_text)
