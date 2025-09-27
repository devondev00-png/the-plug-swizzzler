from typing import Dict, List, Any, Optional

class HumanizedVoiceService:
    """Service for managing humanized voice options (accents, genders, ages)"""
    
    def get_humanized_voices(self) -> List[Dict[str, Any]]:
        """Get all humanized voice options"""
        return self.get_all_voices()
    
    def get_all_voices(self) -> List[Dict[str, Any]]:
        """Get all humanized voice options (alias for get_humanized_voices)"""
        return [
            # British Accents
            {
                "id": "british_man_young",
                "name": "Young British Man",
                "description": "Friendly, energetic British male voice (20-30)",
                "accent": "British",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "energetic",
                "phrases": [
                    "Hi there, how are you doing today?",
                    "I hope I'm not catching you at a bad time",
                    "I just wanted to have a quick chat with you",
                    "That sounds brilliant, let me tell you more",
                    "Thanks so much for your time today"
                ],
                "objection_handling": {
                    "price": "I totally get that cost is important. Let me show you how this actually saves you money.",
                    "time": "I know you're probably busy, but this will only take a couple of minutes.",
                    "skepticism": "I completely understand your hesitation. Let me explain why this is different."
                }
            },
            # Scottish Accents
            {
                "id": "scottish_man_young",
                "name": "Young Scottish Man",
                "description": "Friendly Scottish male voice with local expressions (20-30)",
                "accent": "Scottish",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "local",
                "phrases": [
                    "Hiya, how are you getting on?",
                    "I hope I'm no bothering you",
                    "I just wanted to have a wee chat",
                    "That sounds brilliant, let me tell you more",
                    "Thanks very much for your time"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. This will actually save you money in the long run.",
                    "time": "I know you're probably busy, but this will only take a few minutes.",
                    "skepticism": "I completely understand your hesitation. Let me explain why this is different."
                }
            },
            # Irish Accents
            {
                "id": "irish_man_young",
                "name": "Young Irish Man",
                "description": "Friendly Irish male voice with local expressions (20-30)",
                "accent": "Irish",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "warm",
                "phrases": [
                    "Hello there, how are you keeping?",
                    "I hope I'm not disturbing you",
                    "I just wanted to have a quick word",
                    "That sounds grand, let me tell you more",
                    "Thanks a million for your time"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. This will actually save you money in the long run.",
                    "time": "I know you're probably busy, but this will only take a few minutes.",
                    "skepticism": "I completely understand your hesitation. Let me explain why this is different."
                }
            },
            # Australian Accents
            {
                "id": "australian_man_young",
                "name": "Young Australian Man",
                "description": "Friendly Australian male voice with local expressions (20-30)",
                "accent": "Australian",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "casual",
                "phrases": [
                    "G'day, how are you going?",
                    "I hope I'm not catching you at a bad time",
                    "I just wanted to have a quick chat",
                    "That sounds great, let me tell you more",
                    "Thanks heaps for your time"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. This will actually save you money in the long run.",
                    "time": "I know you're probably flat out, but this will only take a few minutes.",
                    "skepticism": "I completely understand your hesitation. Let me explain why this is different."
                }
            },
            # French Accents (with French phrases)
            {
                "id": "french_man_young",
                "name": "Young French Man",
                "description": "Professional French male voice with French expressions (20-30)",
                "accent": "French",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "professional",
                "style": "sophisticated",
                "phrases": [
                    "Bonjour, comment allez-vous?",
                    "J'espère que je ne vous dérange pas",
                    "Je voulais juste avoir une petite conversation",
                    "Cela semble excellent, laissez-moi vous en dire plus",
                    "Merci beaucoup pour votre temps"
                ],
                "objection_handling": {
                    "price": "Je comprends que le coût est important. Cela vous fera économiser de l'argent à long terme.",
                    "time": "Je sais que vous êtes probablement occupé, mais cela ne prendra que quelques minutes.",
                    "skepticism": "Je comprends parfaitement votre hésitation. Laissez-moi vous expliquer pourquoi c'est différent."
                }
            },
            # German Accents (with German phrases)
            {
                "id": "german_man_young",
                "name": "Young German Man",
                "description": "Professional German male voice with German expressions (20-30)",
                "accent": "German",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "professional",
                "style": "efficient",
                "phrases": [
                    "Guten Tag, wie geht es Ihnen?",
                    "Ich hoffe, ich störe Sie nicht",
                    "Ich wollte nur kurz mit Ihnen sprechen",
                    "Das klingt ausgezeichnet, lassen Sie mich mehr erzählen",
                    "Vielen Dank für Ihre Zeit"
                ],
                "objection_handling": {
                    "price": "Ich verstehe, dass Kosten wichtig sind. Das wird Ihnen langfristig Geld sparen.",
                    "time": "Ich weiß, dass Sie wahrscheinlich beschäftigt sind, aber das dauert nur wenige Minuten.",
                    "skepticism": "Ich verstehe Ihre Bedenken vollkommen. Lassen Sie mich erklären, warum das anders ist."
                }
            },
            # Spanish Accents (with Spanish phrases)
            {
                "id": "spanish_man_young",
                "name": "Young Spanish Man",
                "description": "Friendly Spanish male voice with Spanish expressions (20-30)",
                "accent": "Spanish",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "warm",
                "phrases": [
                    "Hola, ¿cómo está usted?",
                    "Espero no molestarle",
                    "Solo quería tener una pequeña conversación",
                    "Eso suena excelente, déjeme contarle más",
                    "Muchas gracias por su tiempo"
                ],
                "objection_handling": {
                    "price": "Entiendo que el costo es importante. Esto le ahorrará dinero a largo plazo.",
                    "time": "Sé que probablemente está ocupado, pero esto solo tomará unos minutos.",
                    "skepticism": "Entiendo completamente su hesitación. Déjeme explicarle por qué esto es diferente."
                }
            },
            # Italian Accents (with Italian phrases)
            {
                "id": "italian_man_young",
                "name": "Young Italian Man",
                "description": "Friendly Italian male voice with Italian expressions (20-30)",
                "accent": "Italian",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "passionate",
                "phrases": [
                    "Ciao, come sta?",
                    "Spero di non disturbarla",
                    "Volevo solo fare una piccola chiacchierata",
                    "Sembra fantastico, lasciami raccontare di più",
                    "Grazie mille per il suo tempo"
                ],
                "objection_handling": {
                    "price": "Capisco che il costo è importante. Questo vi farà risparmiare denaro a lungo termine.",
                    "time": "So che probabilmente è occupato, ma questo richiederà solo pochi minuti.",
                    "skepticism": "Capisco completamente la sua esitazione. Lasciami spiegare perché questo è diverso."
                }
            },
            # Canadian Accents
            {
                "id": "canadian_man_young",
                "name": "Young Canadian Man",
                "description": "Friendly Canadian male voice with local expressions (20-30)",
                "accent": "Canadian",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "polite",
                "phrases": [
                    "Hello there, how are you doing?",
                    "I hope I'm not bothering you",
                    "I just wanted to have a quick chat",
                    "That sounds great, let me tell you more",
                    "Thanks so much for your time"
                ],
                "objection_handling": {
                    "price": "I understand cost is important. This will actually save you money in the long run.",
                    "time": "I know you're probably busy, but this will only take a few minutes.",
                    "skepticism": "I completely understand your hesitation. Let me explain why this is different."
                }
            },
            {
                "id": "british_man_middle",
                "name": "Middle-aged British Man",
                "description": "Professional, trustworthy British male voice (35-50)",
                "accent": "British",
                "gender": "Male",
                "age_range": "35-50",
                "tone": "professional",
                "style": "trustworthy",
                "phrases": [
                    "Good day, I hope you're well",
                    "I'm calling to discuss something that might interest you",
                    "I understand your concerns, let me address them",
                    "This could really benefit you and your family",
                    "I appreciate you taking the time to listen"
                ],
                "objection_handling": {
                    "price": "I understand your concerns about cost. This investment will pay for itself quickly.",
                    "time": "I appreciate your time. This consultation could save you significant money.",
                    "skepticism": "I understand your caution. I've been in this business for years and this is legitimate."
                }
            },
            {
                "id": "british_woman_young",
                "name": "Young British Woman",
                "description": "Warm, approachable British female voice (20-30)",
                "accent": "British",
                "gender": "Female",
                "age_range": "20-30",
                "tone": "warm",
                "style": "approachable",
                "phrases": [
                    "Hello, I hope you're having a lovely day",
                    "I'm calling to share something exciting with you",
                    "I completely understand where you're coming from",
                    "This could really make a difference for you",
                    "Thank you so much for listening to me"
                ],
                "objection_handling": {
                    "price": "I know money is tight for everyone right now. This actually helps you save money.",
                    "time": "I know you're probably really busy, but this could change your situation.",
                    "skepticism": "I totally get why you'd be skeptical. Let me explain why this is different."
                }
            },
            {
                "id": "british_woman_middle",
                "name": "Middle-aged British Woman",
                "description": "Caring, experienced British female voice (35-50)",
                "accent": "British",
                "gender": "Female",
                "age_range": "35-50",
                "tone": "caring",
                "style": "experienced",
                "phrases": [
                    "Good morning, I hope you're keeping well",
                    "I'm calling because I think this could help you",
                    "I understand your situation completely",
                    "This has helped many people in your position",
                    "I really appreciate you giving me your time"
                ],
                "objection_handling": {
                    "price": "I understand your budget concerns. This is designed to help people save money.",
                    "time": "I know your time is precious. This could make a real difference to your situation.",
                    "skepticism": "I understand your hesitation. I've helped many people in similar situations."
                }
            },
            {
                "id": "scottish_man",
                "name": "Scottish Man",
                "description": "Friendly, authentic Scottish male voice",
                "accent": "Scottish",
                "gender": "Male",
                "age_range": "30-50",
                "tone": "friendly",
                "style": "authentic",
                "phrases": [
                    "Hello there, how are you doing?",
                    "I'm calling to tell you about something that might interest you",
                    "I can see why you'd be concerned about that",
                    "This could really help you out, you know",
                    "Thanks for taking the time to speak with me"
                ],
                "objection_handling": {
                    "price": "Aye, I understand money's tight. This actually helps you save in the long run.",
                    "time": "I know you're busy, but this will only take a wee minute.",
                    "skepticism": "I can see why you'd be wary. Let me explain why this is genuine."
                }
            },
            {
                "id": "scottish_woman",
                "name": "Scottish Woman",
                "description": "Warm, genuine Scottish female voice",
                "accent": "Scottish",
                "gender": "Female",
                "age_range": "30-50",
                "tone": "warm",
                "style": "genuine",
                "phrases": [
                    "Hello, I hope you're keeping well",
                    "I'm calling to share something that might help you",
                    "I completely understand your concerns",
                    "This has helped many people like yourself",
                    "Thank you so much for your time today"
                ],
                "objection_handling": {
                    "price": "I know money's tight for everyone. This is designed to help you save.",
                    "time": "I understand you're busy, but this could really help your situation.",
                    "skepticism": "I can see why you'd be cautious. Let me explain why this is legitimate."
                }
            },
            {
                "id": "irish_man",
                "name": "Irish Man",
                "description": "Charming, conversational Irish male voice",
                "accent": "Irish",
                "gender": "Male",
                "age_range": "30-50",
                "tone": "charming",
                "style": "conversational",
                "phrases": [
                    "Hello there, how are you getting on?",
                    "I'm calling to tell you about something that might interest you",
                    "I can see why you'd have concerns about that",
                    "This could really make a difference for you",
                    "Thanks for taking the time to chat with me"
                ],
                "objection_handling": {
                    "price": "I understand money's tight for everyone. This actually helps you save money.",
                    "time": "I know you're probably busy, but this will only take a few minutes.",
                    "skepticism": "I can see why you'd be skeptical. Let me explain why this is different."
                }
            },
            {
                "id": "irish_woman",
                "name": "Irish Woman",
                "description": "Kind, empathetic Irish female voice",
                "accent": "Irish",
                "gender": "Female",
                "age_range": "30-50",
                "tone": "kind",
                "style": "empathetic",
                "phrases": [
                    "Hello, I hope you're keeping well",
                    "I'm calling because I think this could help you",
                    "I completely understand your situation",
                    "This has helped many people in your position",
                    "I really appreciate you giving me your time"
                ],
                "objection_handling": {
                    "price": "I know money's tight for everyone. This is designed to help you save.",
                    "time": "I understand you're busy, but this could really help your situation.",
                    "skepticism": "I can see why you'd be cautious. Let me explain why this is legitimate."
                }
            },
            # American Accents
            {
                "id": "american_man_young",
                "name": "Young American Man",
                "description": "Energetic, confident American male voice (20-30)",
                "accent": "American",
                "gender": "Male",
                "age_range": "20-30",
                "tone": "energetic",
                "style": "confident",
                "phrases": [
                    "Hey there, how's it going?",
                    "I'm calling to tell you about something awesome",
                    "I totally get where you're coming from",
                    "This could really change things for you",
                    "Thanks for taking the time to talk with me"
                ],
                "objection_handling": {
                    "price": "I totally understand cost is a concern. This actually saves you money in the long run.",
                    "time": "I know you're probably busy, but this will only take a couple of minutes.",
                    "skepticism": "I completely get why you'd be skeptical. Let me explain why this is different."
                }
            },
            {
                "id": "american_man_middle",
                "name": "Middle-aged American Man",
                "description": "Professional, experienced American male voice (35-50)",
                "accent": "American",
                "gender": "Male",
                "age_range": "35-50",
                "tone": "professional",
                "style": "experienced",
                "phrases": [
                    "Good day, I hope you're doing well",
                    "I'm calling to discuss something that might benefit you",
                    "I understand your concerns, let me address them",
                    "This could really help you and your family",
                    "I appreciate you taking the time to listen"
                ],
                "objection_handling": {
                    "price": "I understand your concerns about cost. This investment will pay for itself quickly.",
                    "time": "I appreciate your time. This consultation could save you significant money.",
                    "skepticism": "I understand your caution. I've been in this business for years and this is legitimate."
                }
            },
            {
                "id": "american_woman_young",
                "name": "Young American Woman",
                "description": "Friendly, enthusiastic American female voice (20-30)",
                "accent": "American",
                "gender": "Female",
                "age_range": "20-30",
                "tone": "friendly",
                "style": "enthusiastic",
                "phrases": [
                    "Hi there, I hope you're having a great day",
                    "I'm calling to share something exciting with you",
                    "I completely understand where you're coming from",
                    "This could really make a difference for you",
                    "Thank you so much for listening to me"
                ],
                "objection_handling": {
                    "price": "I know money is tight for everyone right now. This actually helps you save money.",
                    "time": "I know you're probably really busy, but this could change your situation.",
                    "skepticism": "I totally get why you'd be skeptical. Let me explain why this is different."
                }
            },
            {
                "id": "american_woman_middle",
                "name": "Middle-aged American Woman",
                "description": "Caring, professional American female voice (35-50)",
                "accent": "American",
                "gender": "Female",
                "age_range": "35-50",
                "tone": "caring",
                "style": "professional",
                "phrases": [
                    "Good morning, I hope you're keeping well",
                    "I'm calling because I think this could help you",
                    "I understand your situation completely",
                    "This has helped many people in your position",
                    "I really appreciate you giving me your time"
                ],
                "objection_handling": {
                    "price": "I understand your budget concerns. This is designed to help people save money.",
                    "time": "I know your time is precious. This could make a real difference to your situation.",
                    "skepticism": "I understand your hesitation. I've helped many people in similar situations."
                }
            },
            # Australian Accents
            {
                "id": "australian_man",
                "name": "Australian Man",
                "description": "Relaxed, friendly Australian male voice",
                "accent": "Australian",
                "gender": "Male",
                "age_range": "30-50",
                "tone": "relaxed",
                "style": "friendly",
                "phrases": [
                    "G'day, how are you going?",
                    "I'm calling to tell you about something that might interest you",
                    "I can see why you'd be concerned about that",
                    "This could really help you out, mate",
                    "Thanks for taking the time to have a chat"
                ],
                "objection_handling": {
                    "price": "I understand money's tight for everyone. This actually helps you save in the long run.",
                    "time": "I know you're probably busy, but this will only take a few minutes.",
                    "skepticism": "I can see why you'd be skeptical. Let me explain why this is different."
                }
            },
            {
                "id": "australian_woman",
                "name": "Australian Woman",
                "description": "Warm, genuine Australian female voice",
                "accent": "Australian",
                "gender": "Female",
                "age_range": "30-50",
                "tone": "warm",
                "style": "genuine",
                "phrases": [
                    "Hello, I hope you're keeping well",
                    "I'm calling to share something that might help you",
                    "I completely understand your concerns",
                    "This has helped many people like yourself",
                    "Thank you so much for your time today"
                ],
                "objection_handling": {
                    "price": "I know money's tight for everyone. This is designed to help you save.",
                    "time": "I understand you're busy, but this could really help your situation.",
                    "skepticism": "I can see why you'd be cautious. Let me explain why this is legitimate."
                }
            },
            # Canadian Accents
            {
                "id": "canadian_man",
                "name": "Canadian Man",
                "description": "Polite, professional Canadian male voice",
                "accent": "Canadian",
                "gender": "Male",
                "age_range": "30-50",
                "tone": "polite",
                "style": "professional",
                "phrases": [
                    "Hello there, how are you doing today?",
                    "I'm calling to tell you about something that might interest you",
                    "I can see why you'd have concerns about that",
                    "This could really make a difference for you",
                    "Thanks for taking the time to speak with me"
                ],
                "objection_handling": {
                    "price": "I understand money's tight for everyone. This actually helps you save money.",
                    "time": "I know you're probably busy, but this will only take a few minutes.",
                    "skepticism": "I can see why you'd be skeptical. Let me explain why this is different."
                }
            },
            {
                "id": "canadian_woman",
                "name": "Canadian Woman",
                "description": "Kind, helpful Canadian female voice",
                "accent": "Canadian",
                "gender": "Female",
                "age_range": "30-50",
                "tone": "kind",
                "style": "helpful",
                "phrases": [
                    "Hello, I hope you're keeping well",
                    "I'm calling because I think this could help you",
                    "I completely understand your situation",
                    "This has helped many people in your position",
                    "I really appreciate you giving me your time"
                ],
                "objection_handling": {
                    "price": "I know money's tight for everyone. This is designed to help you save.",
                    "time": "I understand you're busy, but this could really help your situation.",
                    "skepticism": "I can see why you'd be cautious. Let me explain why this is legitimate."
                }
            }
        ]
    
    def get_voice_template(self, voice_id: str) -> Optional[Dict[str, Any]]:
        """Get specific humanized voice template by ID"""
        voices = self.get_humanized_voices()
        for voice in voices:
            if voice["id"] == voice_id:
                return voice
        return None
    
    def get_voices_by_accent(self, accent: str) -> List[Dict[str, Any]]:
        """Get all voices for a specific accent"""
        voices = self.get_humanized_voices()
        return [voice for voice in voices if voice["accent"].lower() == accent.lower()]
    
    def get_voices_by_gender(self, gender: str) -> List[Dict[str, Any]]:
        """Get all voices for a specific gender"""
        voices = self.get_humanized_voices()
        return [voice for voice in voices if voice["gender"].lower() == gender.lower()]
    
    def get_voices_by_age_range(self, age_range: str) -> List[Dict[str, Any]]:
        """Get all voices for a specific age range"""
        voices = self.get_humanized_voices()
        return [voice for voice in voices if voice["age_range"] == age_range]
    
    def get_available_accents(self) -> List[str]:
        """Get list of available accents"""
        voices = self.get_humanized_voices()
        accents = list(set([voice["accent"] for voice in voices]))
        return sorted(accents)
    
    def get_available_genders(self) -> List[str]:
        """Get list of available genders"""
        voices = self.get_humanized_voices()
        genders = list(set([voice["gender"] for voice in voices]))
        return sorted(genders)
    
    def get_available_age_ranges(self) -> List[str]:
        """Get list of available age ranges"""
        voices = self.get_humanized_voices()
        age_ranges = list(set([voice["age_range"] for voice in voices]))
        return sorted(age_ranges)


