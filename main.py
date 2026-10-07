from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RapidAPI Details
RAPIDAPI_URL = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
# Aapki RapidAPI key playground window se automatically link ho jaayegi
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"  # Isse apni RapidAPI key se replace karein

@app.get("/")
def home():
    return {"status": "RapidAPI Engine Active"}

@app.post("/api/get-direct-link")
def get_direct_link(payload: dict):
    url = payload.get("url", "").strip()
    quality = payload.get("quality", "1080")
    format_type = payload.get("format", "mp4")

    if not url:
        raise HTTPException(status_code=400, detail="URL is missing")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(RAPIDAPI_URL, json={"url": url}, headers=headers, timeout=10)
        data = response.json()

        if "medias" in data and len(data["medias"]) > 0:
            medias = data["medias"]
            download_url = None

            if format_type == "mp3":
                for item in medias:
                    if item.get("extension") == "mp3" or item.get("quality") == "audio":
                        download_url = item.get("url")
                        break
            else:
                # Video quality filter based on response
                if quality == "1080" or quality == "720":
                    download_url = medias[0].get("url")  # hd_no_watermark / high quality
                else:
                    download_url = medias[1].get("url") if len(medias) > 1 else medias[0].get("url")

            if not download_url:
                download_url = medias[0].get("url")

            return {"status": "success", "url": download_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "error", "message": "Failed to fetch link"}
