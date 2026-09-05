from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import cv2
import hashlib
import time

app = FastAPI(title="VeriSafe AI Forensic API", version="2026.1")

@app.get("/")
def root():
    return {"status": "VeriSafe AI Backend API is operational"}

@app.post("/detect-deepfake")
async def detect_deepfake(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        doc_hash = hashlib.sha256(contents).hexdigest()
        
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        start_time = time.time()
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        is_deepfake = laplacian_var < 100.0
        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "status": "Success",
            "sha256_hash": doc_hash,
            "results": {
                "is_deepfake": is_deepfake,
                "liveness_score": f"{min(laplacian_var / 2.0, 100.0):.2f}%",
                "variance": round(laplacian_var, 2),
                "latency_ms": execution_time_ms
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))