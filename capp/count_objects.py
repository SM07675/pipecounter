from ultralytics import YOLO
import os
import glob
import random

def count_objects_in_image(image_path):
    # Dynamically find paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "runs", "object_counter3", "weights", "best.pt")
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Using 'yolov8n.pt' for demo (untrained).")
        model = YOLO("yolov8n.pt")
    else:
        print(f"Loading custom trained model from {model_path}")
        model = YOLO(model_path)

    print(f"Predicting on: {image_path}")
    results = model.predict(image_path, save=True, project=os.path.join(BASE_DIR, "runs"), name="predict")
    
    for result in results:
        # result.boxes contains the detection boxes
        count = len(result.boxes)
        print(f"Detected {count} objects in {os.path.basename(image_path)}")
        
        # detailed class counts
        class_counts = {}
        for box in result.boxes:
            cls_id = int(box.cls[0])
            if result.names:
                cls_name = result.names[cls_id]
            else:
                cls_name = str(cls_id)
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
            
        print("Breakdown per class:")
        for cls_name, cls_count in class_counts.items():
            print(f"  {cls_name}: {cls_count}")

def main():
    # Pick a random image from test set
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    test_images_dir = os.path.join(BASE_DIR, "dataset", "images", "test")
    if not os.path.exists(test_images_dir):
        print(f"Test directory {test_images_dir} does not exist.")
        return

    test_images = glob.glob(os.path.join(test_images_dir, "*.jpg"))
    if not test_images:
        print("No images found in test directory.")
        return
        
    random_image = random.choice(test_images)
    count_objects_in_image(random_image)

if __name__ == "__main__":
    main()
