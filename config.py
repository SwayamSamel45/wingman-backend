import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Gemini Model (flash is faster & cheaper, pro is more capable)
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # CORS Origins (add your app domains)
    CORS_ORIGINS: list = [
        "*",  # Allow all for development - restrict in production
    ]

settings = Settings()
