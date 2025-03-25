import requests
url = "http://127.0.0.1:8000/analyze-transcript"
payload = {"transcript_id": "t_d004c097-424d-45d4-8f91-833d85c2da31"}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
