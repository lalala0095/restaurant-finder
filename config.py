from google import genai
from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=api_key)

foursquare_api_key = os.getenv("FOURSQUARE_API_KEY")

