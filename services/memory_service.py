from typing import Dict, List, Any, Optional
from database.models import MemoryData, Company
from sqlalchemy.orm import Session
from datetime import datetime

class MemoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def save_memory(self, 
                   company_id: int, 
                   memory_type: str, 
                   memory_key: str, 
                   memory_value: str, 
                   metadata: Dict = None) -> MemoryData:
        """Save or update a memory"""
        # Check if memory already exists
        existing_memory = self.db.query(MemoryData).filter(
            MemoryData.company_id == company_id,
            MemoryData.memory_key == memory_key
        ).first()
        
        if existing_memory:
            # Update existing memory
            existing_memory.memory_value = memory_value
            existing_memory.metadata = metadata or {}
            existing_memory.updated_at = datetime.utcnow()
            self.db.commit()
            return existing_memory
        else:
            # Create new memory
            memory = MemoryData(
                company_id=company_id,
                memory_type=memory_type,
                memory_key=memory_key,
                memory_value=memory_value,
                metadata=metadata or {}
            )
            self.db.add(memory)
            self.db.commit()
            return memory
    
    def get_memory(self, company_id: int, memory_key: str) -> Optional[MemoryData]:
        """Get a specific memory"""
        return self.db.query(MemoryData).filter(
            MemoryData.company_id == company_id,
            MemoryData.memory_key == memory_key
        ).first()
    
    def get_memories_by_type(self, company_id: int, memory_type: str) -> List[MemoryData]:
        """Get all memories of a specific type"""
        return self.db.query(MemoryData).filter(
            MemoryData.company_id == company_id,
            MemoryData.memory_type == memory_type
        ).all()
    
    def get_all_memories(self, company_id: int) -> List[MemoryData]:
        """Get all memories for a company"""
        return self.db.query(MemoryData).filter(
            MemoryData.company_id == company_id
        ).all()
    
    def delete_memory(self, company_id: int, memory_key: str) -> bool:
        """Delete a memory"""
        memory = self.db.query(MemoryData).filter(
            MemoryData.company_id == company_id,
            MemoryData.memory_key == memory_key
        ).first()
        
        if memory:
            self.db.delete(memory)
            self.db.commit()
            return True
        return False
    
    def save_script_preferences(self, company_id: int, preferences: Dict[str, Any]) -> MemoryData:
        """Save script generation preferences"""
        return self.save_memory(
            company_id=company_id,
            memory_type="script_preference",
            memory_key="default_preferences",
            memory_value=str(preferences),
            metadata={"updated_at": datetime.utcnow().isoformat()}
        )
    
    def get_script_preferences(self, company_id: int) -> Dict[str, Any]:
        """Get saved script preferences"""
        memory = self.get_memory(company_id, "default_preferences")
        if memory:
            try:
                return eval(memory.memory_value)  # Convert string back to dict
            except:
                return {}
        return {}
    
    def save_brand_style(self, company_id: int, style_guide: Dict[str, Any]) -> MemoryData:
        """Save brand style guide"""
        return self.save_memory(
            company_id=company_id,
            memory_type="brand_style",
            memory_key="style_guide",
            memory_value=str(style_guide),
            metadata={"updated_at": datetime.utcnow().isoformat()}
        )
    
    def get_brand_style(self, company_id: int) -> Dict[str, Any]:
        """Get saved brand style"""
        memory = self.get_memory(company_id, "style_guide")
        if memory:
            try:
                return eval(memory.memory_value)
            except:
                return {}
        return {}
    
    def save_custom_training(self, company_id: int, training_info: str) -> MemoryData:
        """Save custom training information"""
        return self.save_memory(
            company_id=company_id,
            memory_type="custom_training",
            memory_key=f"training_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            memory_value=training_info,
            metadata={"created_at": datetime.utcnow().isoformat()}
        )
    
    def get_custom_training(self, company_id: int) -> List[str]:
        """Get all custom training information"""
        memories = self.get_memories_by_type(company_id, "custom_training")
        return [memory.memory_value for memory in memories]
    
    def save_objection_handling(self, company_id: int, objection_responses: Dict[str, str]) -> MemoryData:
        """Save custom objection handling responses"""
        return self.save_memory(
            company_id=company_id,
            memory_type="objection_handling",
            memory_key="custom_responses",
            memory_value=str(objection_responses),
            metadata={"updated_at": datetime.utcnow().isoformat()}
        )
    
    def get_objection_handling(self, company_id: int) -> Dict[str, str]:
        """Get custom objection handling responses"""
        memory = self.get_memory(company_id, "custom_responses")
        if memory:
            try:
                return eval(memory.memory_value)
            except:
                return {}
        return {}
    
    def build_memory_context(self, company_id: int) -> str:
        """Build memory context for script generation"""
        memories = self.get_all_memories(company_id)
        
        if not memories:
            return ""
        
        context_parts = ["MEMORY CONTEXT:"]
        
        for memory in memories:
            if memory.memory_type == "script_preference":
                context_parts.append(f"Script Preferences: {memory.memory_value}")
            elif memory.memory_type == "brand_style":
                context_parts.append(f"Brand Style: {memory.memory_value}")
            elif memory.memory_type == "custom_training":
                context_parts.append(f"Custom Training: {memory.memory_value}")
            elif memory.memory_type == "objection_handling":
                context_parts.append(f"Objection Handling: {memory.memory_value}")
        
        return "\n".join(context_parts)
