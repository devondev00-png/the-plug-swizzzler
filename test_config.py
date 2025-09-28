#!/usr/bin/env python3
"""
Test configuration loading
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set a test API key
os.environ["OPENAI_API_KEY"] = "sk-test-key-for-testing"

try:
    from config import settings, validate_settings
    
    print("Testing configuration...")
    print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY[:10]}...")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"TTS_ENGINE: {settings.TTS_ENGINE}")
    
    # Test validation
    validate_settings()
    print("Configuration validation passed!")
    
except Exception as e:
    print(f"Configuration test failed: {e}")
    import traceback
    traceback.print_exc()
