import os
import requests
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

def get_apod(date=None):
    """
    Fetch NASA Astronomy Picture of the Day
    """
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
