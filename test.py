
from dotenv import load_dotenv
import os

load_dotenv()  # make sure .env is loaded
print("Loaded Gemini API Key:", os.getenv("GEMINI_API_KEY"))
