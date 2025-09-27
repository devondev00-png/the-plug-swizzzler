from typing import Dict, List, Any, Optional

class ScriptModeService:
    """Service for handling different script modes and industry-specific templates"""
    
    def __init__(self):
        self.script_modes = {
            # Financial Services
            "banking": {
                "name": "Banking & Finance",
                "tone": "professional, trustworthy, authoritative",
                "phrases": [
                    "This is regarding your account",
                    "For security purposes",
                    "We need to verify your identity",
                    "This is a secure call",
                    "Your account information"
                ],
                "customer_responses": {
                    "positive": [
                        "Oh, okay. What do you need from me?",
                        "Sure, I can help with that.",
                        "Yes, I'm interested in protecting my account.",
                        "What information do you need?",
                        "That sounds important, go ahead."
                    ],
                    "suspicious": [
                        "I'm not sure about this. How do I know you're really from the bank?",
                        "This sounds like a scam. I'm going to hang up.",
                        "I don't give out personal information over the phone.",
                        "I need to verify who you are first.",
                        "I'm going to call the bank directly to check this."
                    ],
                    "busy": [
                        "I'm really busy right now. Can you call back later?",
                        "I don't have time for this right now.",
                        "I'm in the middle of something important.",
                        "Can we do this another time?",
                        "I'm not available right now."
                    ],
                    "confused": [
                        "I don't understand what you're asking for.",
                        "Can you explain this more clearly?",
                        "What exactly do you need from me?",
                        "I'm not sure what this is about.",
                        "Can you slow down and explain again?"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I completely understand your concern about security. This is exactly why we're calling - to protect your account.",
                    "busy": "I know your time is valuable, which is why this call will only take 2 minutes to secure your account.",
                    "not_interested": "I understand, but this is about protecting your money and personal information."
                },
                "compliance_notes": "Must comply with banking regulations, verify identity, maintain security protocols"
            },
            
            "payment": {
                "name": "Payment Processing",
                "tone": "urgent, professional, solution-focused",
                "phrases": [
                    "Payment issue detected",
                    "Immediate action required",
                    "Your payment method",
                    "Transaction processing",
                    "Account verification needed"
                ],
                "customer_responses": {
                    "positive": [
                        "Oh no! What's wrong with my payment?",
                        "I need to fix this right away. What do I do?",
                        "Yes, please help me resolve this.",
                        "What information do you need from me?",
                        "This is urgent, let's get this sorted."
                    ],
                    "suspicious": [
                        "I don't believe this. How do I know you're legitimate?",
                        "This sounds like a scam. I'm not giving you any information.",
                        "I need to verify this with my bank first.",
                        "I'm going to hang up and call my bank directly.",
                        "I don't trust this call at all."
                    ],
                    "busy": [
                        "I'm really busy. Can this wait?",
                        "I don't have time for this right now.",
                        "Can you call back later?",
                        "I'm in a meeting, this will have to wait.",
                        "I'm not available right now."
                    ],
                    "confused": [
                        "I don't understand what the problem is.",
                        "Can you explain what's wrong with my payment?",
                        "What exactly needs to be fixed?",
                        "I'm not sure what you're asking for.",
                        "Can you be more specific about the issue?"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I understand your concern. This is exactly why we need to verify your payment information immediately.",
                    "busy": "This is urgent - your payment is at risk. It will only take 1 minute to resolve.",
                    "not_interested": "This isn't optional - your payment method needs immediate attention."
                },
                "compliance_notes": "Must verify payment details, maintain PCI compliance, secure transaction processing"
            },
            
            "insurance": {
                "name": "Insurance Services",
                "tone": "caring, professional, reassuring",
                "phrases": [
                    "Your policy coverage",
                    "Claims processing",
                    "Premium payment",
                    "Policy renewal",
                    "Coverage verification"
                ],
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about protecting your coverage and ensuring you're properly insured.",
                    "busy": "I know you're busy, but this affects your coverage. It's important we get this sorted quickly.",
                    "not_interested": "This is about your protection and coverage. We need to ensure you're properly insured."
                },
                "compliance_notes": "Must verify policy details, maintain insurance regulations, ensure proper coverage"
            },
            
            "debt_collection": {
                "name": "Debt Collection",
                "tone": "firm but respectful, professional, persistent",
                "phrases": [
                    "This is an automated call from",
                    "We are calling regarding your unpaid/unsettled balance/fine with us of",
                    "Press 1 now to pay now",
                    "Press 2 for call back at a later time",
                    "Press 3 to hang up"
                ],
                "customer_responses": {
                    "positive": [
                        "I want to pay this now",
                        "Yes, I'll make a payment",
                        "I can pay today",
                        "Let me pay this off",
                        "I'll take care of this right away"
                    ],
                    "suspicious": [
                        "I don't believe this is legitimate",
                        "I need to verify this debt first",
                        "I'm going to call the company directly",
                        "This sounds like a scam",
                        "I don't recognize this debt"
                    ],
                    "busy": [
                        "I'm busy right now, call back later",
                        "I can't deal with this now",
                        "I'm at work, call me back",
                        "I don't have time for this",
                        "Can you call back tomorrow?"
                    ],
                    "confused": [
                        "I don't understand what this is about",
                        "Can you explain this debt to me?",
                        "I don't remember this charge",
                        "What is this for exactly?",
                        "I need more information about this"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about resolving your account and finding a solution.",
                    "busy": "I know you're busy, but this affects your credit. Let's resolve this quickly.",
                    "not_interested": "This isn't optional - we need to resolve your outstanding balance."
                },
                "compliance_notes": "Must follow FDCPA regulations, maintain professional conduct, offer payment options"
            },
            
            # Technology
            "tech_support": {
                "name": "Tech Support",
                "tone": "helpful, patient, technical",
                "phrases": [
                    "Technical issue detected",
                    "System maintenance",
                    "Account security",
                    "Software update",
                    "Troubleshooting required"
                ],
                "customer_responses": {
                    "positive": [
                        "Yes, I've been having problems with my computer.",
                        "I need help with this technical issue.",
                        "What do you need me to do?",
                        "I'm ready to follow your instructions.",
                        "Let's get this fixed right away."
                    ],
                    "suspicious": [
                        "I don't trust remote access calls. How do I know you're legitimate?",
                        "This sounds like a scam. I'm not giving you access to my computer.",
                        "I need to verify who you are first.",
                        "I'm going to call the company directly to check this.",
                        "I don't believe this is a real tech support call."
                    ],
                    "busy": [
                        "I'm really busy right now. Can you call back later?",
                        "I don't have time for this technical stuff right now.",
                        "I'm in the middle of something important.",
                        "Can we schedule this for another time?",
                        "I'm not available right now."
                    ],
                    "confused": [
                        "I don't understand what the technical problem is.",
                        "Can you explain this in simpler terms?",
                        "What exactly is wrong with my computer?",
                        "I'm not very technical, can you help me understand?",
                        "Can you walk me through this step by step?"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about fixing your technical issue and securing your account.",
                    "busy": "I know you're busy, but this technical issue needs immediate attention to prevent further problems.",
                    "not_interested": "This technical issue will only get worse if we don't fix it now."
                },
                "compliance_notes": "Must verify user identity, maintain system security, provide technical assistance"
            },
            
            "software_sales": {
                "name": "Software Sales",
                "tone": "enthusiastic, professional, solution-focused",
                "phrases": [
                    "Software solution",
                    "Productivity improvement",
                    "Cost savings",
                    "Efficiency boost",
                    "Business growth"
                ],
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about improving your business with proven software solutions.",
                    "busy": "I know you're busy, which is exactly why this software will save you time and money.",
                    "not_interested": "This software could revolutionize your business operations and increase your profits."
                },
                "compliance_notes": "Must provide accurate product information, maintain sales ethics, offer legitimate solutions"
            },
            
            # Sales & Marketing
            "lead_generation": {
                "name": "Lead Generation",
                "tone": "professional, curious, engaging",
                "phrases": [
                    "Business opportunity",
                    "Market research",
                    "Industry insights",
                    "Growth potential",
                    "Competitive advantage"
                ],
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about legitimate business opportunities and market research.",
                    "busy": "I know you're busy, which is why I'll be brief. This could significantly impact your business.",
                    "not_interested": "This opportunity could transform your business. Let me explain how."
                },
                "compliance_notes": "Must provide accurate information, respect privacy, maintain professional standards"
            },
            
            "cold_calling": {
                "name": "Cold Calling",
                "tone": "confident, persistent, professional",
                "phrases": [
                    "Business opportunity",
                    "Quick question",
                    "Value proposition",
                    "Time-sensitive offer",
                    "Exclusive opportunity"
                ],
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about legitimate business opportunities and value.",
                    "busy": "I know you're busy, which is why I'll be brief. This could significantly impact your business.",
                    "not_interested": "This opportunity could transform your business. Let me explain how."
                },
                "compliance_notes": "Must respect do-not-call lists, maintain professional conduct, provide accurate information"
            },
            
            # Customer Service
            "customer_support": {
                "name": "Customer Support",
                "tone": "helpful, patient, solution-focused",
                "phrases": [
                    "How can I help you",
                    "Account assistance",
                    "Issue resolution",
                    "Customer satisfaction",
                    "Service improvement"
                ],
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about helping you with your account and resolving any issues.",
                    "busy": "I know you're busy, which is why I'll help you quickly resolve this issue.",
                    "not_interested": "This is about improving your experience and resolving any problems you may have."
                },
                "compliance_notes": "Must verify customer identity, maintain service standards, resolve issues effectively"
            },
            
            "complaint_handling": {
                "name": "Complaint Handling",
                "tone": "apologetic, empathetic, solution-focused",
                "phrases": [
                    "I sincerely apologize",
                    "We value your feedback",
                    "Let me resolve this",
                    "Customer satisfaction is our priority",
                    "We'll make this right"
                ],
                "objection_handling": {
                    "suspicious": "I understand your concern. This is about making things right and ensuring your satisfaction.",
                    "busy": "I know you're busy, which is why I'll resolve this quickly and efficiently.",
                    "not_interested": "This is about fixing the problem and ensuring you're completely satisfied."
                },
                "compliance_notes": "Must address complaints professionally, maintain customer satisfaction, resolve issues effectively"
            },
            
            # Additional Script Types
            "fraud": {
                "name": "Fraud Prevention",
                "tone": "urgent_but_calm, professional",
                "phrases": [
                    "This is an urgent security call from [Company]",
                    "We've detected suspicious activity on your account",
                    "We need to verify this transaction immediately",
                    "This is to protect your account from fraud",
                    "Please confirm this activity is authorized by you"
                ],
                "customer_responses": {
                    "positive": [
                        "Yes, that's me",
                        "I authorized that transaction",
                        "Thank you for calling about this",
                        "I'm glad you caught this",
                        "What do I need to do?"
                    ],
                    "suspicious": [
                        "I don't trust this call",
                        "This seems like a scam",
                        "I need to call the bank directly",
                        "I'm not giving you any information",
                        "I'm hanging up now"
                    ],
                    "busy": [
                        "I'm busy right now",
                        "Can this wait?",
                        "I don't have time for this",
                        "Call me back later",
                        "I'm in a meeting"
                    ],
                    "confused": [
                        "I don't understand what happened",
                        "What activity are you talking about?",
                        "Can you explain what you detected?",
                        "I don't remember doing that",
                        "What account is this about?"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I understand your concern about security. This is exactly why we're calling - to protect your account from fraud.",
                    "busy": "This is urgent and time-sensitive. We need to act quickly to protect your account.",
                    "confused": "Don't worry, we're here to help. This is just a verification call to ensure your account is secure."
                },
                "compliance_notes": "Must follow strict fraud prevention protocols and never ask for full account details."
            },
            "shopping": {
                "name": "Shopping/E-commerce",
                "tone": "friendly, helpful, enthusiastic",
                "phrases": [
                    "Thank you for your recent order with [Store]",
                    "I'm calling about your recent purchase",
                    "We have an update on your order",
                    "Your order is ready for delivery",
                    "We need to confirm some details for your order"
                ],
                "customer_responses": {
                    "positive": [
                        "That's great news!",
                        "I'm excited to receive it",
                        "When will it arrive?",
                        "Perfect, thank you for the update",
                        "I can't wait to get it"
                    ],
                    "suspicious": [
                        "I didn't order anything",
                        "This seems suspicious",
                        "I need to check my account",
                        "I don't remember placing an order",
                        "This might be a scam"
                    ],
                    "busy": [
                        "I'm busy right now",
                        "Can you call back later?",
                        "I don't have time for this",
                        "I'm in the middle of something",
                        "Not right now, sorry"
                    ],
                    "confused": [
                        "I don't remember ordering anything",
                        "What order are you talking about?",
                        "Can you explain what I ordered?",
                        "I'm not sure about this",
                        "What's this about?"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I understand your concern. This is a legitimate call from [Store] about your recent order.",
                    "busy": "I know you're busy. This will only take a moment to confirm your order details.",
                    "confused": "Let me help clarify what this is about. You recently placed an order with us."
                },
                "compliance_notes": "Must comply with consumer protection laws and data privacy regulations."
            },
            "utilities": {
                "name": "Utilities",
                "tone": "helpful, professional, informative",
                "phrases": [
                    "This is regarding your utility account",
                    "We need to discuss your service",
                    "This is about your bill",
                    "We're here to help with your account",
                    "This is an important update about your service"
                ],
                "customer_responses": {
                    "positive": [
                        "That's helpful, thank you",
                        "I appreciate the information",
                        "What do I need to do?",
                        "This is good to know",
                        "Thank you for calling"
                    ],
                    "suspicious": [
                        "I'm not sure about this",
                        "This seems suspicious",
                        "I need to verify this",
                        "I don't trust this call",
                        "I'm going to call the company directly"
                    ],
                    "busy": [
                        "I'm busy right now",
                        "Can you call back later?",
                        "I don't have time for this",
                        "I'm in a meeting",
                        "Not right now"
                    ],
                    "confused": [
                        "I don't understand what this is about",
                        "What account are you talking about?",
                        "Can you explain this more clearly?",
                        "I'm not sure what you mean",
                        "What's this regarding?"
                    ]
                },
                "objection_handling": {
                    "suspicious": "I understand your concern. This is a legitimate call from [Utility Company] about your account.",
                    "busy": "I know your time is valuable. This is regarding an important matter with your utility service.",
                    "confused": "Let me explain this clearly. This is about your utility account with us."
                },
                "compliance_notes": "Must comply with utility regulations and consumer protection laws."
            }
        }
    
    def get_script_mode(self, mode_id: str) -> Optional[Dict[str, Any]]:
        """Get script mode configuration by ID"""
        return self.script_modes.get(mode_id)
    
    def get_mode_config(self, mode_id: str) -> Dict[str, Any]:
        """Get configuration for a specific script mode (alias for get_script_mode)"""
        return self.script_modes.get(mode_id, {
            "name": "General",
            "tone": "professional",
            "department": "customer service",
            "customer_responses": {},
            "objection_handling": {},
            "compliance_notes": "Follow standard compliance procedures"
        })
    
    def get_all_modes(self) -> Dict[str, Dict[str, Any]]:
        """Get all available script modes"""
        return self.script_modes
    
    def get_mode_phrases(self, mode_id: str) -> List[str]:
        """Get industry-specific phrases for a mode"""
        mode = self.get_script_mode(mode_id)
        return mode.get("phrases", []) if mode else []
    
    def get_mode_tone(self, mode_id: str) -> str:
        """Get industry-specific tone for a mode"""
        mode = self.get_script_mode(mode_id)
        return mode.get("tone", "professional") if mode else "professional"
    
    def get_mode_objection_handling(self, mode_id: str) -> Dict[str, str]:
        """Get industry-specific objection handling for a mode"""
        mode = self.get_script_mode(mode_id)
        return mode.get("objection_handling", {}) if mode else {}
    
    def get_mode_compliance_notes(self, mode_id: str) -> str:
        """Get compliance notes for a mode"""
        mode = self.get_script_mode(mode_id)
        return mode.get("compliance_notes", "") if mode else ""
    
    def get_customer_responses(self, mode_id: str, response_type: str = "positive") -> List[str]:
        """Get customer responses for a specific mode and response type"""
        mode = self.get_script_mode(mode_id)
        if not mode or "customer_responses" not in mode:
            return []
        
        responses = mode["customer_responses"]
        return responses.get(response_type, [])
    
    def get_all_customer_response_types(self, mode_id: str) -> List[str]:
        """Get all available customer response types for a mode"""
        mode = self.get_script_mode(mode_id)
        if not mode or "customer_responses" not in mode:
            return []
        
        return list(mode["customer_responses"].keys())
    
    def generate_mode_specific_prompt(self, mode_id: str, call_type: str, product_info: str) -> str:
        """Generate a mode-specific prompt for script generation"""
        mode = self.get_script_mode(mode_id)
        if not mode:
            return product_info
        
        tone = mode.get("tone", "professional")
        compliance = mode.get("compliance_notes", "")
        
        prompt_parts = [
            f"Create a {mode['name']} call script with a {tone} tone.",
            f"Call Type: {call_type.title()}",
            f"Industry: {mode['name']}",
            f"User's Request: {product_info}",
            "",
            f"Tone Requirements: {tone}",
            f"Industry Phrases: {', '.join(mode.get('phrases', [])[:3])}",
            "",
            f"Compliance Notes: {compliance}",
            "",
            "Generate a professional, industry-appropriate script that:",
            "1. Uses industry-specific language and terminology",
            "2. Follows compliance requirements",
            "3. Addresses the user's specific request",
            "4. Maintains professional standards",
            "5. Includes appropriate objection handling"
        ]
        
        return "\n".join(prompt_parts)
