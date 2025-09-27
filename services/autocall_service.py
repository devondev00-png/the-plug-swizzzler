from typing import Dict, List, Any, Optional
from services.company_voice_service import CompanyVoiceService
from services.tts_service import TTSService
from services.export_service import ExportService
import json
import re

class AutoCallService:
    def __init__(self, db, company_voice_service: CompanyVoiceService):
        self.db = db
        self.company_voice_service = company_voice_service
        self.tts_service = TTSService()
        self.export_service = ExportService()
    
    def generate_autocall_script(self, 
                                voice_id: str,
                                script_type: str,
                                product_info: str,
                                interactive_elements: List[Dict[str, Any]],
                                negative_prompts: str = "",
                                custom_prompts: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate complete auto-call script with audio"""
        
        # Handle "use_prompt" option - create a generic voice template
        if voice_id == "use_prompt":
            voice = {
                "id": "use_prompt",
                "name": "Custom Company",
                "description": "Uses your prompt to determine company voice",
                "tone": "professional",
                "style": "custom",
                "phrases": [
                    "Hello, this is an important call",
                    "I'm calling regarding your account",
                    "This is about your service",
                    "We need to discuss something important",
                    "Thank you for your time"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. Let me explain the value.",
                    "time": "I appreciate you're busy. This will only take a few minutes.",
                    "skepticism": "I understand your concerns. Let me address them."
                }
            }
        else:
            # Get voice template
            voice = self.company_voice_service.get_voice_template(voice_id)
            if not voice:
                raise ValueError(f"Voice template {voice_id} not found")
        
        # Create script structure
        script_data = self.company_voice_service.create_autocall_script(
            voice_id, script_type, product_info, interactive_elements, negative_prompts
        )
        
        # Generate detailed script using AI
        detailed_script = self._generate_detailed_script(
            voice, script_type, product_info, interactive_elements, custom_prompts
        )
        
        # Create audio segments
        audio_segments = self._create_audio_segments(script_data["audio_instructions"])
        
        # Generate auto-call bot compatible format
        autocall_format = self._create_autocall_format(script_data, audio_segments)
        
        return {
            "voice_template": voice,
            "script_text": detailed_script,
            "audio_segments": audio_segments,
            "autocall_format": autocall_format,
            "interactive_elements": interactive_elements,
            "metadata": {
                "voice_id": voice_id,
                "script_type": script_type,
                "product_info": product_info,
                "total_duration": sum(segment.get("duration", 0) for segment in audio_segments)
            }
        }
    
    def _generate_detailed_script(self, 
                                 voice: Dict[str, Any],
                                 script_type: str,
                                 product_info: str,
                                 interactive_elements: List[Dict[str, Any]],
                                 custom_prompts: Dict[str, Any] = None) -> str:
        """Generate detailed script using AI"""
        
        # Build prompt for AI using the user's specific request
        prompt_parts = [
            f"Create a professional {script_type} call script using the {voice['name']} voice style.",
            f"Company: {voice['name']}",
            f"Voice Style: {voice['description']}",
            f"Tone: {voice['tone']}",
            "",
            f"USER'S SPECIFIC REQUEST: {product_info}",
            "",
            "Voice Characteristics:",
            f"- Style: {voice['style']}",
            f"- Common phrases: {', '.join(voice['phrases'])}",
            "",
            "Interactive Elements to Include:"
        ]
        
        for element in interactive_elements:
            if element["type"] == "menu":
                prompt_parts.append(f"- Menu: {element['prompt']} (Options: {', '.join(element['options'])})")
            elif element["type"] == "input":
                prompt_parts.append(f"- Input: {element['prompt']} (Validation: {element.get('validation', 'none')})")
            elif element["type"] == "confirmation":
                prompt_parts.append(f"- Confirmation: {element['prompt']}")
            elif element["type"] == "pause":
                prompt_parts.append(f"- Pause: {element.get('duration', 2)} seconds")
        
        prompt_parts.extend([
            "",
            "Requirements:",
            "- Make it sound natural and professional",
            "- Include appropriate pauses for responses",
            "- Use the company's voice style consistently",
            "- Include objection handling where appropriate",
            "- Format for auto-call bot integration",
            "",
            "Format the script as:",
            "AGENT: [dialogue]",
            "SYSTEM: [instructions]",
            "CUSTOMER: [expected response]",
            "AGENT: [response]",
            "",
            "Make it engaging, professional, and suitable for automated calling."
        ])
        
        # For now, return a template-based script
        # In production, this would call OpenAI
        return self._create_template_script(voice, script_type, product_info, interactive_elements)
    
    def _create_template_script(self, 
                               voice: Dict[str, Any],
                               script_type: str,
                               product_info: str,
                               interactive_elements: List[Dict[str, Any]]) -> str:
        """Create script from template"""
        
        script_parts = []
        
        # Check if this is debt collection and format accordingly
        if "debt" in product_info.lower() or "balance" in product_info.lower() or "fine" in product_info.lower() or "due" in product_info.lower() or "unpaid" in product_info.lower():
            # Extract amount from product_info if present
            import re
            amount_match = re.search(r'£?(\d+\.?\d*)', product_info)
            amount = amount_match.group(1) if amount_match else "the amount"
            
            script_parts.append(f"AGENT: Hi, this is an automated call from {voice['name']}.")
            script_parts.append(f"AGENT: We are calling regarding your unpaid/unsettled balance/fine with us of £{amount}.")
            script_parts.append("AGENT: Press 1 now to pay now, or 2 for call back at a later time, or 3 to hang up.")
            script_parts.append("SYSTEM: [Wait for keypad input - 5 second timeout]")
            script_parts.append("CUSTOMER: [Presses key - possible responses:]")
            script_parts.append("  - Press 1: \"I want to pay now\"")
            script_parts.append("  - Press 2: \"I want a call back\"")
            script_parts.append("  - Press 3: \"I'm hanging up\"")
        else:
            # Skip opening, go straight to the user's specific prompt
            script_parts.append(f"AGENT: {product_info}")
            
            # Add context based on script type
            if script_type == "sales":
                script_parts.append("AGENT: This is an exclusive opportunity we're offering to valued customers like yourself.")
            elif script_type == "support":
                script_parts.append("AGENT: I'm here to help you with this and ensure you're completely satisfied.")
            elif script_type == "follow_up":
                script_parts.append("AGENT: I wanted to personally follow up and see how this is working for you.")
        
        # Interactive elements with customer responses
        for element in interactive_elements:
            if element["type"] == "menu":
                script_parts.append(f"AGENT: {element['prompt']}")
                script_parts.append("SYSTEM: [Wait for keypad input - 3 second timeout]")
                script_parts.append("CUSTOMER: [Presses key - possible responses:]")
                script_parts.append("  - Press 1: \"I'm interested\"")
                script_parts.append("  - Press 2: \"I'm not interested\"")
                script_parts.append("  - Press 3: \"I need more information\"")
                
            elif element["type"] == "input":
                script_parts.append(f"AGENT: {element['prompt']}")
                script_parts.append("SYSTEM: [Wait for input - 10 second timeout]")
                script_parts.append("CUSTOMER: [Provides input - possible responses:]")
                script_parts.append("  - \"I'll give you my [card number/account info/etc.]\"")
                script_parts.append("  - \"I'm not comfortable giving that information\"")
                script_parts.append("  - \"Can you explain why you need this?\"")
                
                # Confirmation
                if element.get("confirmation"):
                    confirmation = element["confirmation"].replace("{input}", "[CUSTOMER_INPUT]")
                    script_parts.append(f"AGENT: {confirmation}")
                    script_parts.append("SYSTEM: [Wait for confirmation - 3 second timeout]")
                    script_parts.append("CUSTOMER: [Presses 1 or 2 - possible responses:]")
                    script_parts.append("  - Press 1: \"Yes, that's correct\"")
                    script_parts.append("  - Press 2: \"No, that's not right\"")
                
            elif element["type"] == "confirmation":
                script_parts.append(f"AGENT: {element['prompt']}")
                script_parts.append("SYSTEM: [Wait for response - 5 second timeout]")
                script_parts.append("CUSTOMER: [Presses key - possible responses:]")
                script_parts.append("  - Press 1: \"Yes, I agree\"")
                script_parts.append("  - Press 2: \"No, I don't agree\"")
                script_parts.append("  - Press 0: \"I need to speak to someone\"")
                
            elif element["type"] == "pause":
                script_parts.append(f"SYSTEM: [Pause for {element.get('duration', 2)} seconds]")
        
        # Objection handling
        script_parts.append("AGENT: I understand if you have any concerns. Let me address the most common questions our customers have.")
        script_parts.append("CUSTOMER: [Potential objection]")
        script_parts.append("AGENT: That's a great question. [Address objection using company's style]")
        
        # Closing
        closing = "Thank you for your time today. Is there anything else I can help you with?"
        script_parts.append(f"AGENT: {closing}")
        script_parts.append("CUSTOMER: [Response]")
        script_parts.append("AGENT: Thank you again. Have a wonderful day!")
        
        return "\n".join(script_parts)
    
    def _create_audio_segments(self, audio_instructions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create audio segments for auto-call bot"""
        segments = []
        
        for i, instruction in enumerate(audio_instructions):
            if instruction["text"] == "[PAUSE FOR INPUT]":
                segments.append({
                    "id": f"pause_{i}",
                    "type": "pause",
                    "duration": 3,
                    "text": "Waiting for input..."
                })
            elif instruction["text"] == "[PAUSE FOR CONFIRMATION]":
                segments.append({
                    "id": f"pause_{i}",
                    "type": "pause",
                    "duration": 5,
                    "text": "Waiting for confirmation..."
                })
            elif instruction["text"] == "[PAUSE]":
                segments.append({
                    "id": f"pause_{i}",
                    "type": "pause",
                    "duration": instruction.get("pause", 2),
                    "text": "Pause"
                })
            else:
                segments.append({
                    "id": f"speech_{i}",
                    "type": "speech",
                    "text": instruction["text"],
                    "duration": len(instruction["text"]) * 0.1,  # Rough estimate
                    "pause_after": instruction.get("pause", 1)
                })
        
        return segments
    
    def _create_autocall_format(self, 
                               script_data: Dict[str, Any], 
                               audio_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create auto-call bot compatible format"""
        
        return {
            "script_id": "autocall_script",
            "voice_settings": {
                "voice_id": script_data["voice_template"]["id"],
                "voice_name": script_data["voice_template"]["name"],
                "speech_rate": 0.9,
                "pitch": 1.0,
                "volume": 0.8
            },
            "call_flow": {
                "opening": {
                    "type": "speech",
                    "text": script_data["voice_template"]["phrases"][0],
                    "next": "introduction"
                },
                "introduction": {
                    "type": "speech",
                    "text": "I'm calling from {company_name} regarding {product_info}",
                    "next": "main_content"
                },
                "main_content": {
                    "type": "interactive",
                    "elements": script_data["interactive_elements"],
                    "next": "closing"
                },
                "closing": {
                    "type": "speech",
                    "text": "Thank you for your time. Have a great day!",
                    "next": "end"
                }
            },
            "interactive_elements": script_data["interactive_elements"],
            "audio_segments": audio_segments,
            "validation_rules": {
                "phone": r"^\d{10,11}$",
                "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "16_digits": r"^\d{16}$",
                "card_number": r"^\d{13,19}$"
            },
            "timeout_settings": {
                "menu_input": 3,
                "text_input": 10,
                "confirmation": 5,
                "general_pause": 2
            }
        }
    
    def export_for_autocall_bot(self, script_data: Dict[str, Any], format_type: str = "json") -> str:
        """Export script in auto-call bot compatible format"""
        
        if format_type == "json":
            return json.dumps(script_data["autocall_format"], indent=2)
        elif format_type == "xml":
            return self._create_xml_format(script_data)
        elif format_type == "csv":
            return self._create_csv_format(script_data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _create_xml_format(self, script_data: Dict[str, Any]) -> str:
        """Create XML format for auto-call bot"""
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_parts.append('<autocall_script>')
        xml_parts.append(f'  <voice_id>{script_data["voice_template"]["id"]}</voice_id>')
        xml_parts.append(f'  <voice_name>{script_data["voice_template"]["name"]}</voice_name>')
        xml_parts.append('  <call_flow>')
        
        for segment in script_data["audio_segments"]:
            xml_parts.append(f'    <segment id="{segment["id"]}" type="{segment["type"]}">')
            xml_parts.append(f'      <text>{segment["text"]}</text>')
            if "duration" in segment:
                xml_parts.append(f'      <duration>{segment["duration"]}</duration>')
            xml_parts.append('    </segment>')
        
        xml_parts.append('  </call_flow>')
        xml_parts.append('</autocall_script>')
        
        return '\n'.join(xml_parts)
    
    def _create_csv_format(self, script_data: Dict[str, Any]) -> str:
        """Create CSV format for auto-call bot"""
        csv_parts = ['Type,Text,Duration,Next_Action']
        
        for segment in script_data["audio_segments"]:
            csv_parts.append(f'{segment["type"]},"{segment["text"]}",{segment.get("duration", 0)},continue')
        
        return '\n'.join(csv_parts)
