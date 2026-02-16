import os
from ultralytics import YOLO
import numpy as np
from PIL import Image

def test_model():
    # Setup paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Go up one level from backend to capp, then to runs/...
    # Note: the original code had BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # because main.py is in backend/ and it wants to reach runs/ which is in capp/
    # So if this file is in backend/ too, the logic is the same.
    PROJECT_ROOT = os.path.dirname(BASE_DIR) 
    MODEL_PATH = os.path.join(PROJECT_ROOT, "runs", "object_counter3", "weights", "best.pt")
    
    print(f"Testing Model Path: {MODEL_PATH}")
    
    if not os.path.exists(MODEL_PATH):
        print("ERROR: Model file not found at path!")
        return

    try:
        print("Loading model...")
        model = YOLO(MODEL_PATH)
        print("Model loaded successfully.")
        
        # Create a dummy image for testing if no real image is provided
        print("Creating dummy image...")
        img = Image.new('RGB', (640, 640), color = (73, 109, 137))
        dummy_path = os.path.join(BASE_DIR, "debug_test_image.jpg")
        img.save(dummy_path)
        
        print(f"Running inference on {dummy_path}...")
        results = model.predict(dummy_path)
        
        print("Inference successful!")
        print(f"Results: {results}")
        
        # specific check for boxes
        if len(results) > 0:
            print(f"Objects detected: {len(results[0].boxes)}")
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                print(f" - Class: {cls_id}, Conf: {conf}")

        # Cleanup
        if os.path.exists(dummy_path):
            os.remove(dummy_path)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_model()
