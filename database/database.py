from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./call_scripts.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_default_data():
    """Initialize default objection templates and brand voices"""
    db = SessionLocal()
    try:
        from .models import ObjectionTemplate, BrandVoice, Company
        
        # Check if data already exists
        if db.query(ObjectionTemplate).count() == 0:
            # Add default objection templates
            default_objections = [
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
            
            for obj in default_objections:
                objection = ObjectionTemplate(**obj)
                db.add(objection)
        
        # Add default brand voices
        if db.query(BrandVoice).count() == 0:
            default_voices = [
                {
                    "name": "Dd Style",
                    "voice_type": "Dd style",
                    "description": "Meme-driven humor, confident, punchy phrasing, Solana-native tech references",
                    "training_prompts": {
                        "style": "meme-driven, confident, punchy",
                        "tone": "tech-native, no fluff, straight to value",
                        "references": "Solana, crypto, tech culture",
                        "phrasing": "short, impactful, memorable"
                    }
                },
                {
                    "name": "British Professional",
                    "voice_type": "British professional", 
                    "description": "Polished, courteous tone with clear enunciation and structure",
                    "training_prompts": {
                        "style": "polished, courteous, professional",
                        "tone": "subtle persuasion, no hard sell",
                        "phrasing": "clear, structured, articulate"
                    }
                }
            ]
            
            for voice in default_voices:
                brand_voice = BrandVoice(**voice)
                db.add(brand_voice)
        
        db.commit()
        print("Default data initialized successfully")
        
    except Exception as e:
        print(f"Error initializing default data: {e}")
        db.rollback()
    finally:
        db.close()
