import os
import tempfile
from typing import Optional
import pyttsx3
from gtts import gTTS
import io

class TTSService:
    def __init__(self):
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a good voice
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            print(f"TTS engine initialization failed: {e}")
            self.engine = None
    
    def text_to_speech(self, text: str, output_format: str = "mp3", voice: str = "default") -> Optional[bytes]:
        """Convert text to speech and return audio data"""
        try:
            if voice == "default" and self.engine:
                return self._generate_with_pyttsx3(text)
            else:
                return self._generate_with_gtts(text, voice)
        except Exception as e:
            print(f"TTS generation failed: {e}")
            return None
    
    def _generate_with_pyttsx3(self, text: str) -> bytes:
        """Generate speech using pyttsx3 (offline)"""
        if not self.engine:
            raise Exception("TTS engine not initialized")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Save to temporary file
            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()
            
            # Read the file
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            return audio_data
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _generate_with_gtts(self, text: str, voice: str = "default") -> bytes:
        """Generate speech using gTTS (online)"""
        # Map voice names to gTTS languages
        voice_map = {
            "default": "en",
            "british": "en-co.uk",
            "australian": "en-au",
            "american": "en-us",
            "canadian": "en-ca"
        }
        
        lang = voice_map.get(voice, "en")
        
        # Generate TTS
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to bytes
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.getvalue()
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        voices = []
        
        # Add gTTS voices
        voices.extend([
            {"name": "Default English", "id": "default", "provider": "gTTS"},
            {"name": "British English", "id": "british", "provider": "gTTS"},
            {"name": "Australian English", "id": "australian", "provider": "gTTS"},
            {"name": "American English", "id": "american", "provider": "gTTS"},
            {"name": "Canadian English", "id": "canadian", "provider": "gTTS"}
        ])
        
        # Add pyttsx3 voices if available
        if self.engine:
            try:
                system_voices = self.engine.getProperty('voices')
                for voice in system_voices:
                    voices.append({
                        "name": voice.name,
                        "id": voice.id,
                        "provider": "pyttsx3"
                    })
            except:
                pass
        
        return voices
    
    def create_audio_file(self, text: str, filename: str, voice: str = "default") -> bool:
        """Create an audio file from text"""
        try:
            audio_data = self.text_to_speech(text, voice=voice)
            if audio_data:
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                return True
            return False
        except Exception as e:
            print(f"Audio file creation failed: {e}")
            return False
