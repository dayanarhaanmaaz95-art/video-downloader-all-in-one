from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
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
    return {"status": "Universal Direct Engine Active"}

@app.get("/api/download")
def download_media(url: str, quality: str = "1080", format: str = "mp4"):
    if not url:
        raise HTTPException(status_code=400, detail="URL missing")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    req_body = {
        "url": url,
        "videoQuality": quality,
        "downloadMode": "audio" if format == "mp3" else "auto"
    }

    # Fast High-Speed Global Stream Endpoints
    instances = [
        "https://co.wuk.sh/api/json",
        "https://api.cobalt.tools/api/json",
        "https://cobalt-api.kwippy.com/api/json"
    ]

    for endpoint in instances:
        try:
            res = requests.post(endpoint, json=req_body, headers=headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                if "url" in data:
                    # Direct redirect to real media file server (Prevents 28 KB empty file)
                    return RedirectResponse(url=data["url"])
        except Exception:
            continue

    # Fallback to direct stream node
    encoded_url = requests.utils.quote(url)
    fallback_url = f"https://loader.to/api/button/?url={encoded_url}&f={format}&q={quality}"
    return RedirectResponse(url=fallback_url)
