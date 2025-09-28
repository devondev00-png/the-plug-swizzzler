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
    TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts")  # Changed to gtts since pyttsx3 has issues
    TTS_VOICE = os.getenv("TTS_VOICE", "default")
    
    # Export Configuration
    EXPORT_DIR = os.getenv("EXPORT_DIR", "./exports")
    MAX_EXPORT_SIZE = int(os.getenv("MAX_EXPORT_SIZE", "10485760"))  # 10MB
    
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
    
    # Brand Voice Defaults
    DEFAULT_BRAND_VOICES = {
        "Dd style": {
            "description": "Meme-driven humor, confident, punchy phrasing",
            "style_guidelines": {
                "tone": "meme-driven, confident, punchy",
                "phrasing": "short, impactful, memorable",
                "references": "Solana, crypto, tech culture",
                "humor": "meme-native, tech-savvy",
                "approach": "no fluff, straight to value"
            }
        },
        "British professional": {
            "description": "Polished, courteous tone with clear enunciation",
            "style_guidelines": {
                "tone": "polished, courteous, professional",
                "phrasing": "clear, structured, articulate",
                "approach": "subtle persuasion, no hard sell",
                "manners": "polite, respectful, proper"
            }
        }
    }
    
    # Objection Templates
    DEFAULT_OBJECTION_TEMPLATES = [
        {
            "objection_type": "price",
            "objection_text": "It's too expensive",
            "response_template": "I understand cost is important. Let me show you the ROI - this typically pays for itself within [timeframe] by saving [hours] per week."
        },
        {
            "objection_type": "time",
            "objection_text": "I don't have time right now",
            "response_template": "I totally get that - everyone's busy. This actually saves time once implemented. Can we schedule just 15 minutes to show you how it works?"
        },
        {
            "objection_type": "competitor",
            "objection_text": "We're already using [competitor]",
            "response_template": "That's great! What I love about our solution is [unique differentiator]. Many of our clients switched from [competitor] because [benefit]. Want to see the difference?"
        },
        {
            "objection_type": "authority",
            "objection_text": "I need to check with my team/boss",
            "response_template": "Absolutely, that makes sense. What information would be most helpful for that conversation? I can prepare a summary of key benefits and ROI."
        },
        {
            "objection_type": "skepticism",
            "objection_text": "I've heard this before",
            "response_template": "I understand the skepticism - there are a lot of promises out there. What I can do is show you real results from similar companies. Would that help?"
        }
    ]
    
    # Script Generation Defaults
    SCRIPT_DEFAULTS = {
        "max_script_length": 2000,
        "min_script_length": 100,
        "default_script_type": "sales",
        "default_audience": "cold_lead",
        "default_tone": "professional",
        "default_format": "humanized",
        "default_brand_voice": "trained"
    }
    
    # Validation Rules
    VALIDATION_RULES = {
        "company_name": {
            "min_length": 2,
            "max_length": 100,
            "pattern": r"^[a-zA-Z0-9\s\-&.]+$"
        },
        "product_info": {
            "min_length": 10,
            "max_length": 1000
        },
        "training_data_content": {
            "min_length": 5,
            "max_length": 5000
        }
    }

# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are present"""
    required_settings = ["OPENAI_API_KEY"]
    missing_settings = []
    
    # Debug: Print all environment variables
    print("Debug: Environment variables:")
    for key, value in os.environ.items():
        if 'OPENAI' in key.upper() or 'SECRET' in key.upper():
            print(f"  {key}: {value[:10]}..." if value else f"  {key}: None")
    
    for setting in required_settings:
        value = getattr(settings, setting)
        print(f"Debug: {setting} = {value[:10] if value else 'None'}...")
        if not value:
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")
    
    return True

# Initialize settings validation
if __name__ == "__main__":
    try:
        validate_settings()
        print("✅ All settings validated successfully")
    except ValueError as e:
        print(f"❌ Settings validation failed: {e}")
        print("Please check your .env file and ensure all required settings are present.")
