from fastapi import FastAPI
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

@app.get("/")
def home():
    return {"status": "Universal Stream Helper Active"}

@app.post("/api/extract")
def extract_media(payload: dict):
    url = payload.get("url")
    quality = payload.get("quality", "1080")
    is_audio = payload.get("isAudio", False)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    req_body = {
        "url": url,
        "videoQuality": quality,
        "downloadMode": "audio" if is_audio else "auto"
    }

    instances = [
        "https://co.wuk.sh/api/json",
        "https://api.cobalt.tools/api/json",
        "https://cobalt-api.kwippy.com/api/json"
    ]

    for endpoint in instances:
        try:
            res = requests.post(endpoint, json=req_body, headers=headers, timeout=8)
            data = res.json()
            if "url" in data:
                return {"status": "success", "url": data["url"]}
        except Exception:
            continue

    return {"status": "error", "message": "Unable to extract direct stream link"}
