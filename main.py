from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
import yt_dlp
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
    return {"status": "Universal Multi-Engine Active"}

@app.get("/api/download")
def download_media(url: str, format: str = "mp4"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if format == "mp4" else 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            media_title = info.get('title', 'video')
            direct_url = info.get('url')

            if not direct_url and 'formats' in info:
                for f in reversed(info['formats']):
                    if format == "mp3" and f.get('vcodec') == 'none':
                        direct_url = f.get('url')
                        break
                    elif format == "mp4" and f.get('ext') == 'mp4':
                        direct_url = f.get('url')
                        break

            if direct_url:
                req = requests.get(direct_url, stream=True)
                filename = f"{media_title}.{format}"
                return StreamingResponse(
                    req.iter_content(chunk_size=1024*1024),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'}
                )
    except Exception:
        pass

    # Direct Fast Download Fallback Engine
    encoded_url = requests.utils.quote(url)
    if "youtube.com" in url or "youtu.be" in url:
        fallback_stream = f"https://loader.to/api/card/?url={encoded_url}&f={format}"
    else:
        fallback_stream = f"https://cobalt.tools/api/json"
    
    return RedirectResponse(url=fallback_stream)
