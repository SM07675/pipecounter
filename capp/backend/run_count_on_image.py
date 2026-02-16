
import os
from ultralytics import YOLO
import cv2

def count_objects():
    # Setup paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR) 
    MODEL_PATH = os.path.join(PROJECT_ROOT, "runs", "object_counter3", "weights", "best.pt")
    
    IMAGE_PATH = r"C:\Users\sarve\Downloads\2-inch-pipes.png"
    
    print(f"Loading model from: {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        print("Model not found!")
        return

    model = YOLO(MODEL_PATH)
    
    print(f"Predicting on: {IMAGE_PATH}")
    results = model.predict(IMAGE_PATH)
    
    total_count = 0
    if len(results) > 0:
        boxes = results[0].boxes
        total_count = len(boxes)
        print(f"Total objects detected: {total_count}")
        for box in boxes:
            print(f" - Class: {int(box.cls[0])}, Conf: {float(box.conf[0]):.2f}")
    else:
        print("No results returned.")

if __name__ == "__main__":
    count_objects()
