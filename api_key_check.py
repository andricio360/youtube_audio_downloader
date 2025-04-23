from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in the .env file.")


def check_api_key_valid():
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.videos().list(part="snippet", id="dQw4w9WgXcQ")
        response = request.execute()
        print("✅ API key is valid.")
        print("Video title:", response["items"][0]["snippet"]["title"])
    except Exception as e:
        print("❌ API key is invalid or there's another issue.")
        print(e)


check_api_key_valid()
