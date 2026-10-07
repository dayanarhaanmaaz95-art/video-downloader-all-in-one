from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
    return {"status": "Universal Direct Engine Running"}

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

    # Clean Stream Extractors
    instances = [
        "https://co.wuk.sh/api/json",
        "https://api.cobalt.tools/api/json",
        "https://cobalt-api.kwippy.com/api/json"
    ]

    direct_file_url = None

    for endpoint in instances:
        try:
            res = requests.post(endpoint, json=req_body, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if "url" in data:
                    direct_file_url = data["url"]
                    break
        except Exception:
            continue

    if not direct_file_url:
        # Fallback for Universal Links
        encoded_url = requests.utils.quote(url)
        direct_file_url = f"https://loader.to/api/button/?url={encoded_url}&f={format}&q={quality}"

    # Stream file through backend to force direct file saving in browser (No new tab)
    try:
        stream_res = requests.get(direct_file_url, stream=True, timeout=15)
        ext = "mp3" if format == "mp3" else "mp4"
        filename = f"video_download_{quality}p.{ext}"

        return StreamingResponse(
            stream_res.iter_content(chunk_size=1024*1024),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
