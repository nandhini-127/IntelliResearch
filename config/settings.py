
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Gemini configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Tavily configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))




def get_llm():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing in .env")

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        max_retries=5,
        timeout=60
    )

