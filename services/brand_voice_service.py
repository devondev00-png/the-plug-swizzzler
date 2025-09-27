from typing import Dict, List, Any, Optional
from database.models import BrandVoice, Company, TrainingData
from sqlalchemy.orm import Session
import json

class BrandVoiceService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_brand_voice_prompts(self, brand_voice_type: str, company_name: str = None) -> Dict[str, Any]:
        """Get brand voice specific prompts and training data"""
        
        if brand_voice_type == "trained" and company_name:
            return self._get_trained_voice_data(company_name)
        elif brand_voice_type == "Dd style":
            return self._get_dd_style_prompts()
        elif brand_voice_type == "British professional":
            return self._get_british_professional_prompts()
        else:
            return self._get_default_prompts()
    
    def _get_trained_voice_data(self, company_name: str) -> Dict[str, Any]:
        """Get training data for custom brand voice"""
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            return self._get_default_prompts()
        
        # Get training data
        training_data = self.db.query(TrainingData).filter(
            TrainingData.company_id == company.id
        ).all()
        
        # Get brand voice if exists
        brand_voice = self.db.query(BrandVoice).filter(
            BrandVoice.company_id == company.id,
            BrandVoice.voice_type == "trained"
        ).first()
        
        tweets = [td for td in training_data if td.data_type == "tweet"]
        call_logs = [td for td in training_data if td.data_type == "call_log"]
        
        return {
            "voice_type": "trained",
            "company_name": company_name,
            "tweets": [{"content": t.content, "metadata": t.metadata} for t in tweets],
            "call_logs": [{"content": c.content, "metadata": c.metadata} for c in call_logs],
            "custom_prompts": brand_voice.training_prompts if brand_voice else {},
            "style_guidelines": self._extract_style_guidelines(tweets, call_logs)
        }
    
    def _get_dd_style_prompts(self) -> Dict[str, Any]:
        """Get Dd style brand voice prompts"""
        return {
            "voice_type": "Dd style",
            "style_guidelines": {
                "tone": "meme-driven, confident, punchy",
                "phrasing": "short, impactful, memorable",
                "references": "Solana, crypto, tech culture",
                "humor": "meme-native, tech-savvy",
                "approach": "no fluff, straight to value"
            },
            "sample_phrases": [
                "We built this like it's a Solana validator — fast, lean, no downtime",
                "If you're still using Excel, blink twice. We're sending help",
                "This isn't your grandma's CRM",
                "ROI in week one, guaranteed",
                "We're not here to waste your time"
            ],
            "objection_style": "confident, tech-savvy responses with humor"
        }
    
    def _get_british_professional_prompts(self) -> Dict[str, Any]:
        """Get British professional brand voice prompts"""
        return {
            "voice_type": "British professional",
            "style_guidelines": {
                "tone": "polished, courteous, professional",
                "phrasing": "clear, structured, articulate",
                "approach": "subtle persuasion, no hard sell",
                "manners": "polite, respectful, proper"
            },
            "sample_phrases": [
                "I do hope you'll find this rather useful",
                "If I may, I'd like to show you something quite remarkable",
                "I understand your concerns, and I do appreciate you taking the time",
                "This has proven rather effective for similar companies",
                "I do believe this could be of genuine benefit to your team"
            ],
            "objection_style": "polite, structured responses with clear benefits"
        }
    
    def _get_default_prompts(self) -> Dict[str, Any]:
        """Get default brand voice prompts"""
        return {
            "voice_type": "default",
            "style_guidelines": {
                "tone": "professional, friendly",
                "phrasing": "clear, conversational",
                "approach": "value-focused, consultative"
            }
        }
    
    def _extract_style_guidelines(self, tweets: List, call_logs: List) -> Dict[str, Any]:
        """Extract style guidelines from training data"""
        guidelines = {
            "common_phrases": [],
            "tone_indicators": [],
            "objection_handling": [],
            "humor_style": [],
            "tech_references": []
        }
        
        # Analyze tweets for style patterns
        for tweet in tweets:
            content = tweet.content.lower()
            if any(word in content for word in ["meme", "crypto", "solana", "tech"]):
                guidelines["tech_references"].append(tweet.content)
            if any(word in content for word in ["lol", "haha", "funny", "joke"]):
                guidelines["humor_style"].append(tweet.content)
        
        # Analyze call logs for objection handling
        for call_log in call_logs:
            content = call_log.content.lower()
            if any(word in content for word in ["objection", "concern", "problem"]):
                guidelines["objection_handling"].append(call_log.content)
        
        return guidelines
    
    def create_custom_brand_voice(self, 
                                 company_name: str,
                                 voice_name: str,
                                 description: str,
                                 training_prompts: Dict[str, Any]) -> BrandVoice:
        """Create a custom brand voice for a company"""
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            company = Company(name=company_name)
            self.db.add(company)
            self.db.commit()
        
        brand_voice = BrandVoice(
            name=voice_name,
            company_id=company.id,
            voice_type="trained",
            description=description,
            training_prompts=training_prompts
        )
        
        self.db.add(brand_voice)
        self.db.commit()
        return brand_voice
    
    def get_company_training_data(self, company_name: str) -> List[Dict[str, Any]]:
        """Get all training data for a company"""
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            return []
        
        training_data = self.db.query(TrainingData).filter(
            TrainingData.company_id == company.id
        ).all()
        
        return [
            {
                "id": td.id,
                "data_type": td.data_type,
                "content": td.content,
                "metadata": td.metadata,
                "created_at": td.created_at
            }
            for td in training_data
        ]
