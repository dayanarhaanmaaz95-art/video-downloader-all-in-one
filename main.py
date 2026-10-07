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

@app.get("/")
def home():
    return {"status": "Clean Direct Engine Active"}

@app.post("/api/get-direct-link")
def get_direct_link(payload: dict):
    url = payload.get("url", "").strip()
    quality = payload.get("quality", "1080")
    format_type = payload.get("format", "mp4")

    if not url:
        raise HTTPException(status_code=400, detail="URL missing")

    # Clean URL tracking parameters
    clean_url = url.split("?")[0] if ("youtube.com/shorts/" in url or "youtu.be/" in url) else url

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    req_body = {
        "url": clean_url,
        "videoQuality": quality,
        "downloadMode": "audio" if format_type == "mp3" else "auto"
    }

    # Only Clean Public Nodes (NO AD-SUPPORTED FALLBACKS)
    instances = [
        "https://co.wuk.sh/api/json",
        "https://api.cobalt.tools/api/json",
        "https://cobalt-api.kwippy.com/api/json"
    ]

    for endpoint in instances:
        try:
            res = requests.post(endpoint, json=req_body, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if "url" in data:
                    return {"status": "success", "url": data["url"]}
        except Exception:
            continue

    raise HTTPException(status_code=500, detail="Server busy. Please try another link.")
