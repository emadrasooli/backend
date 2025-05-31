from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import asyncio, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

DATA_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 256 * 1024

@app.get("/download")
async def download():
    async def streamer():
        sent = 0
        while sent < DATA_SIZE:
            chunk = b"x" * min(CHUNK_SIZE, DATA_SIZE - sent)
            sent += len(chunk)
            yield chunk
            await asyncio.sleep(0)
    return StreamingResponse(streamer(), media_type="application/octet-stream")

@app.post("/upload")
async def upload(request: Request):
    total = 0
    async for chunk in request.stream():
        total += len(chunk)
    return JSONResponse({"received_bytes": total})

@app.get("/ping")
def ping():
    return {"timestamp": time.time()}
