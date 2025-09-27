from typing import List, Dict, Any, Optional
from database.models import ObjectionTemplate, Company
from sqlalchemy.orm import Session
from services.openai_service import OpenAIService

class ObjectionService:
    def __init__(self, db: Session):
        self.db = db
        self.openai_service = OpenAIService()
    
    def get_objection_templates(self, company_name: str = None) -> List[Dict[str, Any]]:
        """Get objection templates, optionally filtered by company"""
        query = self.db.query(ObjectionTemplate)
        
        if company_name:
            company = self.db.query(Company).filter(Company.name == company_name).first()
            if company:
                query = query.filter(
                    (ObjectionTemplate.company_id == company.id) | 
                    (ObjectionTemplate.is_default == True)
                )
        else:
            query = query.filter(ObjectionTemplate.is_default == True)
        
        templates = query.all()
        
        return [
            {
                "id": template.id,
                "objection_type": template.objection_type,
                "objection_text": template.objection_text,
                "response_template": template.response_template,
                "is_default": template.is_default
            }
            for template in templates
        ]
    
    def create_objection_template(self, 
                                 objection_type: str,
                                 objection_text: str,
                                 response_template: str,
                                 company_name: str = None) -> ObjectionTemplate:
        """Create a new objection template"""
        company_id = None
        if company_name:
            company = self.db.query(Company).filter(Company.name == company_name).first()
            if company:
                company_id = company.id
        
        template = ObjectionTemplate(
            objection_type=objection_type,
            objection_text=objection_text,
            response_template=response_template,
            company_id=company_id,
            is_default=company_id is None
        )
        
        self.db.add(template)
        self.db.commit()
        return template
    
    def generate_objection_responses(self, 
                                   objection_type: str,
                                   context: str = "",
                                   brand_voice: str = "default") -> List[str]:
        """Generate multiple objection responses using AI"""
        try:
            # Get base template
            template = self.db.query(ObjectionTemplate).filter(
                ObjectionTemplate.objection_type == objection_type
            ).first()
            
            base_response = template.response_template if template else ""
            
            # Generate variations using AI
            prompt = f"""
            Generate 3 different responses to the objection: "{objection_type}"
            
            Context: {context}
            Base template: {base_response}
            Brand voice: {brand_voice}
            
            Make each response:
            1. Natural and conversational
            2. Specific to the context
            3. Matching the brand voice
            4. Focused on value and benefits
            
            Format as:
            Response 1: [response]
            Response 2: [response] 
            Response 3: [response]
            """
            
            response = self.openai_service.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at handling sales objections. Create natural, persuasive responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=600
            )
            
            # Parse the response
            content = response.choices[0].message.content.strip()
            responses = []
            
            for line in content.split('\n'):
                if line.strip().startswith('Response'):
                    response_text = line.split(':', 1)[1].strip()
                    responses.append(response_text)
            
            return responses if responses else [base_response]
            
        except Exception as e:
            # Fallback to template if AI fails
            template = self.db.query(ObjectionTemplate).filter(
                ObjectionTemplate.objection_type == objection_type
            ).first()
            return [template.response_template] if template else ["I understand your concern. Let me address that for you."]
    
    def get_common_objections(self) -> List[str]:
        """Get list of common objection types"""
        return [
            "price",
            "time", 
            "competitor",
            "authority",
            "skepticism",
            "budget",
            "timing",
            "need",
            "trust",
            "complexity"
        ]
    
    def analyze_objection_patterns(self, company_name: str) -> Dict[str, Any]:
        """Analyze objection patterns for a company (if we had call data)"""
        # This would analyze actual call data to identify common objections
        # For now, return default analysis
        return {
            "most_common_objections": ["price", "time", "authority"],
            "success_rate_by_objection": {
                "price": 0.75,
                "time": 0.80,
                "authority": 0.65
            },
            "recommended_responses": {
                "price": "Focus on ROI and value demonstration",
                "time": "Emphasize time savings and efficiency",
                "authority": "Provide decision-maker resources"
            }
        }
