from typing import Dict, List, Any, Optional
from services.company_voice_service import CompanyVoiceService
from services.humanized_voice_service import HumanizedVoiceService
from services.autocall_service import AutoCallService
from services.tts_service import TTSService
from services.export_service import ExportService
from services.script_mode_service import ScriptModeService
import json
import re

class ScriptGeneratorService:
    def __init__(self, db, company_voice_service: CompanyVoiceService):
        self.db = db
        self.company_voice_service = company_voice_service
        self.humanized_voice_service = HumanizedVoiceService()
        self.autocall_service = AutoCallService(db, company_voice_service)
        self.tts_service = TTSService()
        self.export_service = ExportService()
        self.script_mode_service = ScriptModeService()
    
    def generate_script(self, 
                       script_type: str,  # "autocall" or "humanized"
                       voice_id: str,
                       call_type: str,  # "inbound" or "outbound"
                       script_mode: str,  # "banking", "payment", "tech_support", etc.
                       product_info: str,
                       negative_prompts: str = "",
                       interactive_elements: List[Dict[str, Any]] = None,
                       custom_prompts: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate script for either auto-call bot or humanized calling"""
        
        if script_type == "autocall":
            return self._generate_autocall_script(voice_id, call_type, script_mode, product_info, negative_prompts, interactive_elements, custom_prompts)
        elif script_type == "humanized":
            return self._generate_humanized_script(voice_id, call_type, script_mode, product_info, negative_prompts, custom_prompts)
        else:
            raise ValueError("script_type must be 'autocall' or 'humanized'")
    
    def _generate_autocall_script(self, 
                                 voice_id: str,
                                 call_type: str,
                                 script_mode: str,
                                 product_info: str,
                                 negative_prompts: str = "",
                                 interactive_elements: List[Dict[str, Any]] = None,
                                 custom_prompts: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate auto-call bot compatible script with enhanced category integration"""
        
        # Use the company voice service to generate the script with enhanced analysis
        return self.company_voice_service.create_autocall_script(
            voice_id=voice_id,
            call_type=call_type,
            script_mode=script_mode,
            product_info=product_info,
            interactive_elements=interactive_elements or [],
            negative_prompts=negative_prompts
        )
    
    def _generate_humanized_script(self, 
                                  voice_id: str,
                                  call_type: str,
                                  script_mode: str,
                                  product_info: str,
                                  negative_prompts: str = "",
                                  custom_prompts: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate humanized script for human agents"""
        
        # Handle "use_prompt" option - extract company info from prompt
        if voice_id == "use_prompt":
            # Extract company information from the prompt
            company_info = self._extract_company_from_prompt(product_info)
            
            voice = {
                "id": "use_prompt",
                "name": company_info.get("company_name", "Custom Company"),
                "description": f"Uses your prompt to determine voice style for {company_info.get('company_name', 'your company')}",
                "tone": company_info.get("tone", "professional"),
                "style": company_info.get("style", "custom"),
                "phrases": company_info.get("phrases", [
                    "Hello, this is an important call",
                    "I'm calling regarding your account",
                    "This is about your service",
                    "We need to discuss something important",
                    "Thank you for your time"
                ]),
                "objection_handling": company_info.get("objection_handling", {
                    "price": "I understand cost is important. Let me explain the value.",
                    "time": "I appreciate you're busy. This will only take a few minutes.",
                    "skepticism": "I understand your concerns. Let me address them."
                }),
                "company_type": company_info.get("company_type", "general"),
                "industry": company_info.get("industry", "general")
            }
        else:
            # Try to get voice from humanized voices first, then company voices
            voice = self.humanized_voice_service.get_voice_template(voice_id)
            if not voice:
                voice = self.company_voice_service.get_voice_template(voice_id)
            
            if not voice:
                raise ValueError(f"Voice template {voice_id} not found")
        
        # Generate humanized script with enhanced category integration
        custom_prompts = custom_prompts or {}
        custom_prompts['call_type'] = call_type
        custom_prompts['script_mode'] = script_mode
        custom_prompts['negative_prompts'] = negative_prompts
        
        # Use enhanced analysis for humanized scripts too
        script_text = self._create_enhanced_humanized_script(voice, call_type, script_mode, product_info, negative_prompts, custom_prompts)
        
        # Create audio version (commented out for now to avoid hanging)
        # audio_data = self.tts_service.text_to_speech(script_text, voice="default")
        
        return {
            "script_text": script_text,
            "voice": voice,
            "script_type": "humanized",
            "call_type": call_type,
            "script_mode": script_mode,
            "product_info": product_info,
            "negative_prompts": negative_prompts,
            "audio_data": None  # audio_data
        }
    
    def _extract_company_from_prompt(self, product_info: str) -> Dict[str, Any]:
        """Extract company information from the prompt text"""
        company_info = {
            "company_name": "Custom Company",
            "company_type": "general",
            "industry": "general",
            "tone": "professional",
            "style": "custom"
        }
        
        # Enhanced company name extraction patterns
        company_patterns = [
            r'the company is ([A-Za-z0-9\s&]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)',
            r'my company is ([A-Za-z0-9\s&]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)',
            r'company name is ([A-Za-z0-9\s&]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)',
            r'calling from ([A-Za-z0-9\s&]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)',
            r'this is ([A-Za-z0-9\s&]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)',
            r'from ([A-Za-z0-9\s&]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)',
            r'([A-Za-z0-9\s&]+?)\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)',
            r'([A-Za-z0-9\s&]+?)\s+(?:calling|phoning|contacting)',
            r'([A-Za-z0-9\s&]+?)\s+(?:regarding|about|concerning)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, product_info, re.IGNORECASE)
            if match:
                company_name = match.group(1).strip()
                # Clean up the company name
                company_name = re.sub(r'\s+', ' ', company_name)
                if len(company_name) > 2:
                    company_info["company_name"] = company_name
                    break
        
        # Determine company type and industry based on keywords
        prompt_lower = product_info.lower()
        
        if any(keyword in prompt_lower for keyword in ['bank', 'banking', 'financial', 'finance', 'account', 'loan', 'mortgage']):
            company_info["company_type"] = "banking"
            company_info["industry"] = "financial_services"
            company_info["tone"] = "professional"
            company_info["style"] = "formal"
        elif any(keyword in prompt_lower for keyword in ['shop', 'store', 'retail', 'order', 'purchase', 'fashion', 'clothing']):
            company_info["company_type"] = "retail"
            company_info["industry"] = "e_commerce"
            company_info["tone"] = "friendly"
            company_info["style"] = "customer_focused"
        elif any(keyword in prompt_lower for keyword in ['utility', 'electric', 'gas', 'water', 'energy', 'service']):
            company_info["company_type"] = "utilities"
            company_info["industry"] = "utilities"
            company_info["tone"] = "helpful"
            company_info["style"] = "service_oriented"
        elif any(keyword in prompt_lower for keyword in ['fraud', 'security', 'suspicious', 'verify', 'protect']):
            company_info["company_type"] = "security"
            company_info["industry"] = "security_services"
            company_info["tone"] = "urgent"
            company_info["style"] = "security_focused"
        
        return company_info
    
    def _create_enhanced_humanized_script(self, 
                                        voice: Dict[str, Any], 
                                        call_type: str,
                                        script_mode: str,
                                        product_info: str, 
                                        negative_prompts: str = "",
                                        custom_prompts: Dict[str, Any] = None) -> str:
        """Create enhanced humanized script that integrates all selected options"""
        
        script_parts = []
        
        # Get company name from voice or extract from prompt
        company_name = voice.get("name", "our company")
        
        # Get mode configuration
        mode_config = self.script_mode_service.get_mode_config(script_mode)
        
        # Opening based on call type and category
        if call_type == 'inbound':
            script_parts.append(f"AGENT: Thank you for calling {company_name}. This is {voice.get('name', 'Sarah')} from our {mode_config.get('department', 'customer service')} team.")
        else:  # outbound
            script_parts.append(f"AGENT: Hi, this is {voice.get('name', 'Sarah')} from {company_name}.")
            script_parts.append(f"AGENT: We are calling from our {mode_config.get('department', 'customer service')} team regarding {product_info}.")
        
        # Add category-specific context
        if script_mode == "fraud_prevention":
            script_parts.append("AGENT: I'm calling about a potential security concern with your account.")
            script_parts.append("AGENT: We've detected some unusual activity that we need to verify with you.")
        elif script_mode == "banking":
            script_parts.append("AGENT: I'm calling about your banking account and some important information we need to discuss.")
        elif script_mode == "shopping":
            script_parts.append("AGENT: I'm calling about your recent order and wanted to provide you with an update.")
        elif script_mode == "utilities":
            script_parts.append("AGENT: I'm calling about your utility service and some important information regarding your account.")
        
        # Add the main prompt content
        script_parts.append(f"AGENT: {product_info}")
        
        # Add category-specific responses
        if mode_config and mode_config.get('customer_responses'):
            script_parts.append("\n--- CUSTOMER RESPONSES ---")
            for response_type, responses in mode_config['customer_responses'].items():
                script_parts.append(f"\nCUSTOMER: [If {response_type}:]")
                for i, response in enumerate(responses[:2], 1):  # Show first 2 responses
                    script_parts.append(f"  {i}. \"{response}\"")
        
        # Add objection handling
        script_parts.append("\n--- OBJECTION HANDLING ---")
        if mode_config and mode_config.get('objection_handling'):
            objection_handling = mode_config['objection_handling']
            for objection_type, response in objection_handling.items():
                script_parts.append(f"\nCUSTOMER: [If they say '{objection_type}']")
                script_parts.append(f"AGENT: {response}")
        else:
            # Add voice-specific objection handling as fallback
            objection_handling = voice.get("objection_handling", {})
            for objection_type, response in objection_handling.items():
                script_parts.append(f"\nCUSTOMER: [If they say '{objection_type}']")
                script_parts.append(f"AGENT: {response}")
        
        # Add negative prompts guidance if provided
        if negative_prompts.strip():
            script_parts.append(f"\n--- AVOID THESE TOPICS ---")
            script_parts.append(f"DO NOT mention: {negative_prompts}")
        
        # Add compliance notes if available
        if mode_config and mode_config.get('compliance_notes'):
            script_parts.append(f"\n--- COMPLIANCE NOTES ---")
            script_parts.append(f"AGENT: [Remember: {mode_config['compliance_notes']}]")
        
        # Closing
        script_parts.append("\n--- CLOSING ---")
        script_parts.append("AGENT: Is there anything else I can help you with today?")
        script_parts.append("AGENT: Thank you for taking the time to speak with me. Have a great day!")
        
        return "\n".join(script_parts)
    
    def get_available_voices(self, voice_type: str = "autocall") -> List[Dict[str, Any]]:
        """Get available voices for the specified type"""
        if voice_type == "autocall":
            return self.company_voice_service.get_professional_voices()
        else:
            return self.humanized_voice_service.get_all_voices()
    
    def get_humanized_voices(self) -> List[Dict[str, Any]]:
        """Get all humanized voice options"""
        return self.humanized_voice_service.get_all_voices()
    
    def get_voices_by_accent(self, accent: str) -> List[Dict[str, Any]]:
        """Get humanized voices by accent"""
        return self.humanized_voice_service.get_voices_by_accent(accent)
    
    def get_voices_by_gender(self, gender: str) -> List[Dict[str, Any]]:
        """Get humanized voices by gender"""
        return self.humanized_voice_service.get_voices_by_gender(gender)
    
    def get_available_accents(self) -> List[str]:
        """Get available accents"""
        return self.humanized_voice_service.get_available_accents()
    
    def get_available_genders(self) -> List[str]:
        """Get available genders"""
        return self.humanized_voice_service.get_available_genders()
    
    def generate_connected_humanized_script(self, 
                                          autocall_script: Dict[str, Any],
                                          voice_id: str,
                                          call_type: str,
                                          script_mode: str,
                                          product_info: str,
                                          negative_prompts: str = "",
                                          custom_prompts: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a humanized script that follows up on an auto-call script"""
        
        # Analyze the auto-call script to extract context
        context = self._analyze_autocall_context(autocall_script)
        
        # Generate the humanized script with context awareness
        return self._create_connected_humanized_script(
            context, voice_id, call_type, script_mode, product_info, negative_prompts, custom_prompts
        )
    
    def _analyze_autocall_context(self, autocall_script: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze auto-call script to extract context for humanized follow-up"""
        script_text = autocall_script.get('script_text', '')
        
        context = {
            "company_name": "our company",
            "issue_type": "general inquiry",
            "amount": None,
            "urgency": "normal",
            "department": "customer service"
        }
        
        # Extract company name
        company_match = re.search(r'calling from ([A-Za-z\s]+?)(?:\s+(?:Bank|Banking|Ltd|Limited|Inc|Corp|Corporation|Group|Holdings|PLC|plc)|\s*[.,]|\s*$)', script_text)
        if company_match:
            context["company_name"] = company_match.group(1).strip()
        
        # Extract amount
        amount_match = re.search(r'£?(\d+\.?\d*)', script_text)
        if amount_match:
            context["amount"] = f"£{amount_match.group(1)}"
        
        # Determine issue type
        if any(keyword in script_text.lower() for keyword in ['payment', 'pay now', 'unsettled balance', 'outstanding balance']):
            context["issue_type"] = "payment"
            context["urgency"] = "high"
        elif any(keyword in script_text.lower() for keyword in ['fraud', 'security', 'suspicious activity']):
            context["issue_type"] = "security"
            context["urgency"] = "high"
            context["department"] = "fraud team"
        elif any(keyword in script_text.lower() for keyword in ['order', 'purchase', 'shipping']):
            context["issue_type"] = "order"
            context["department"] = "customer service"
        elif any(keyword in script_text.lower() for keyword in ['utility', 'bill', 'service']):
            context["issue_type"] = "utility"
            context["department"] = "utility services"
        
        return context
    
    def _create_connected_humanized_script(self, 
                                         context: Dict[str, Any],
                                         voice_id: str,
                                         call_type: str,
                                         script_mode: str,
                                         product_info: str,
                                         negative_prompts: str = "",
                                         custom_prompts: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a humanized script that follows up on auto-call context"""
        
        # Get voice template
        if voice_id == "use_prompt":
            company_info = self._extract_company_from_prompt(product_info)
            voice = {
                "id": "use_prompt",
                "name": company_info.get("company_name", context["company_name"]),
                "description": f"Uses your prompt to determine voice style for {company_info.get('company_name', context['company_name'])}",
                "tone": company_info.get("tone", "professional"),
                "style": company_info.get("style", "custom")
            }
        else:
            voice = self.humanized_voice_service.get_voice_template(voice_id)
            if not voice:
                voice = self.company_voice_service.get_voice_template(voice_id)
            
            if not voice:
                raise ValueError(f"Voice template {voice_id} not found")
        
        # Create connected script
        script_parts = []
        company_name = voice.get("name", context["company_name"])
        
        # Opening that acknowledges the auto-call
        if call_type == 'inbound':
            script_parts.append(f"AGENT: Thank you for calling {company_name}. This is {voice.get('name', 'Sarah')} from our {context['department']} team.")
        else:
            script_parts.append(f"AGENT: Hi, this is {voice.get('name', 'Sarah')} from {company_name}.")
            script_parts.append(f"AGENT: I'm calling to follow up on our recent automated call regarding your {context['issue_type']}.")
        
        # Acknowledge the specific issue from auto-call
        if context["issue_type"] == "payment":
            script_parts.append(f"AGENT: I understand you may have questions about the payment of {context['amount'] or 'the amount'} we discussed.")
        elif context["issue_type"] == "security":
            script_parts.append("AGENT: I'm calling to help you with the security concern we mentioned in our automated call.")
        elif context["issue_type"] == "order":
            script_parts.append("AGENT: I wanted to personally follow up on your order and make sure everything is going smoothly.")
        elif context["issue_type"] == "utility":
            script_parts.append("AGENT: I'm calling to discuss your utility service and the information we shared earlier.")
        
        # Add the main prompt content
        script_parts.append(f"AGENT: {product_info}")
        
        # Add context-specific responses
        script_parts.append("\n--- CUSTOMER RESPONSES ---")
        if context["issue_type"] == "payment":
            script_parts.append("\nCUSTOMER: [If they want to pay now:]")
            script_parts.append("  1. \"Yes, I'd like to pay now\"")
            script_parts.append("  2. \"I need a payment plan\"")
            script_parts.append("\nCUSTOMER: [If they have questions:]")
            script_parts.append("  1. \"Can you explain the charges?\"")
            script_parts.append("  2. \"I don't recognize this amount\"")
        elif context["issue_type"] == "security":
            script_parts.append("\nCUSTOMER: [If they're concerned:]")
            script_parts.append("  1. \"I'm worried about my account\"")
            script_parts.append("  2. \"What should I do?\"")
            script_parts.append("\nCUSTOMER: [If they're skeptical:]")
            script_parts.append("  1. \"How do I know this is legitimate?\"")
            script_parts.append("  2. \"I don't trust this call\"")
        
        # Add objection handling
        script_parts.append("\n--- OBJECTION HANDLING ---")
        script_parts.append("\nCUSTOMER: [If they say 'I'm not interested']")
        script_parts.append("AGENT: I completely understand. I just wanted to make sure you have all the information you need about this important matter.")
        script_parts.append("\nCUSTOMER: [If they say 'I'm busy']")
        script_parts.append("AGENT: I appreciate your time. This is important, so I'll be brief and get you the help you need quickly.")
        script_parts.append("\nCUSTOMER: [If they say 'I don't trust this']")
        script_parts.append("AGENT: I understand your caution. You can verify this call by calling us back at our main number, or I can provide you with a reference number.")
        
        # Add negative prompts guidance if provided
        if negative_prompts.strip():
            script_parts.append(f"\n--- AVOID THESE TOPICS ---")
            script_parts.append(f"DO NOT mention: {negative_prompts}")
        
        # Closing
        script_parts.append("\n--- CLOSING ---")
        script_parts.append("AGENT: Is there anything else I can help you with regarding this matter?")
        script_parts.append("AGENT: Thank you for taking the time to speak with me. Have a great day!")
        
        script_text = "\n".join(script_parts)
        
        return {
            "script_text": script_text,
            "voice": voice,
            "script_type": "humanized",
            "call_type": call_type,
            "script_mode": script_mode,
            "product_info": product_info,
            "negative_prompts": negative_prompts,
            "audio_data": None
        }
