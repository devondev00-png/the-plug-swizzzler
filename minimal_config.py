import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./call_scripts.db")
    
    # OpenAI Configuration
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.8"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1500"))
    
    # TTS Configuration
    TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts")
    TTS_VOICE = os.getenv("TTS_VOICE", "default")
    
    # Export Configuration
    EXPORT_DIR = os.getenv("EXPORT_DIR", "./exports")
    MAX_EXPORT_SIZE = int(os.getenv("MAX_EXPORT_SIZE", "10485760"))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
    
    # Feature Flags
    ENABLE_TTS = os.getenv("ENABLE_TTS", "True").lower() == "true"
    ENABLE_EXPORT = os.getenv("ENABLE_EXPORT", "True").lower() == "true"
    ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "False").lower() == "true"

# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are present"""
    required_settings = ["OPENAI_API_KEY"]
    missing_settings = []
    
    for setting in required_settings:
        value = getattr(settings, setting)
        if not value:
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")
    
    return True