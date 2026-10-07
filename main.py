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
    return {"status": "Clean Direct Stream Engine Active"}

@app.get("/api/download")
def download_media(url: str, format: str = "mp4"):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # Clean Cobalt / Direct Engine Node
    payload = {
        "url": url,
        "videoQuality": "1080",
        "downloadMode": "audio" if format == "mp3" else "auto"
    }

    try:
        res = requests.post("https://co.wuk.sh/api/json", json=payload, headers=headers, timeout=10)
        data = res.json()
        if "url" in data:
            return {"status": "success", "url": data["url"]}
    except Exception:
        pass

    # Backup Engine
    try:
        res2 = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers, timeout=10)
        data2 = res2.json()
        if "url" in data2:
            return {"status": "success", "url": data2["url"]}
    except Exception:
        pass

    raise HTTPException(status_code=400, detail="Unable to extract direct link")
