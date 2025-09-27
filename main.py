from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import tempfile
import json

from database.database import get_db, create_tables, init_default_data
from schemas import (
    ScriptGenerationRequest, ScriptResponse, TrainingDataRequest, 
    BulkTrainingDataRequest, CompanyResponse, BrandVoiceResponse,
    TrainingDataResponse, ObjectionTemplateResponse, ScriptLibraryRequest,
    ScriptLibraryResponse
)
from services.script_service import ScriptService
from services.brand_voice_service import BrandVoiceService
from services.objection_service import ObjectionService
from services.tts_service import TTSService
from services.export_service import ExportService
from services.company_voice_service import CompanyVoiceService
from services.autocall_service import AutoCallService
from services.script_generator_service import ScriptGeneratorService

# Initialize FastAPI app
app = FastAPI(
    title="The Plug Swizzler",
    description="Generate personalized call scripts with custom training and memory system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
tts_service = TTSService()
export_service = ExportService()

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    init_default_data()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "The Plug Swizzler API",
        "version": "1.0.0",
        "description": "Generate personalized call scripts with custom training and memory system",
        "endpoints": {
            "generate_script": "/generate-script",
            "training_data": "/training-data",
            "objections": "/objections",
            "companies": "/companies",
            "scripts": "/scripts",
            "memory": "/memory",
            "auth": "/auth"
        }
    }

# Script Generation Endpoints (Legacy - for backward compatibility)
@app.post("/generate-script-legacy", response_model=ScriptResponse)
async def generate_script_legacy(
    request: ScriptGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate a new call script (legacy endpoint)"""
    try:
        script_service = ScriptService(db)
        result = script_service.generate_script(request.dict())
        return ScriptResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/scripts/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: int, db: Session = Depends(get_db)):
    """Get a specific script by ID"""
    script_service = ScriptService(db)
    script = script_service.get_script(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return ScriptResponse(**script)

@app.get("/scripts/company/{company_name}", response_model=List[ScriptResponse])
async def get_company_scripts(
    company_name: str, 
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all scripts for a company"""
    script_service = ScriptService(db)
    scripts = script_service.get_company_scripts(company_name, limit)
    return [ScriptResponse(**script) for script in scripts]

@app.post("/scripts/{script_id}/regenerate", response_model=ScriptResponse)
async def regenerate_script(
    script_id: int,
    modifications: dict,
    db: Session = Depends(get_db)
):
    """Regenerate a script with modifications"""
    try:
        script_service = ScriptService(db)
        result = script_service.regenerate_script(script_id, modifications)
        return ScriptResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Training Data Endpoints
@app.post("/training-data", response_model=TrainingDataResponse)
async def add_training_data(
    request: TrainingDataRequest,
    db: Session = Depends(get_db)
):
    """Add training data for a company"""
    try:
        brand_voice_service = BrandVoiceService(db)
        
        # Get or create company
        from database.models import Company
        company = db.query(Company).filter(Company.name == request.company_name).first()
        if not company:
            company = Company(name=request.company_name)
            db.add(company)
            db.commit()
        
        # Add training data
        from database.models import TrainingData
        training_data = TrainingData(
            company_id=company.id,
            data_type=request.data_type,
            content=request.content,
            metadata=request.metadata or {}
        )
        
        db.add(training_data)
        db.commit()
        
        return TrainingDataResponse(
            id=training_data.id,
            data_type=training_data.data_type,
            content=training_data.content,
            metadata=training_data.metadata,
            created_at=training_data.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/training-data/bulk", response_model=List[TrainingDataResponse])
async def add_bulk_training_data(
    request: BulkTrainingDataRequest,
    db: Session = Depends(get_db)
):
    """Add multiple training data entries"""
    try:
        from database.models import Company, TrainingData
        
        # Get or create company
        company = db.query(Company).filter(Company.name == request.company_name).first()
        if not company:
            company = Company(name=request.company_name)
            db.add(company)
            db.commit()
        
        results = []
        for data in request.training_data:
            training_data = TrainingData(
                company_id=company.id,
                data_type=data.data_type,
                content=data.content,
                metadata=data.metadata or {}
            )
            db.add(training_data)
            results.append(training_data)
        
        db.commit()
        
        return [
            TrainingDataResponse(
                id=td.id,
                data_type=td.data_type,
                content=td.content,
                metadata=td.metadata,
                created_at=td.created_at
            ) for td in results
        ]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/training-data/{company_name}", response_model=List[TrainingDataResponse])
async def get_training_data(company_name: str, db: Session = Depends(get_db)):
    """Get all training data for a company"""
    brand_voice_service = BrandVoiceService(db)
    training_data = brand_voice_service.get_company_training_data(company_name)
    return [TrainingDataResponse(**data) for data in training_data]

# Objection Handling Endpoints
@app.get("/objections", response_model=List[ObjectionTemplateResponse])
async def get_objection_templates(
    company_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get objection handling templates"""
    objection_service = ObjectionService(db)
    templates = objection_service.get_objection_templates(company_name)
    return [ObjectionTemplateResponse(**template) for template in templates]

@app.post("/objections", response_model=ObjectionTemplateResponse)
async def create_objection_template(
    objection_type: str = Form(...),
    objection_text: str = Form(...),
    response_template: str = Form(...),
    company_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new objection template"""
    try:
        objection_service = ObjectionService(db)
        template = objection_service.create_objection_template(
            objection_type, objection_text, response_template, company_name
        )
        return ObjectionTemplateResponse(
            id=template.id,
            objection_type=template.objection_type,
            objection_text=template.objection_text,
            response_template=template.response_template,
            is_default=template.is_default
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/objections/generate/{objection_type}")
async def generate_objection_responses(
    objection_type: str,
    context: str = "",
    brand_voice: str = "default",
    db: Session = Depends(get_db)
):
    """Generate AI-powered objection responses"""
    try:
        objection_service = ObjectionService(db)
        responses = objection_service.generate_objection_responses(
            objection_type, context, brand_voice
        )
        return {"objection_type": objection_type, "responses": responses}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Company Management Endpoints
@app.get("/companies", response_model=List[CompanyResponse])
async def get_companies(db: Session = Depends(get_db)):
    """Get all companies"""
    from database.models import Company
    companies = db.query(Company).all()
    return [CompanyResponse(id=c.id, name=c.name, created_at=c.created_at) for c in companies]

# Brand Voice Endpoints
@app.get("/brand-voices", response_model=List[BrandVoiceResponse])
async def get_brand_voices(db: Session = Depends(get_db)):
    """Get all brand voices"""
    from database.models import BrandVoice
    voices = db.query(BrandVoice).all()
    return [
        BrandVoiceResponse(
            id=v.id,
            name=v.name,
            voice_type=v.voice_type,
            description=v.description,
            training_prompts=v.training_prompts
        ) for v in voices
    ]

# TTS Endpoints
@app.post("/scripts/{script_id}/audio")
async def generate_audio(
    script_id: int,
    voice: str = "default",
    db: Session = Depends(get_db)
):
    """Generate audio from script"""
    try:
        script_service = ScriptService(db)
        script = script_service.get_script(script_id)
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
        
        audio_data = tts_service.text_to_speech(script["script"], voice=voice)
        if not audio_data:
            raise HTTPException(status_code=500, detail="Audio generation failed")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name
        
        return FileResponse(
            temp_path,
            media_type="audio/mpeg",
            filename=f"script_{script_id}_audio.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/voices")
async def get_available_voices():
    """Get available TTS voices"""
    voices = tts_service.get_available_voices()
    return {"voices": voices}

# Export Endpoints
@app.get("/scripts/{script_id}/export/{format}")
async def export_script(
    script_id: int,
    format: str,
    db: Session = Depends(get_db)
):
    """Export script in various formats"""
    try:
        script_service = ScriptService(db)
        script = script_service.get_script(script_id)
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
        
        # Add company name to script data
        from database.models import Company
        company = db.query(Company).filter(Company.id == script["company_id"]).first()
        script["company_name"] = company.name if company else "Unknown"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as temp_file:
            temp_path = temp_file.name
        
        success = False
        if format == "pdf":
            success = export_service.export_to_pdf(script, temp_path)
        elif format == "txt":
            success = export_service.export_to_txt(script, temp_path)
        elif format == "json":
            success = export_service.export_to_json(script, temp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        if not success:
            raise HTTPException(status_code=500, detail="Export failed")
        
        media_type = {
            "pdf": "application/pdf",
            "txt": "text/plain",
            "json": "application/json"
        }.get(format, "application/octet-stream")
        
        return FileResponse(
            temp_path,
            media_type=media_type,
            filename=f"script_{script_id}.{format}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Script Generation Endpoints
@app.get("/company-voices")
async def get_company_voices(db: Session = Depends(get_db)):
    """Get all professional company voice templates"""
    company_voice_service = CompanyVoiceService(db)
    script_generator = ScriptGeneratorService(db, company_voice_service)
    voices = script_generator.get_available_voices("autocall")
    return {"voices": voices}

@app.get("/humanized-voices")
async def get_humanized_voices(db: Session = Depends(get_db)):
    """Get all humanized voice options"""
    company_voice_service = CompanyVoiceService(db)
    script_generator = ScriptGeneratorService(db, company_voice_service)
    voices = script_generator.get_humanized_voices()
    return {"voices": voices}

@app.get("/humanized-voices/accent/{accent}")
async def get_voices_by_accent(accent: str, db: Session = Depends(get_db)):
    """Get humanized voices by accent"""
    company_voice_service = CompanyVoiceService(db)
    script_generator = ScriptGeneratorService(db, company_voice_service)
    voices = script_generator.get_voices_by_accent(accent)
    return {"voices": voices}

@app.get("/humanized-voices/gender/{gender}")
async def get_voices_by_gender(gender: str, db: Session = Depends(get_db)):
    """Get humanized voices by gender"""
    company_voice_service = CompanyVoiceService(db)
    script_generator = ScriptGeneratorService(db, company_voice_service)
    voices = script_generator.get_voices_by_gender(gender)
    return {"voices": voices}

@app.get("/humanized-voices/accents")
async def get_available_accents(db: Session = Depends(get_db)):
    """Get available accents"""
    company_voice_service = CompanyVoiceService(db)
    script_generator = ScriptGeneratorService(db, company_voice_service)
    accents = script_generator.get_available_accents()
    return {"accents": accents}

@app.get("/humanized-voices/genders")
async def get_available_genders(db: Session = Depends(get_db)):
    """Get available genders"""
    company_voice_service = CompanyVoiceService(db)
    script_generator = ScriptGeneratorService(db, company_voice_service)
    genders = script_generator.get_available_genders()
    return {"genders": genders}

@app.get("/company-voices/{voice_id}")
async def get_company_voice(voice_id: str, db: Session = Depends(get_db)):
    """Get specific company voice template"""
    company_voice_service = CompanyVoiceService(db)
    voice = company_voice_service.get_voice_template(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice template not found")
    return voice

@app.get("/interactive-elements")
async def get_interactive_elements(db: Session = Depends(get_db)):
    """Get common interactive elements for auto-call scripts"""
    company_voice_service = CompanyVoiceService(db)
    elements = company_voice_service.get_common_interactive_elements()
    return {"elements": elements}

@app.post("/generate-script")
async def generate_script(
    script_type: str = Form(...),  # "autocall", "humanized", or "both"
    voice_id: str = Form(None),  # For auto-call scripts
    humanized_voice_id: str = Form(None),  # For humanized scripts
    call_type: str = Form(...),  # "inbound" or "outbound"
    script_mode: str = Form(...),  # "banking", "payment", "tech_support", etc.
    product_info: str = Form(...),
    negative_prompts: str = Form(""),  # What to avoid in the script
    interactive_elements: str = Form(None),  # JSON string, optional for humanized
    db: Session = Depends(get_db)
):
    """Generate script for auto-call bot or humanized calling"""
    try:
        company_voice_service = CompanyVoiceService(db)
        script_generator = ScriptGeneratorService(db, company_voice_service)
        
        # Parse interactive elements if provided
        elements = None
        if interactive_elements:
            elements = json.loads(interactive_elements)
        
        # Generate script(s)
        if script_type == "both":
            # Generate both auto-call and humanized scripts with connection
            autocall_result = script_generator.generate_script(
                script_type="autocall",
                voice_id=voice_id,
                call_type=call_type,
                script_mode=script_mode,
                product_info=product_info,
                negative_prompts=negative_prompts,
                interactive_elements=elements
            )
            
            # Generate connected humanized script that follows up the auto-call
            humanized_result = script_generator.generate_connected_humanized_script(
                autocall_script=autocall_result,
                voice_id=humanized_voice_id or voice_id,
                call_type=call_type,
                script_mode=script_mode,
                product_info=product_info,
                negative_prompts=negative_prompts
            )
            
            return {
                "autocall_script": autocall_result,
                "humanized_script": humanized_result,
                "script_type": "both"
            }
        else:
            # Generate single script
            result = script_generator.generate_script(
                script_type=script_type,
                voice_id=voice_id or humanized_voice_id,
                call_type=call_type,
                script_mode=script_mode,
                product_info=product_info,
                negative_prompts=negative_prompts,
                interactive_elements=elements
            )
            
            return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/autocall-script/{script_id}/export/{format}")
async def export_autocall_script(
    script_id: str,
    format: str,
    db: Session = Depends(get_db)
):
    """Export auto-call script in various formats"""
    try:
        # This would retrieve the script from database
        # For now, return a sample
        sample_script = {
            "voice_template": {"id": "natwest", "name": "NatWest Bank"},
            "autocall_format": {
                "script_id": script_id,
                "voice_settings": {"voice_id": "natwest"},
                "call_flow": {"opening": {"type": "speech"}},
                "interactive_elements": [],
                "audio_segments": []
            }
        }
        
        company_voice_service = CompanyVoiceService(db)
        autocall_service = AutoCallService(db, company_voice_service)
        
        exported = autocall_service.export_for_autocall_bot(sample_script, format)
        
        return {"format": format, "content": exported}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
