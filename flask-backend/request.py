import requests

url = 'http://127.0.0.1:5000/predict_api'
r = requests.post(url,json={'generate':'test'})
print(r.json())