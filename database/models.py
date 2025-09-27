from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    user_id = Column(String(255), index=True)  # Link to your main app user
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scripts = relationship("Script", back_populates="company")
    training_data = relationship("TrainingData", back_populates="company")
    brand_voices = relationship("BrandVoice", back_populates="company")
    memory_data = relationship("MemoryData", back_populates="company")

class BrandVoice(Base):
    __tablename__ = "brand_voices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    voice_type = Column(String(50))  # "trained", "Dd style", "British professional"
    description = Column(Text)
    training_prompts = Column(JSON)  # Store voice-specific prompts
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="brand_voices")
    scripts = relationship("Script", back_populates="brand_voice")

class CompanyVoice(Base):
    __tablename__ = "company_voices"
    
    id = Column(Integer, primary_key=True, index=True)
    voice_id = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    tone = Column(String(50))
    style = Column(String(50))
    phrases = Column(JSON)  # Store common phrases
    objection_handling = Column(JSON)  # Store objection responses
    created_at = Column(DateTime, default=datetime.utcnow)

class TrainingData(Base):
    __tablename__ = "training_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    data_type = Column(String(50))  # "custom_info", "brand_voice", "style_guide", "other"
    content = Column(Text)
    meta_data = Column(JSON)  # Store tags, sentiment, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="training_data")

class MemoryData(Base):
    __tablename__ = "memory_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    memory_type = Column(String(50))  # "script_preference", "brand_style", "objection_handling", "custom"
    memory_key = Column(String(255))  # Key to identify the memory
    memory_value = Column(Text)  # The actual memory content
    meta_data = Column(JSON)  # Additional context
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="memory_data")

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)  # Your main app user ID
    session_token = Column(String(255), unique=True, index=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Script(Base):
    __tablename__ = "scripts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    brand_voice_id = Column(Integer, ForeignKey("brand_voices.id"))
    script_type = Column(String(50))  # "sales", "support", "follow-up"
    audience = Column(String(50))  # "cold_lead", "existing_customer"
    tone = Column(String(50))  # "funny", "friendly", "aggressive", "formal"
    product_info = Column(Text)
    format_type = Column(String(20))  # "humanized", "automated"
    handle_objections = Column(Boolean, default=False)
    use_training_data = Column(Boolean, default=False)
    generated_script = Column(Text)
    meta_data = Column(JSON)  # Store additional parameters
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="scripts")
    brand_voice = relationship("BrandVoice", back_populates="scripts")

class ObjectionTemplate(Base):
    __tablename__ = "objection_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    objection_type = Column(String(100))
    objection_text = Column(Text)
    response_template = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    is_default = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScriptLibrary(Base):
    __tablename__ = "script_library"
    
    id = Column(Integer, primary_key=True, index=True)
    script_id = Column(Integer, ForeignKey("scripts.id"))
    title = Column(String(255))
    tags = Column(JSON)  # Array of tags for categorization
    is_favorite = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    script = relationship("Script")
