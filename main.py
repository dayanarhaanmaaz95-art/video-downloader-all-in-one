from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

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
    return {"status": "Universal Multi-Engine Active"}

@app.post("/api/get-direct-link")
def get_direct_link(payload: dict):
    url = payload.get("url", "").strip()
    quality = payload.get("quality", "1080")
    format_type = payload.get("format", "mp4")

    if not url:
        raise HTTPException(status_code=400, detail="URL is missing")

    # Clean YouTube Shorts & Share Links
    clean_url = url.split("?")[0] if "youtube.com/shorts/" in url or "youtu.be/" in url else url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Engine 1: Cobalt Main
    cobalt_body = {
        "url": clean_url,
        "videoQuality": quality,
        "downloadMode": "audio" if format_type == "mp3" else "auto"
    }

    instances = [
        "https://co.wuk.sh/api/json",
        "https://api.cobalt.tools/api/json",
        "https://cobalt-api.kwippy.com/api/json"
    ]

    for endpoint in instances:
        try:
            res = requests.post(endpoint, json=cobalt_body, headers=headers, timeout=6)
            if res.status_code == 200:
                data = res.json()
                if "url" in data:
                    return {"status": "success", "url": data["url"]}
        except Exception:
            continue

    # Engine 2: Direct Universal Stream Backup (No Ads, Direct Saver)
    try:
        encoded_url = requests.utils.quote(clean_url)
        fallback_stream = f"https://loader.to/api/button/?url={encoded_url}&f={format_type}&q={quality}"
        return {"status": "success", "url": fallback_stream}
    except Exception as e:
        return {"status": "error", "message": "Failed to extract link"}
