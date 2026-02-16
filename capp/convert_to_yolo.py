import os
import pandas as pd
import shutil
import yaml

# Configuration
SOURCE_DIR = r"d:/ai/capp/object counter.v2i.tensorflow"
DEST_DIR = r"d:/ai/capp/dataset"
SETS = ['train', 'valid', 'test']

def convert_to_yolo(row):
    # YOLO format: class x_center y_center width height (normalized)
    img_width = row['width']
    img_height = row['height']
    
    xmin = row['xmin']
    ymin = row['ymin']
    xmax = row['xmax']
    ymax = row['ymax']
    
    # Box dimensions
    box_width = xmax - xmin
    box_height = ymax - ymin
    
    # Box center
    x_center = xmin + (box_width / 2)
    y_center = ymin + (box_height / 2)
    
    # Normalize
    x_center /= img_width
    y_center /= img_height
    box_width /= img_width
    box_height /= img_height
    
    return f"{row['class']} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"

def process_set(set_name):
    print(f"Processing {set_name} set...")
    csv_path = os.path.join(SOURCE_DIR, set_name, "_annotations.csv")
    
    if not os.path.exists(csv_path):
        print(f"Skipping {set_name}, annotation file not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # Create directories
    images_dir = os.path.join(DEST_DIR, "images", set_name)
    labels_dir = os.path.join(DEST_DIR, "labels", set_name)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    # Get unique classes if not already known (assuming consistent across sets, but let's just use what's there)
    # Ideally we scan all first, but for now we'll collect them dynamically or assume 0 based on previous view
    
    for filename, group in df.groupby('filename'):
        # Copy image
        src_img_path = os.path.join(SOURCE_DIR, set_name, filename)
        dst_img_path = os.path.join(images_dir, filename)
        
        if os.path.exists(src_img_path):
            shutil.copy2(src_img_path, dst_img_path)
            
            # Create label file
            label_filename = os.path.splitext(filename)[0] + ".txt"
            label_path = os.path.join(labels_dir, label_filename)
            
            with open(label_path, "w") as f:
                for _, row in group.iterrows():
                    yolo_line = convert_to_yolo(row)
                    f.write(yolo_line + "\n")
        else:
            print(f"Warning: Image not found {src_img_path}")

def create_yaml():
    yaml_content = {
        'path': DEST_DIR,
        'train': 'images/train',
        'val': 'images/valid',
        'test': 'images/test',
        'nc': 1, # Assuming 1 class based on previous check, will verify
        'names': ['object'] # Generic name, update if we find real names
    }
    
    # Check classes
    # Quick scan of train csv to find class ID max
    classes = set()
    train_csv = os.path.join(SOURCE_DIR, 'train', "_annotations.csv")
    if os.path.exists(train_csv):
        df = pd.read_csv(train_csv)
        classes = set(df['class'].unique())
    
    yaml_content['nc'] = len(classes)
    # If we knew the mapping we would put names here. For now 'object' or 'class_0' etc.
    yaml_content['names'] = [f"class_{i}" for i in sorted(list(classes))]
    
    with open(os.path.join(DEST_DIR, "data.yaml"), "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)
    print(f"Created data.yaml with classes: {yaml_content['names']}")

if __name__ == "__main__":
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    
    for set_name in SETS:
        process_set(set_name)
    
    create_yaml()
    print("Conversion complete.")
