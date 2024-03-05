# api.py

import requests
import openai
import logging

#opentripmap api
def fetch_places(lat, lon, radius=1000, kinds="interesting_places"):
    api_key = "5ae2e3f221c38a28845f05b65a7e1cdfbe3a4740c3cbdee55a380d62"  # Use your actual API key
    url = f"https://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={lon}&lat={lat}&kinds={kinds}&apikey={api_key}"
    response = requests.get(url)
    print("API Response:", response.json())  # Debug print
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
    
    
