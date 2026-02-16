from fastapi import FastAPI, UploadFile, File, HTTPException
from database import db
from models import PredictionResult
from ultralytics import YOLO
import asyncio
from PIL import Image
import shutil
import os
import json
from typing import List

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
# Trying to find the best model from previous runs, else fallback
# Dynamically find the model path relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "runs", "object_counter3", "weights", "best.pt")
if not os.path.exists(MODEL_PATH):
    # Fallback/Check if there is another run or just use yolov8n
    MODEL_PATH = "yolov8n.pt" 
    print(f"Custom model not found, using {MODEL_PATH}")
else:
    print(f"Loading custom model from {MODEL_PATH}")

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    print("Health check endpoint (/) called")
    return {"message": "AI Object Counter API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    print(f"Received prediction request for file: {file.filename}")
    if not model:
        print("Error: Model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if db is None:
        print("Error: Database connection not available")
        raise HTTPException(status_code=500, detail="Database connection not available")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run Inference (Offload to thread to verify non-blocking behavior)
    try:
        def process_and_infer(path):
            # 1. Resize Image for Speed
            try:
                with Image.open(path) as img:
                    if img.width > 640 or img.height > 640:
                        img.thumbnail((640, 640))
                        img.save(path)
                        print(f"Resized image to {img.size}")
            except Exception as resize_err:
                print(f"Warning: Could not resize image: {resize_err}")

            # 2. Predict
            print("Running inference...")
            return model.predict(path, conf=0.15)

        results = await asyncio.to_thread(process_and_infer, file_path)
        
        print("Inference complete.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")

    result = results[0]
    
    count = len(result.boxes)
    class_counts = {}
    for box in result.boxes:
        cls_id = int(box.cls[0])
        if model.names:
            cls_name = model.names[cls_id]
        else:
            cls_name = str(cls_id)
        class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
        
    # Save to DB
    try:
        pred_data = PredictionResult(
            filename=file.filename,
            object_count=count,
            details=class_counts
        )
        # Convert pydantic model to dict
        doc = pred_data.model_dump()
        new_prediction = await db["predictions"].insert_one(doc)
        db_id = str(new_prediction.inserted_id)
    except Exception as e:
        print(f"Database error: {e}")
        db_id = None
    
    return {
        "filename": file.filename,
        "count": count,
        "details": class_counts,
        "id": db_id
    }

@app.get("/history")
async def get_history():
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
        
    try:
        # Fetch last 100 records
        predictions = await db["predictions"].find().sort("created_at", -1).to_list(length=100)
        # Convert _id ObjectId to string for JSON serialization
        results = []
        for p in predictions:
            p["id"] = str(p["_id"])
            del p["_id"]
            results.append(p)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
