import requests

url = "http://127.0.0.1:8000/predict"
image_path = r"d:\ai\capp\dataset\images\train\20_jpg.rf.f52eea8697e265b18525616e4912f499.jpg"
files = {'file': ('test_image.jpg', open(image_path, 'rb'))}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
