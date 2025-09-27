import openai
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_script(self, 
                       company_name: str,
                       script_type: str,
                       audience: str,
                       tone: str,
                       product_info: str,
                       format_type: str,
                       brand_voice: str,
                       handle_objections: bool,
                       training_data: List[Dict] = None,
                       custom_prompts: Dict = None) -> str:
        """Generate a call script using OpenAI GPT-4"""
        
        # Build the base prompt
        prompt = self._build_prompt(
            company_name, script_type, audience, tone, 
            product_info, format_type, brand_voice, 
            handle_objections, training_data, custom_prompts
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert call script generator. Create engaging, effective call scripts that convert leads into customers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _build_prompt(self, 
                     company_name: str,
                     script_type: str,
                     audience: str,
                     tone: str,
                     product_info: str,
                     format_type: str,
                     brand_voice: str,
                     handle_objections: bool,
                     training_data: List[Dict] = None,
                     custom_prompts: Dict = None) -> str:
        """Build the complete prompt for script generation"""
        
        # Base prompt structure
        prompt_parts = [
            f"Write a full {format_type} call script for a {script_type} call.",
            f"Company: {company_name}",
            f"Audience: {audience}",
            f"Tone: {tone}",
            f"Product Info: {product_info}",
            f"Brand Voice: {brand_voice}",
            "",
            "Requirements:",
            "- Make it natural, engaging, and conversion-focused",
            "- Include specific talking points and transitions",
            "- Use natural pauses and conversation flow",
            "- Make it sound like a real conversation, not a script"
        ]
        
        # Add brand voice specific instructions
        if brand_voice == "Dd style":
            prompt_parts.extend([
                "",
                "Brand Voice Guidelines (Dd Style):",
                "- Use meme-driven humor and tech culture references",
                "- Be confident and punchy, no fluff",
                "- Include Solana/crypto references where appropriate",
                "- Keep it short, impactful, and memorable",
                "- Use phrases like 'blink twice', 'we're sending help', etc."
            ])
        elif brand_voice == "British professional":
            prompt_parts.extend([
                "",
                "Brand Voice Guidelines (British Professional):",
                "- Use polished, courteous language",
                "- Clear enunciation and structure",
                "- Subtle persuasion, no hard sell",
                "- Professional but approachable tone"
            ])
        elif brand_voice == "trained" and training_data:
            prompt_parts.extend([
                "",
                "Brand Voice Guidelines (Trained from Data):",
                self._format_training_data(training_data)
            ])
        
        # Add objection handling
        if handle_objections:
            prompt_parts.extend([
                "",
                "Include objection handling for common objections:",
                "- Price concerns",
                "- Time constraints", 
                "- Competitor comparisons",
                "- Authority/decision maker concerns",
                "- Skepticism about claims"
            ])
        
        # Add custom prompts if provided
        if custom_prompts:
            prompt_parts.extend([
                "",
                "Additional Requirements:",
                custom_prompts.get("additional_instructions", "")
            ])
        
        prompt_parts.extend([
            "",
            "Format the script as:",
            "Agent: [dialogue]",
            "Customer: [potential response]",
            "Agent: [response]",
            "",
            "Make it uncensored, natural, and effective. Focus on building rapport and demonstrating value."
        ])
        
        return "\n".join(prompt_parts)
    
    def _format_training_data(self, training_data: List[Dict]) -> str:
        """Format training data for prompt inclusion"""
        if not training_data:
            return ""
        
        formatted_data = ["Based on this training data, match the voice and style:"]
        
        for data in training_data:
            if data.get("data_type") == "tweet":
                formatted_data.append(f"Tweet: {data.get('content', '')}")
            elif data.get("data_type") == "call_log":
                formatted_data.append(f"Call Log: {data.get('content', '')}")
        
        return "\n".join(formatted_data)
    
    def generate_objection_responses(self, objection_type: str, context: str = "") -> str:
        """Generate specific objection responses"""
        objection_prompts = {
            "price": "Generate a response to 'It's too expensive' that focuses on ROI and value",
            "time": "Generate a response to 'I don't have time' that emphasizes time savings",
            "competitor": "Generate a response to competitor comparison that highlights differentiators",
            "authority": "Generate a response to 'I need to check with my team' that provides helpful information",
            "skepticism": "Generate a response to skepticism that builds credibility"
        }
        
        prompt = objection_prompts.get(objection_type, "Generate a response to this objection")
        if context:
            prompt += f" in the context of: {context}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at handling sales objections. Create natural, persuasive responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI API error for objection response: {str(e)}")
