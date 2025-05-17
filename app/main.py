
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import summarize, upload, history, visitor

app = FastAPI(title="AI Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(summarize.router, prefix="/api/summarize", tags=["Summarization"])
app.include_router(upload.router, prefix="/api/upload", tags=["File Upload"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(visitor.router, prefix="/api/visitor", tags=["Visitor"])


# Optional: If you want a specific route to serve index.html explicitly
@app.get("/api/health")
async def health():
    """
    Check status of application
    """
    return {"status":"Ok"}



# Mount the frontend folder as static files under root
app.mount("/", StaticFiles(directory="./frontend", html=True), name="frontend")

# Optional: If you want a specific route to serve index.html explicitly
@app.get("/")
async def root():
    """
    Load HTML File
    """
    return FileResponse(os.path.join("frontend", "index.html"))

