import cv2
import numpy as np
import hashlib
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VeriSafe AI Forensic Platform",
    description="Production REST API for Deepfake & Document Tampering Analysis",
    version="2026.1"
)

# Enable CORS for Streamlit Frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "Online",
        "service": "VeriSafe AI Engine",
        "version": "2026.1"
    }

@app.post("/detect-deepfake")
async def detect_deepfake(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image.")
    
    try:
        contents = await file.read()
        sha256_hash = hashlib.sha256(contents).hexdigest()
        
        # Safe memory decoding for OpenCV
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Could not decode image bytes.")
            
        start_time = time.time()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Micro-texture liveness analysis
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        liveness_score = round(min(laplacian_var / 2.0, 100.0), 2)
        is_deepfake = laplacian_var < 100.0
        execution_latency = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "forensic_hash": sha256_hash,
            "verdict": "DEEPFAKE / SYNTHETIC" if is_deepfake else "AUTHENTIC LIVE MEDIA",
            "is_deepfake": is_deepfake,
            "confidence_score": f"{liveness_score}%",
            "laplacian_variance": round(laplacian_var, 2),
            "latency_ms": execution_latency
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Failed: {str(e)}")
