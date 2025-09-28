#!/usr/bin/env python3
"""
Minimal run script
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from minimal_config import settings, validate_settings

def main():
    """Main entry point for the application"""
    try:
        # Validate settings
        validate_settings()
        print("Starting The Plug Swizzler...")
        print(f"Debug mode: {settings.DEBUG}")
        print(f"Database: {settings.DATABASE_URL}")
        print(f"OpenAI Model: {settings.OPENAI_MODEL}")
        
        # Create necessary directories
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True
        )
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your environment variables.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()