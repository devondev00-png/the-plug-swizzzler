from typing import Dict, List, Any, Optional
from database.models import CompanyVoice, Company
from sqlalchemy.orm import Session
import json
import re

class CompanyVoiceService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_professional_voices(self) -> List[Dict[str, Any]]:
        """Get all professional company voice templates"""
        return [
            # Banking & Finance
            {
                "id": "natwest",
                "name": "NatWest Bank",
                "description": "Professional, trustworthy banking voice",
                "tone": "professional",
                "style": "formal",
                "phrases": [
                    "Thank you for calling NatWest",
                    "I'm calling from NatWest regarding your account",
                    "For security purposes, I need to verify some details",
                    "Is this a convenient time to speak?",
                    "I understand your concern, let me help you with that"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. Our services provide excellent value and security for your money.",
                    "time": "I appreciate you're busy. This will only take a few minutes and could save you money.",
                    "skepticism": "I completely understand your caution. NatWest has been serving customers for over 300 years."
                }
            },
            {
                "id": "hsbc",
                "name": "HSBC Bank",
                "description": "International banking expertise with local knowledge",
                "tone": "professional",
                "style": "international",
                "phrases": [
                    "Welcome to HSBC, the world's local bank",
                    "I'm calling from HSBC regarding your account",
                    "We're here to support your financial goals",
                    "How may I help you with your banking needs?",
                    "Your financial wellbeing is our priority"
                ],
                "objection_handling": {
                    "price": "I understand your concerns about cost. HSBC offers competitive rates and flexible solutions.",
                    "time": "I know your time is valuable. This call could help you optimize your financial situation.",
                    "skepticism": "I understand your hesitation. HSBC has been trusted globally for over 150 years."
                }
            },
            {
                "id": "barclays",
                "name": "Barclays Bank",
                "description": "Innovative banking solutions with personal touch",
                "tone": "professional",
                "style": "innovative",
                "phrases": [
                    "Hello, this is Barclays calling",
                    "I'm calling from Barclays about your account",
                    "We have some exciting opportunities for you",
                    "Let me explain how this can benefit you",
                    "Your success is our success"
                ],
                "objection_handling": {
                    "price": "I understand cost matters. Barclays offers competitive rates with added value services.",
                    "time": "I respect your time. This opportunity could significantly improve your financial position.",
                    "skepticism": "I appreciate your caution. Barclays has been innovating in banking for over 300 years."
                }
            },
            {
                "id": "lloyds",
                "name": "Lloyds Bank",
                "description": "Traditional banking with modern solutions",
                "tone": "professional",
                "style": "traditional",
                "phrases": [
                    "Good day, this is Lloyds Bank calling",
                    "I'm calling from Lloyds regarding your account",
                    "We have some important information to share",
                    "This could help you save money",
                    "We're here to support you"
                ],
                "objection_handling": {
                    "price": "I understand your concern about cost. Lloyds offers competitive rates and excellent service.",
                    "time": "I know you're busy. This could save you time and money in the long run.",
                    "skepticism": "I understand your hesitation. Lloyds has been helping customers for over 250 years."
                }
            },
            {
                "id": "santander",
                "name": "Santander Bank",
                "description": "Customer-focused banking with Spanish heritage",
                "tone": "professional",
                "style": "customer_focused",
                "phrases": [
                    "Hello, this is Santander calling",
                    "I'm calling from Santander about your account",
                    "We have some great news for you",
                    "This could benefit you significantly",
                    "We're committed to your financial success"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. Santander offers competitive rates with excellent service.",
                    "time": "I appreciate your time. This opportunity could improve your financial situation.",
                    "skepticism": "I understand your caution. Santander has been serving customers for over 160 years."
                }
            },
            # E-commerce & Retail
            {
                "id": "amazon",
                "name": "Amazon",
                "description": "Customer-obsessed e-commerce giant",
                "tone": "friendly",
                "style": "customer_obsessed",
                "phrases": [
                    "Hello, this is Amazon calling",
                    "I'm calling from Amazon about your order",
                    "We want to make sure you're completely satisfied",
                    "How can we make this right for you?",
                    "Your satisfaction is our priority"
                ],
                "objection_handling": {
                    "price": "I understand price matters. Amazon offers competitive prices and excellent value.",
                    "time": "I know your time is valuable. This will help you get the best deal.",
                    "skepticism": "I understand your concern. Amazon is committed to customer satisfaction."
                }
            },
            # Major US Banks
            {
                "id": "jpmorgan",
                "name": "JPMorgan Chase",
                "description": "Leading US investment and commercial bank",
                "tone": "professional",
                "style": "prestigious",
                "phrases": [
                    "Good day, this is JPMorgan Chase calling",
                    "I'm calling from JPMorgan regarding your account",
                    "We have some important financial opportunities for you",
                    "This could significantly benefit your portfolio",
                    "We're committed to your financial success"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. JPMorgan offers competitive rates with exceptional service.",
                    "time": "I respect your time. This opportunity could enhance your financial position.",
                    "skepticism": "I appreciate your caution. JPMorgan has been a trusted financial partner for over 200 years."
                }
            },
            {
                "id": "bank_of_america",
                "name": "Bank of America",
                "description": "Major US retail and commercial bank",
                "tone": "professional",
                "style": "accessible",
                "phrases": [
                    "Hello, this is Bank of America calling",
                    "I'm calling from Bank of America about your account",
                    "We have some great financial solutions for you",
                    "This could help you achieve your financial goals",
                    "We're here to support your financial journey"
                ],
                "objection_handling": {
                    "price": "I understand cost matters. Bank of America offers competitive rates and valuable benefits.",
                    "time": "I know your time is valuable. This could save you money and time.",
                    "skepticism": "I understand your hesitation. Bank of America has been serving customers for over 90 years."
                }
            },
            {
                "id": "wells_fargo",
                "name": "Wells Fargo",
                "description": "Major US diversified financial services",
                "tone": "professional",
                "style": "community_focused",
                "phrases": [
                    "Good day, this is Wells Fargo calling",
                    "I'm calling from Wells Fargo regarding your account",
                    "We have some important information to share",
                    "This could help you manage your finances better",
                    "We're here to help you succeed"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. Wells Fargo offers competitive rates and comprehensive services.",
                    "time": "I appreciate your time. This could improve your financial situation.",
                    "skepticism": "I understand your caution. Wells Fargo has been helping customers for over 170 years."
                }
            },
            # Australian Banks
            {
                "id": "commonwealth_bank",
                "name": "Commonwealth Bank of Australia",
                "description": "Australia's largest bank",
                "tone": "professional",
                "style": "australian",
                "phrases": [
                    "G'day, this is Commonwealth Bank calling",
                    "I'm calling from CommBank about your account",
                    "We've got some great opportunities for you",
                    "This could really help you out",
                    "We're here to support you, mate"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. CommBank offers competitive rates and excellent value.",
                    "time": "I know you're flat out. This could save you time and money.",
                    "skepticism": "I understand your hesitation. CommBank has been helping Aussies for over 100 years."
                }
            },
            {
                "id": "anz",
                "name": "ANZ Bank",
                "description": "Major Australian and New Zealand bank",
                "tone": "professional",
                "style": "international",
                "phrases": [
                    "Hello, this is ANZ calling",
                    "I'm calling from ANZ regarding your account",
                    "We have some important updates for you",
                    "This could benefit your financial situation",
                    "We're committed to your success"
                ],
                "objection_handling": {
                    "price": "I understand cost matters. ANZ offers competitive rates with great service.",
                    "time": "I know your time is valuable. This could help you financially.",
                    "skepticism": "I understand your caution. ANZ has been trusted for over 180 years."
                }
            },
            # German Banks
            {
                "id": "deutsche_bank",
                "name": "Deutsche Bank",
                "description": "Major German investment bank",
                "tone": "professional",
                "style": "european",
                "phrases": [
                    "Guten Tag, this is Deutsche Bank calling",
                    "I'm calling from Deutsche Bank regarding your account",
                    "We have some important financial information",
                    "This could significantly benefit you",
                    "We're here to support your financial goals"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. Deutsche Bank offers competitive rates with European expertise.",
                    "time": "I respect your time. This opportunity could enhance your financial position.",
                    "skepticism": "I appreciate your caution. Deutsche Bank has been a trusted financial partner for over 150 years."
                }
            },
            # Major Tech Companies
            {
                "id": "google",
                "name": "Google",
                "description": "Global technology leader",
                "tone": "innovative",
                "style": "tech_forward",
                "phrases": [
                    "Hello, this is Google calling",
                    "I'm calling from Google about your account",
                    "We have some exciting updates for you",
                    "This could help you grow your business",
                    "We're here to help you succeed online"
                ],
                "objection_handling": {
                    "price": "I understand cost matters. Google offers excellent value and measurable results.",
                    "time": "I know your time is valuable. This could save you time and increase efficiency.",
                    "skepticism": "I understand your hesitation. Google is trusted by millions of businesses worldwide."
                }
            },
            {
                "id": "microsoft",
                "name": "Microsoft",
                "description": "Global technology and cloud services",
                "tone": "professional",
                "style": "enterprise",
                "phrases": [
                    "Hello, this is Microsoft calling",
                    "I'm calling from Microsoft about your account",
                    "We have some important updates for you",
                    "This could help you work more efficiently",
                    "We're here to empower your productivity"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. Microsoft offers competitive pricing with excellent ROI.",
                    "time": "I respect your time. This could significantly improve your workflow.",
                    "skepticism": "I appreciate your caution. Microsoft has been empowering businesses for over 40 years."
                }
            },
            {
                "id": "apple",
                "name": "Apple",
                "description": "Premium technology and services",
                "tone": "premium",
                "style": "sophisticated",
                "phrases": [
                    "Hello, this is Apple calling",
                    "I'm calling from Apple about your account",
                    "We have some exciting news for you",
                    "This could enhance your Apple experience",
                    "We're here to help you get the most from your devices"
                ],
                "objection_handling": {
                    "price": "I understand cost matters. Apple offers premium quality and exceptional value.",
                    "time": "I know your time is valuable. This could save you time and improve your experience.",
                    "skepticism": "I understand your hesitation. Apple is committed to delivering the best user experience."
                }
            },
            {
                "id": "asos",
                "name": "ASOS",
                "description": "Fashion-forward online retailer",
                "tone": "trendy",
                "style": "fashion_forward",
                "phrases": [
                    "Hey, this is ASOS calling",
                    "I'm calling from ASOS about your order",
                    "We have some amazing fashion updates for you",
                    "This could help you stay on trend",
                    "We're here to help you look amazing"
                ],
                "objection_handling": {
                    "price": "I understand style matters. ASOS offers great fashion at amazing prices.",
                    "time": "I know you're busy. This will help you stay stylish effortlessly.",
                    "skepticism": "I understand your hesitation. ASOS is trusted by millions of fashion lovers."
                }
            },
            {
                "id": "use_prompt",
                "name": "Use Prompt",
                "description": "Extract company name and details from your prompt",
                "tone": "custom",
                "style": "extracted",
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
        ]
    
    def get_voice_template(self, voice_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific voice template by ID"""
        voices = self.get_professional_voices()
        for voice in voices:
            if voice["id"] == voice_id:
                return voice
        return None
    
    def create_autocall_script(self, 
                              voice_id: str,
                              call_type: str,
                              script_mode: str,
                              product_info: str,
                              interactive_elements: List[Dict[str, Any]] = None,
                              negative_prompts: str = "") -> Dict[str, Any]:
        """Create an auto-call script with enhanced integration"""
        
        # Handle "use_prompt" option - extract company info from prompt
        if voice_id == "use_prompt":
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
            voice = self.get_voice_template(voice_id)
            if not voice:
                raise ValueError(f"Voice template {voice_id} not found")
        
        script_parts = []
        audio_instructions = []
        
        # Analyze the prompt to understand exactly what the user wants
        prompt_analysis = self._analyze_prompt_intent(product_info)
        
        # Integrate script_mode (category) with prompt analysis
        enhanced_analysis = self._enhance_analysis_with_category(prompt_analysis, script_mode, call_type, negative_prompts)
        
        if enhanced_analysis["intent"] == "payment_collection":
            script_parts = self._create_payment_collection_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "debt_collection":
            script_parts = self._create_debt_collection_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "balance_inquiry":
            script_parts = self._create_balance_inquiry_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "service_update":
            script_parts = self._create_service_update_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "fraud_prevention":
            script_parts = self._create_fraud_prevention_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "banking":
            script_parts = self._create_banking_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "shopping":
            script_parts = self._create_shopping_script(voice, product_info, enhanced_analysis)
        elif enhanced_analysis["intent"] == "utilities":
            script_parts = self._create_utilities_script(voice, product_info, enhanced_analysis)
        else:
            # Generic script based on prompt
            script_parts = self._create_generic_script(voice, product_info, enhanced_analysis)
        
        # Create the final script
        script_text = "\n".join(script_parts)
        
        return {
            "script_text": script_text,
            "voice": voice,
            "script_type": "autocall",
            "call_type": call_type,
            "script_mode": script_mode,
            "product_info": product_info,
            "negative_prompts": negative_prompts,
            "interactive_elements": interactive_elements or []
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
        
        # Set appropriate phrases based on company type
        if company_info["company_type"] == "banking":
            company_info["phrases"] = [
                "Hello, this is an important call from {company_name}",
                "I'm calling regarding your account",
                "This is about your banking service",
                "We need to discuss something important",
                "Thank you for your time"
            ]
        elif company_info["company_type"] == "retail":
            company_info["phrases"] = [
                "Hi, this is {company_name} calling",
                "I'm calling about your recent order",
                "We have some great news for you",
                "This could help you save money",
                "Thank you for being a valued customer"
            ]
        elif company_info["company_type"] == "utilities":
            company_info["phrases"] = [
                "Hello, this is {company_name} calling",
                "I'm calling about your utility service",
                "We have important information for you",
                "This could help you save on your bills",
                "Thank you for choosing {company_name}"
            ]
        elif company_info["company_type"] == "security":
            company_info["phrases"] = [
                "Hello, this is an urgent call from {company_name}",
                "I'm calling about a security concern",
                "This is about protecting your account",
                "We need to verify some information",
                "Thank you for your immediate attention"
            ]
        else:
            company_info["phrases"] = [
                "Hello, this is an important call",
                "I'm calling regarding your account",
                "This is about your service",
                "We need to discuss something important",
                "Thank you for your time"
            ]
        
        # Set objection handling based on company type
        company_info["objection_handling"] = {
            "price": "I understand cost is important. Let me explain the value.",
            "time": "I appreciate you're busy. This will only take a few minutes.",
            "skepticism": "I understand your concerns. Let me address them."
        }
        
        return company_info
    
    def _analyze_prompt_intent(self, product_info: str) -> Dict[str, Any]:
        """Analyze the prompt to understand exactly what the user wants"""
        prompt_lower = product_info.lower()
        
        # Extract amount
        amount_match = re.search(r'£?(\d+\.?\d*)', product_info)
        amount = f"£{amount_match.group(1)}" if amount_match else None
        
        # Extract company name
        company_name = "our company"
        company_patterns = [
            r'company\s+is\s+([A-Za-z\s]+?)(?:\s+Bank|\s+Banking|\.|,|$)',
            r'calling\s+from\s+([A-Za-z\s]+?)(?:\s+Bank|\s+Banking|\.|,|$)',
            r'this\s+is\s+([A-Za-z\s]+?)(?:\s+Bank|\s+Banking|\.|,|$)',
            r'from\s+([A-Za-z\s]+?)(?:\s+Bank|\s+Banking|\.|,|$)',
            r'([A-Za-z\s]+?)\s+Bank',
        ]
        
        for pattern in company_patterns:
            company_match = re.search(pattern, product_info, re.IGNORECASE)
            if company_match:
                company_name = company_match.group(1).strip()
                company_name = re.sub(r'\s+', ' ', company_name)
                if len(company_name) > 2:
                    break
        
        # Determine intent based on specific keywords and context
        if any(keyword in prompt_lower for keyword in ['unsettled balance', 'outstanding balance', 'unpaid balance']):
            return {
                "intent": "debt_collection",
                "amount": amount,
                "company_name": company_name,
                "specific_issue": "unsettled balance",
                "urgency": "high"
            }
        elif any(keyword in prompt_lower for keyword in ['fine', 'penalty', 'late fee']):
            return {
                "intent": "debt_collection", 
                "amount": amount,
                "company_name": company_name,
                "specific_issue": "fine",
                "urgency": "high"
            }
        elif any(keyword in prompt_lower for keyword in ['payment', 'pay now', 'immediate payment']):
            return {
                "intent": "payment_collection",
                "amount": amount,
                "company_name": company_name,
                "specific_issue": "payment",
                "urgency": "high"
            }
        elif any(keyword in prompt_lower for keyword in ['balance', 'account balance', 'check balance']):
            return {
                "intent": "balance_inquiry",
                "amount": amount,
                "company_name": company_name,
                "specific_issue": "balance inquiry",
                "urgency": "normal"
            }
        elif any(keyword in prompt_lower for keyword in ['service', 'update', 'maintenance', 'outage']):
            return {
                "intent": "service_update",
                "amount": amount,
                "company_name": company_name,
                "specific_issue": "service update",
                "urgency": "normal"
            }
        else:
            return {
                "intent": "general",
                "amount": amount,
                "company_name": company_name,
                "specific_issue": "general inquiry",
                "urgency": "normal"
            }
    
    def _enhance_analysis_with_category(self, prompt_analysis: Dict[str, Any], script_mode: str, call_type: str, negative_prompts: str) -> Dict[str, Any]:
        """Enhance prompt analysis with selected category and other options"""
        enhanced = prompt_analysis.copy()
        
        # Override intent based on selected category if it's more specific
        category_intent_mapping = {
            "fraud_prevention": "fraud_prevention",
            "banking": "banking", 
            "shopping": "shopping",
            "utilities": "utilities",
            "debt_collection": "debt_collection",
            "payment_processing": "payment_collection",
            "balance_inquiry": "balance_inquiry",
            "service_update": "service_update"
        }
        
        if script_mode in category_intent_mapping:
            enhanced["intent"] = category_intent_mapping[script_mode]
            enhanced["category"] = script_mode
        else:
            enhanced["category"] = "general"
        
        # Add call type context
        enhanced["call_type"] = call_type
        
        # Add negative prompts context
        enhanced["negative_prompts"] = negative_prompts
        
        # Add category-specific context
        if script_mode == "fraud_prevention":
            enhanced["urgency"] = "high"
            enhanced["tone"] = "urgent and professional"
            enhanced["department"] = "fraud team"
        elif script_mode == "banking":
            enhanced["urgency"] = "normal"
            enhanced["tone"] = "professional and reassuring"
            enhanced["department"] = "banking services"
        elif script_mode == "shopping":
            enhanced["urgency"] = "normal"
            enhanced["tone"] = "friendly and helpful"
            enhanced["department"] = "customer service"
        elif script_mode == "utilities":
            enhanced["urgency"] = "normal"
            enhanced["tone"] = "helpful and informative"
            enhanced["department"] = "utility services"
        
        return enhanced
    
    def _create_payment_collection_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a proper payment collection script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        amount = analysis["amount"] or "the amount"
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling regarding your payment of {amount}.",
            "AGENT: Press 1 to pay now, 2 for payment plan, or 3 to speak to someone.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Payment]",
            "AGENT: Thank you for choosing to pay now. Please enter your 16-digit card number after the beep.",
            "SYSTEM: [Wait for input - 15 second timeout]",
            "CUSTOMER: [Enters card number]",
            "AGENT: Please enter your card expiry date in MM/YY format.",
            "SYSTEM: [Wait for input - 10 second timeout]",
            "CUSTOMER: [Enters expiry date]",
            "AGENT: Please enter your 3-digit security code on the back of your card.",
            "SYSTEM: [Wait for input - 10 second timeout]",
            "CUSTOMER: [Enters CVV]",
            f"AGENT: Please confirm the payment amount of {amount}. Press 1 for yes, 2 for no.",
            "SYSTEM: [Wait for confirmation - 5 second timeout]",
            "CUSTOMER: [Presses 1]",
            "AGENT: Payment processed successfully. You will receive a confirmation email shortly. Thank you!",
            "",
            "CUSTOMER: [Presses 2 - Payment Plan]",
            "AGENT: I understand you need a payment plan. Let me transfer you to our payment department.",
            "AGENT: Please hold while I connect you.",
            "",
            "CUSTOMER: [Presses 3 - Speak to Someone]",
            "AGENT: I'll transfer you to one of our representatives who can help you with your payment.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_debt_collection_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a proper debt collection script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        amount = analysis["amount"] or "the amount"
        specific_issue = analysis["specific_issue"]
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling regarding your {specific_issue} of {amount}.",
            "AGENT: Press 1 to pay now, 2 for payment plan, or 3 to speak to someone.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Pay Now]",
            "AGENT: Thank you for choosing to pay now. Please enter your 16-digit card number after the beep.",
            "SYSTEM: [Wait for input - 15 second timeout]",
            "CUSTOMER: [Enters card number]",
            "AGENT: Please enter your card expiry date in MM/YY format.",
            "SYSTEM: [Wait for input - 10 second timeout]",
            "CUSTOMER: [Enters expiry date]",
            "AGENT: Please enter your 3-digit security code on the back of your card.",
            "SYSTEM: [Wait for input - 10 second timeout]",
            "CUSTOMER: [Enters CVV]",
            f"AGENT: Please confirm the payment amount of {amount}. Press 1 for yes, 2 for no.",
            "SYSTEM: [Wait for confirmation - 5 second timeout]",
            "CUSTOMER: [Presses 1]",
            f"AGENT: Payment processed successfully. Your {specific_issue} has been cleared. Thank you!",
            "",
            "CUSTOMER: [Presses 2 - Payment Plan]",
            f"AGENT: I understand you need a payment plan for your {specific_issue}. Let me transfer you to our collections department.",
            "AGENT: Please hold while I connect you.",
            "",
            "CUSTOMER: [Presses 3 - Speak to Someone]",
            f"AGENT: I'll transfer you to one of our representatives who can help you with your {specific_issue}.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_fraud_prevention_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a fraud prevention script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        department = analysis.get("department", "fraud team")
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling from our {department} regarding a potential security concern with your account.",
            "AGENT: Press 1 to verify your identity, 2 to speak to our fraud team, or 3 to end the call.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Verify Identity]",
            "AGENT: Thank you for choosing to verify. For security purposes, please enter the last 4 digits of your social security number.",
            "SYSTEM: [Wait for input - 10 second timeout]",
            "CUSTOMER: [Enters last 4 digits]",
            "AGENT: Please confirm your date of birth in MM/DD/YYYY format.",
            "SYSTEM: [Wait for input - 10 second timeout]",
            "CUSTOMER: [Enters date of birth]",
            "AGENT: Thank you for verifying your identity. We have detected suspicious activity on your account.",
            "AGENT: Press 1 to secure your account now, 2 to speak to a fraud specialist, or 3 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Speak to Fraud Team]",
            "AGENT: I'll transfer you to our fraud prevention team immediately.",
            "AGENT: Please hold while I connect you to a specialist.",
            "",
            "CUSTOMER: [Presses 3 - End Call]",
            "AGENT: If you have any concerns about your account security, please call us immediately at our fraud hotline.",
            "AGENT: Thank you for your time."
        ])
        
        return script_parts
    
    def _create_banking_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a banking script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        department = analysis.get("department", "banking services")
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling from our {department} regarding your account.",
            "AGENT: Press 1 for account information, 2 to speak to a banking specialist, or 3 to end the call.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Account Information]",
            "AGENT: Please enter your account number or the last 4 digits of your social security number.",
            "SYSTEM: [Wait for input - 15 second timeout]",
            "CUSTOMER: [Enters account information]",
            "AGENT: Thank you. I can see your account information. How can I assist you today?",
            "AGENT: Press 1 for balance inquiry, 2 for transaction history, 3 to speak to someone, or 4 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Speak to Banking Specialist]",
            "AGENT: I'll transfer you to one of our banking specialists.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_shopping_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a shopping/e-commerce script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        department = analysis.get("department", "customer service")
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling from our {department} regarding your recent order.",
            "AGENT: Press 1 for order status, 2 to speak to customer service, or 3 to end the call.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Order Status]",
            "AGENT: Please enter your order number or the email address used for the purchase.",
            "SYSTEM: [Wait for input - 15 second timeout]",
            "CUSTOMER: [Enters order information]",
            "AGENT: Thank you. I can see your order details. Your order is currently being processed.",
            "AGENT: Press 1 for shipping updates, 2 to modify your order, 3 to speak to someone, or 4 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Speak to Customer Service]",
            "AGENT: I'll transfer you to our customer service team.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_utilities_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a utilities script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        department = analysis.get("department", "utility services")
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling from our {department} regarding your utility service.",
            "AGENT: Press 1 for account information, 2 to speak to a service representative, or 3 to end the call.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Account Information]",
            "AGENT: Please enter your account number or service address.",
            "SYSTEM: [Wait for input - 15 second timeout]",
            "CUSTOMER: [Enters account information]",
            "AGENT: Thank you. I can see your utility account. How can I assist you today?",
            "AGENT: Press 1 for bill inquiry, 2 for service updates, 3 to speak to someone, or 4 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Speak to Service Representative]",
            "AGENT: I'll transfer you to one of our service representatives.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_balance_inquiry_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a balance inquiry script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        amount = analysis["amount"] or "your current balance"
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: We are calling to inform you about your account balance of {amount}.",
            "AGENT: Press 1 for more details, 2 to make a payment, or 3 to speak to someone.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - More Details]",
            f"AGENT: Your current balance is {amount}. This includes any recent transactions and fees.",
            "AGENT: Press 1 to make a payment, 2 to speak to someone, or 3 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Make Payment]",
            "AGENT: I'll transfer you to our payment department to process your payment.",
            "AGENT: Please hold while I connect you.",
            "",
            "CUSTOMER: [Presses 3 - Speak to Someone]",
            "AGENT: I'll transfer you to one of our representatives who can help you with your account.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_service_update_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a service update script"""
        script_parts = []
        
        company_name = analysis["company_name"]
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            "AGENT: We are calling to inform you about an important service update.",
            "AGENT: Press 1 to hear the update, 2 to speak to someone, or 3 to end the call.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - Hear Update]",
            "AGENT: [Service update details based on prompt]",
            "AGENT: Press 1 if you have questions, 2 to speak to someone, or 3 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Speak to Someone]",
            "AGENT: I'll transfer you to one of our representatives who can help you with your service.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
    
    def _create_generic_script(self, voice: Dict[str, Any], product_info: str, analysis: Dict[str, Any]) -> List[str]:
        """Create a generic script based on the prompt"""
        script_parts = []
        
        company_name = analysis["company_name"]
        
        script_parts.extend([
            f"AGENT: Hi, this is an automated call from {company_name}.",
            f"AGENT: {product_info}",
            "AGENT: Press 1 for more information, 2 to speak to someone, or 3 to end the call.",
            "SYSTEM: [Wait for keypad input - 5 second timeout]",
            "",
            "CUSTOMER: [Presses 1 - More Information]",
            "AGENT: [Additional information based on prompt]",
            "AGENT: Press 1 to speak to someone, 2 to end the call.",
            "",
            "CUSTOMER: [Presses 2 - Speak to Someone]",
            "AGENT: I'll transfer you to one of our representatives who can help you.",
            "AGENT: Please hold while I connect you."
        ])
        
        return script_parts
