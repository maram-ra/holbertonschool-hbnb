import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1Mzc0NTUwMSwianRpIjoiYTM3NjhiNGUtYmMyYy00OGM0LWI1ZmItYWViOWRjYjgwNGJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijc3ZWZjYWRhLTQ3NmItNDMxMi04YWY0LWRjZGU0ZWM5NmZlZCIsIm5iZiI6MTc1Mzc0NTUwMSwiY3NyZiI6ImRhZTYxYTY0LTBkMTQtNDIyNC1iMjgwLWUxYmQ5Y2IyYzY1MyIsImV4cCI6MTc1Mzc0NjQwMSwiaXNfYWRtaW4iOnRydWV9.a1G9x0Vm4GLDIe_Tz_G7YBvxOxvo32TaoetUuK-MpDc"

url = "http://127.0.0.1:5000/api/v1/amenities"

amenities = [
    {"name": "wifi"},
    {"name": "balcony"},
    {"name": "fireplace"},
    {"name": "parking"},
    {"name": "air_conditioning"}
]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

for a in amenities:
    res = requests.post(url, json=a, headers=headers)
    print("✅" if res.status_code == 201 else "❌", res.text)
