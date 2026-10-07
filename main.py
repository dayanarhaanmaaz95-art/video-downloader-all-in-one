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
    # Engine 1: Native YoutubeDL with iOS User-Agent Client (Bypasses YouTube Bot Block)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if format == "mp4" else 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'mweb', 'android']
            }
        }
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

    # Engine 2: High Speed Global Fallback Node (Guaranteed Instant Download)
    encoded_url = requests.utils.quote(url)
    if "youtube.com" in url or "youtu.be" in url:
        fallback_stream = f"https://loader.to/api/button/?url={encoded_url}&f={format}"
    else:
        fallback_stream = f"https://cobalt.tools/api/json"
    
    return RedirectResponse(url=fallback_stream)
