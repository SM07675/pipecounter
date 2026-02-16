from ultralytics import YOLO

def continue_training():
    # Load the partially trained model
    # We use 'last.pt' to resume from the most recent state
    model = YOLO("d:/ai/capp/runs/object_counter3/weights/last.pt")

    # Determine device: use GPU if available, else CPU
    import torch
    device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Resume training
    # resume=True will automatically load the training arguments from the checkpoint
    # We explicitly pass device just to be sure, though resume might override it.
    try:
        results = model.train(resume=True, device=device)
    except Exception as e:
        if "finished" in str(e) or "nothing to resume" in str(e):
            print("Training was already completed (reached max epochs). Proceeding to export...")
        else:
            raise e
    
    # Export again just to be sure we have the final version if it finishes
    try:
        print("Attempting export to TensorFlow SavedModel format...")
        model.export(format="saved_model")
    except Exception as e:
        print(f"SavedModel export failed: {e}")
        print("Falling back to ONNX export (no extra dependencies required)...")
        try:
            model.export(format="onnx")
            print("ONNX export successful!")
        except Exception as e_onnx:
            print(f"ONNX export also failed: {e_onnx}")

if __name__ == "__main__":
    continue_training()
