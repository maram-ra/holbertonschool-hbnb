import requests

base_url = "http://127.0.0.1:5000/api/v1"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1Mzc1NzExMCwianRpIjoiNTc5NTQyYjgtYmJlYi00NTMyLWIxNWMtMDNlZTVjYjU5ZDM0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijc3ZWZjYWRhLTQ3NmItNDMxMi04YWY0LWRjZGU0ZWM5NmZlZCIsIm5iZiI6MTc1Mzc1NzExMCwiY3NyZiI6ImJlZTIzNzQ1LWMwYzEtNGMzZS1iNWQzLTcwM2M2MDM0YmMzMyIsImV4cCI6MTc1Mzc1ODAxMCwiaXNfYWRtaW4iOnRydWV9.Gv6wUBChpnee6D2fFP9sHl36bD49yIu2cLwA1Y_fAiY"

url = f"{base_url}/places"

amenities = {
    "wifi": "2150a8e8-9747-4150-a7f5-faf4274b8bd1",
    "balcony": "8d99d35d-73a4-4bbc-967d-89cf6eaa5d47",
    "fireplace": "ebd15d2a-088a-46a6-b0a4-2f0dc9db465b",
    "parking": "8df9fc75-1fb4-4bb3-a705-5d2f59b29a76",
    "air_conditioning": "8ad090ea-78d8-44ab-afde-6ed94380ec7f",
}

places = [
    {
        "title": "Ocean View Cabin",
        "price": 120,
        "description": "Relaxing cabin with ocean view.",
        "latitude": 24.7136,
        "longitude": 46.6753,
        "owner_id": "77efcada-476b-4312-8af4-dcde4ec96fed",
        "amenities": [amenities["wifi"], amenities["balcony"]]
    },
    {
        "title": "Mountain Retreat",
        "price": 98,
        "description": "Cozy escape in the mountains.",
        "latitude": 36.7783,
        "longitude": -119.4179,
        "owner_id": "77efcada-476b-4312-8af4-dcde4ec96fed",
        "amenities": [amenities["fireplace"], amenities["parking"]]
    },
    {
        "title": "City Loft",
        "price": 150,
        "description": "Modern loft in the heart of the city.",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": "77efcada-476b-4312-8af4-dcde4ec96fed",
        "amenities": [amenities["wifi"], amenities["air_conditioning"]]
    }
]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

for place in places:
    print(f"🚀 Sending: {place}")
    response = requests.post(url, json=place, headers=headers)
    if response.status_code == 201:
        print(f"✅ Added: {place['title']}")
    else:
        print(f"❌ Failed to add: {place['title']}")
        print("Response:", response.text)
