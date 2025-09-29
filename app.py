from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="The Plug Swizzler")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>The Plug Swizzler</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 The Plug Swizzler</h1>
            <div class="status">
                <strong>✅ System Online</strong><br>
                AI-Powered Call Script Generator is ready!
            </div>
            <p>Your app is working perfectly!</p>
            <h2>Features:</h2>
            <ul>
                <li>🤖 AI Script Generation</li>
                <li>🎯 Custom Training</li>
                <li>📞 Objection Handling</li>
                <li>📊 Analytics</li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "The Plug Swizzler is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
