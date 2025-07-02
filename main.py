from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI()

HF_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Please set HF_API_TOKEN in .env file")

API_URL = "https://api-inference.huggingface.co/models/Falconsai/nsfw_image_detection"

@app.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    logging.info(f"File content type: {file.content_type}")

    headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": file.content_type or "application/octet-stream"
}
    try:
        resp = requests.post(
            API_URL,
            data=content,
            headers=headers,
            timeout=10
        )
    except requests.RequestException as e:
        logging.error(f"Request to Hugging Face failed: {e}")
        raise HTTPException(status_code=502, detail="Failed to contact Hugging Face API")

    try:
        data = resp.json()
    except ValueError:
        logging.error(f"Hugging Face returned non-JSON response: {resp.text}")
        raise HTTPException(status_code=502, detail="Invalid response from Hugging Face API")

    logging.info(f"Hugging Face response: {data}")

    if isinstance(data, dict) and "error" in data:
        logging.error(f"Hugging Face API error: {data['error']}")
        raise HTTPException(status_code=503, detail=f"Hugging Face API error: {data['error']}")

    if not isinstance(data, list):
        logging.error(f"Unexpected Hugging Face response structure: {data}")
        raise HTTPException(status_code=502, detail="Unexpected Hugging Face response structure")

    nsfw_score = next((item["score"] for item in data if item["label"] == "nsfw"), None)

    if nsfw_score is None:
        logging.error(f"'nsfw' label not found in response: {data}")
        raise HTTPException(status_code=502, detail="Could not find 'nsfw' score in response")

    logging.info(f"nsfw_score = {nsfw_score}")

    if nsfw_score > 0.7:
        return {"status": "REJECTED", "reason": "NSFW content", "score": nsfw_score}
    
    return {"status": "OK", "score": nsfw_score}
