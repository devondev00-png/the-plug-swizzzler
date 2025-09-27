from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ScriptType(str, Enum):
    SALES = "sales"
    SUPPORT = "support"
    FOLLOW_UP = "follow-up"
    COLD_CALL = "cold_call"
    WARM_UP = "warm_up"

class Audience(str, Enum):
    COLD_LEAD = "cold_lead"
    EXISTING_CUSTOMER = "existing_customer"
    HOT_LEAD = "hot_lead"
    RETURNING_CUSTOMER = "returning_customer"

class Tone(str, Enum):
    FUNNY = "funny"
    FRIENDLY = "friendly"
    AGGRESSIVE = "aggressive"
    FORMAL = "formal"
    CASUAL = "casual"
    PROFESSIONAL = "professional"

class FormatType(str, Enum):
    HUMANIZED = "humanized"
    AUTOMATED = "automated"

class BrandVoiceType(str, Enum):
    TRAINED = "trained"
    DD_STYLE = "Dd style"
    BRITISH_PROFESSIONAL = "British professional"

class ScriptGenerationRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    script_type: ScriptType = Field(..., description="Type of call script")
    audience: Audience = Field(..., description="Target audience")
    tone: Tone = Field(..., description="Tone of the script")
    product_info: str = Field(..., description="Information about the product/service")
    format: FormatType = Field(..., description="Script format")
    brand_voice: BrandVoiceType = Field(..., description="Brand voice to use")
    handle_objections: bool = Field(False, description="Include objection handling")
    use_training_data: bool = Field(False, description="Use uploaded training data")
    custom_prompts: Optional[Dict[str, Any]] = Field(None, description="Custom prompts for generation")

class TrainingDataRequest(BaseModel):
    company_name: str
    data_type: str = Field(..., description="Type of training data: tweet, call_log, email, other")
    content: str = Field(..., description="The actual content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata like tags, sentiment")

class BulkTrainingDataRequest(BaseModel):
    company_name: str
    training_data: List[TrainingDataRequest]

class ScriptResponse(BaseModel):
    id: int
    script: str
    metadata: Dict[str, Any]
    created_at: datetime

class CompanyResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

class BrandVoiceResponse(BaseModel):
    id: int
    name: str
    voice_type: str
    description: str
    training_prompts: Dict[str, Any]

class TrainingDataResponse(BaseModel):
    id: int
    data_type: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime

class ObjectionTemplateResponse(BaseModel):
    id: int
    objection_type: str
    objection_text: str
    response_template: str
    is_default: bool

class ScriptLibraryRequest(BaseModel):
    script_id: int
    title: str
    tags: Optional[List[str]] = None
    is_favorite: bool = False

class ScriptLibraryResponse(BaseModel):
    id: int
    title: str
    tags: List[str]
    is_favorite: bool
    usage_count: int
    created_at: datetime
    script: ScriptResponse
