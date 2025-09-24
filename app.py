from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Создаем папку static если её нет
os.makedirs('static', exist_ok=True)

# Монтируем статические файлы
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

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/{path:path}")
async def serve_static(path: str):
    if path == "health":
        return await health_check()
    return FileResponse(f'static/{path}')