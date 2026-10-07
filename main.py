from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
    return {"status": "Python Downloader Engine is Active!"}

@app.get("/api/download")
def download_video(url: str, format: str = "mp4"):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if format == "mp4" else 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
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

            if not direct_url:
                direct_url = info.get('webpage_url', url)

            req = requests.get(direct_url, stream=True)
            filename = f"{media_title}.{format}"
            
            return StreamingResponse(
                req.iter_content(chunk_size=1024*1024),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"'
                }
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
