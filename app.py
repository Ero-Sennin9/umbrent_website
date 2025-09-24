from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Логирование при старте
@app.on_event("startup")
async def startup_event():
    print("🚀 Server starting up...")
    print("📁 Current directory:", os.getcwd())
    print("📁 Static files path:", os.path.abspath('static'))

os.makedirs('static', exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Создаем дефолтную страницу если её нет
if not os.path.exists('static/index.html'):
    with open('static/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Umbrent Website</title>
    <style>
        body {
            font-family: Arial;
            background: #667eea;
            color: white;
            text-align: center;
            padding: 100px;
        }
    </style>
</head>
<body>
    <h1>Umbrent Website</h1>
    <p>Сайт работает!</p>
</body>
</html>""")
    print("📄 Created default index.html")

@app.get("/")
async def read_root():
    print("📨 GET / request received")
    return FileResponse('static/index.html')

@app.get("/health")
async def health_check():
    print("❤️ Health check request")
    return {"status": "healthy"}

@app.get("/{path:path}")
async def serve_static(path: str):
    print(f"📨 GET /{path} request received")
    if path == "health":
        return await health_check()
    return FileResponse(f'static/{path}')