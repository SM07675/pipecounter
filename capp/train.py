from ultralytics import YOLO

def train_model():
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    import torch
    device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    results = model.train(
        data="d:/ai/capp/dataset/data.yaml", 
        epochs=5, 
        imgsz=640,
        project="d:/ai/capp/runs",
        name="object_counter",
        device=device
    )
    
    # Export the model
    success = model.export(format="saved_model")
    print("Training finished.")

if __name__ == "__main__":
    train_model()
