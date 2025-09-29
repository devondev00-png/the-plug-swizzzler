#!/usr/bin/env python3
"""
Simple HTML version of The Plug Swizzler
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="The Plug Swizzler", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Plug Swizzler</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 600px;
                margin: 20px;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .feature {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .feature h3 {
                color: #333;
                margin: 0 0 10px 0;
            }
            .feature p {
                color: #666;
                margin: 0;
                font-size: 0.9em;
            }
            .cta {
                background: #667eea;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                margin: 20px 0;
                text-decoration: none;
                display: inline-block;
            }
            .cta:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
            }
            .status {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #28a745;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 The Plug Swizzler</h1>
            <p class="subtitle">AI-Powered Call Script Generator</p>
            
            <div class="status">
                <strong>✅ System Online</strong><br>
                Your AI call script generator is ready to use!
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🤖 AI Script Generation</h3>
                    <p>Generate personalized call scripts using advanced AI technology</p>
                </div>
                <div class="feature">
                    <h3>🎯 Custom Training</h3>
                    <p>Train the AI with your company's voice and style</p>
                </div>
                <div class="feature">
                    <h3>📞 Objection Handling</h3>
                    <p>Built-in objection handling templates and responses</p>
                </div>
                <div class="feature">
                    <h3>📊 Analytics</h3>
                    <p>Track script performance and optimize your calls</p>
                </div>
            </div>
            
            <a href="/api" class="cta">View API Documentation</a>
            
            <p style="margin-top: 30px; color: #666; font-size: 0.9em;">
                Ready to generate your first call script? The API is fully functional!
            </p>
        </div>
    </body>
    </html>
    """

@app.get("/api")
async def api_docs():
    return {
        "message": "The Plug Swizzler API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "generate_script": "/generate-script",
            "training_data": "/training-data",
            "objections": "/objections",
            "companies": "/companies",
            "scripts": "/scripts",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
