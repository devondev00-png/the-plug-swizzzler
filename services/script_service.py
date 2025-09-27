from typing import Dict, List, Any, Optional
from database.models import Script, Company, BrandVoice, TrainingData
from sqlalchemy.orm import Session
from services.openai_service import OpenAIService
from services.brand_voice_service import BrandVoiceService
from services.objection_service import ObjectionService
from datetime import datetime
import json

class ScriptService:
    def __init__(self, db: Session):
        self.db = db
        self.openai_service = OpenAIService()
        self.brand_voice_service = BrandVoiceService(db)
        self.objection_service = ObjectionService(db)
    
    def generate_script(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete call script"""
        try:
            # Get or create company
            company = self._get_or_create_company(request_data["company_name"])
            
            # Get brand voice data
            brand_voice_data = self.brand_voice_service.get_brand_voice_prompts(
                request_data["brand_voice"], 
                request_data["company_name"]
            )
            
            # Get training data if requested
            training_data = []
            if request_data.get("use_training_data", False):
                training_data = self.brand_voice_service.get_company_training_data(
                    request_data["company_name"]
                )
            
            # Get objection templates if needed
            objection_templates = []
            if request_data.get("handle_objections", False):
                objection_templates = self.objection_service.get_objection_templates(
                    request_data["company_name"]
                )
            
            # Generate the script using OpenAI
            generated_script = self.openai_service.generate_script(
                company_name=request_data["company_name"],
                script_type=request_data["script_type"],
                audience=request_data["audience"],
                tone=request_data["tone"],
                product_info=request_data["product_info"],
                format_type=request_data["format"],
                brand_voice=request_data["brand_voice"],
                handle_objections=request_data.get("handle_objections", False),
                training_data=training_data,
                custom_prompts=request_data.get("custom_prompts")
            )
            
            # Get or create brand voice record
            brand_voice = self._get_or_create_brand_voice(
                company.id, 
                request_data["brand_voice"],
                brand_voice_data
            )
            
            # Save script to database
            script = Script(
                company_id=company.id,
                brand_voice_id=brand_voice.id if brand_voice else None,
                script_type=request_data["script_type"],
                audience=request_data["audience"],
                tone=request_data["tone"],
                product_info=request_data["product_info"],
                format_type=request_data["format"],
                handle_objections=request_data.get("handle_objections", False),
                use_training_data=request_data.get("use_training_data", False),
                generated_script=generated_script,
                metadata={
                    "brand_voice_data": brand_voice_data,
                    "objection_templates": objection_templates,
                    "training_data_count": len(training_data),
                    "generation_timestamp": datetime.utcnow().isoformat()
                }
            )
            
            self.db.add(script)
            self.db.commit()
            
            return {
                "id": script.id,
                "script": generated_script,
                "metadata": script.metadata,
                "created_at": script.created_at
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Script generation failed: {str(e)}")
    
    def get_script(self, script_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific script by ID"""
        script = self.db.query(Script).filter(Script.id == script_id).first()
        if not script:
            return None
        
        return {
            "id": script.id,
            "script": script.generated_script,
            "metadata": script.metadata,
            "created_at": script.created_at,
            "company_name": script.company.name,
            "script_type": script.script_type,
            "audience": script.audience,
            "tone": script.tone
        }
    
    def get_company_scripts(self, company_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all scripts for a company"""
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            return []
        
        scripts = self.db.query(Script).filter(
            Script.company_id == company.id
        ).order_by(Script.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": script.id,
                "script": script.generated_script,
                "metadata": script.metadata,
                "created_at": script.created_at,
                "script_type": script.script_type,
                "audience": script.audience,
                "tone": script.tone
            }
            for script in scripts
        ]
    
    def regenerate_script(self, script_id: int, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """Regenerate a script with modifications"""
        original_script = self.db.query(Script).filter(Script.id == script_id).first()
        if not original_script:
            raise Exception("Script not found")
        
        # Update parameters with modifications
        updated_params = {
            "company_name": original_script.company.name,
            "script_type": modifications.get("script_type", original_script.script_type),
            "audience": modifications.get("audience", original_script.audience),
            "tone": modifications.get("tone", original_script.tone),
            "product_info": modifications.get("product_info", original_script.product_info),
            "format": modifications.get("format", original_script.format_type),
            "brand_voice": modifications.get("brand_voice", "default"),
            "handle_objections": modifications.get("handle_objections", original_script.handle_objections),
            "use_training_data": modifications.get("use_training_data", original_script.use_training_data),
            "custom_prompts": modifications.get("custom_prompts")
        }
        
        # Generate new script
        return self.generate_script(updated_params)
    
    def _get_or_create_company(self, company_name: str) -> Company:
        """Get existing company or create new one"""
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            company = Company(name=company_name)
            self.db.add(company)
            self.db.commit()
        return company
    
    def _get_or_create_brand_voice(self, company_id: int, voice_type: str, voice_data: Dict) -> Optional[BrandVoice]:
        """Get existing brand voice or create new one"""
        if voice_type == "trained":
            brand_voice = self.db.query(BrandVoice).filter(
                BrandVoice.company_id == company_id,
                BrandVoice.voice_type == "trained"
            ).first()
            
            if not brand_voice:
                brand_voice = BrandVoice(
                    name=f"Trained Voice for Company {company_id}",
                    company_id=company_id,
                    voice_type="trained",
                    description="AI-trained brand voice",
                    training_prompts=voice_data
                )
                self.db.add(brand_voice)
                self.db.commit()
            
            return brand_voice
        
        return None
    
    def analyze_script_performance(self, script_id: int) -> Dict[str, Any]:
        """Analyze script performance (placeholder for future analytics)"""
        script = self.db.query(Script).filter(Script.id == script_id).first()
        if not script:
            return {}
        
        # This would analyze actual performance data
        # For now, return basic analysis
        return {
            "script_length": len(script.generated_script.split()),
            "objection_handling": script.handle_objections,
            "training_data_used": script.use_training_data,
            "brand_voice": script.brand_voice.name if script.brand_voice else "default",
            "generation_time": script.created_at.isoformat()
        }
