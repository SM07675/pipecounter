import requests
import os

def test_api():
    url = "http://127.0.0.1:8000/predict"
    # Use the dummy image created by the previous script if available, or create one
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_test_image.jpg")
    
    if not os.path.exists(file_path):
        from PIL import Image
        img = Image.new('RGB', (640, 640), color = (73, 109, 137))
        img.save(file_path)

    try:
        print(f"Sending request to {url} with {file_path}...")
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
