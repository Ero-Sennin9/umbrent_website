import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Создаем папку static если её нет
os.makedirs('static', exist_ok=True)

app = FastAPI(
    title="Umbrent Website",
    description="Статический веб-сайт",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    debug=os.getenv('FASTAPI_DEBUG', 'False').lower() == 'true'
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/assets", StaticFiles(directory="static"), name="assets")

# Создаем простую главную страницу если её нет
if not os.path.exists('static/index.html'):
    logger.info("Creating default index.html")
    with open('static/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Umbrent Website</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        .container {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 3rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { margin-bottom: 1rem; font-size: 2.5rem; }
        p { margin-bottom: 2rem; font-size: 1.2rem; }
        .status { 
            background: rgba(255,255,255,0.2); 
            padding: 0.5rem 1.5rem; 
            border-radius: 20px; 
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Umbrent Website</h1>
        <p>Сайт успешно запущен на сервере</p>
        <div class="status">Статус: <strong>Работает</strong></div>
        <div style="margin-top: 2rem; font-size: 0.9rem;">
            <p>Серверное время: <span id="time"></span></p>
        </div>
    </div>
    <script>
        document.getElementById('time').textContent = new Date().toLocaleString('ru-RU');
    </script>
</body>
</html>""")


@app.get("/")
async def serve_index():
    """Главная страница"""
    logger.info('Serving index.html')
    if not os.path.exists('static/index.html'):
        return JSONResponse(
            content={"message": "Website is running", "status": "healthy"},
            status_code=200
        )
    return FileResponse('static/index.html')


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info('Health check requested')
    return {
        "status": "healthy",
        "service": "umbrent-website",
        "version": "1.0.0"
    }


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def handle_all_paths(request: Request, path: str = ""):
    """Универсальный обработчик для всех путей"""

    # Health check имеет приоритет
    if path == "health":
        return await health_check()

    # Если путь пустой или корневой - отдаем index.html
    if path in ["", "/"]:
        return await serve_index()

    # Пытаемся найти статический файл
    file_path = f"static/{path}"

    # Если это директория - ищем index.html внутри
    if os.path.isdir(file_path):
        index_path = os.path.join(file_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            logger.warning(f"Directory index not found: {file_path}")
            raise HTTPException(status_code=404, detail="Directory index not found")

    # Если файл существует - отдаем его
    if os.path.exists(file_path) and os.path.isfile(file_path):
        logger.info(f'Serving static file: {path}')
        return FileResponse(file_path)

    # Для API методов возвращаем JSON ошибку
    if request.method != "GET":
        logger.info(f'Handling {request.method} method for path: {path}')
        return JSONResponse(
            content={"error": "Method not allowed", "path": path},
            status_code=405
        )

    # Если файл не найден - отдаем 404
    logger.warning(f"File not found: {file_path}")
    raise HTTPException(status_code=404, detail="File not found")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Кастомный обработчик 404 ошибок"""
    # Если клиент ожидает JSON - возвращаем JSON
    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=404,
            content={"error": "Not found", "path": request.url.path}
        )

    # Иначе пытаемся отдать кастомную 404 страницу
    custom_404 = "static/404.html"
    if os.path.exists(custom_404):
        return FileResponse(custom_404, status_code=404)

    # Или отдаем простую HTML страницу
    html_content = """
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>404 - Страница не найдена</h1>
            <p>Запрошенная страница не существует</p>
            <p><a href="/">Вернуться на главную</a></p>
        </body>
    </html>
    """
    return JSONResponse(content=html_content, status_code=404, media_type="text/html")


# Глобальный обработчик исключений
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений"""
    logger.error(f"Global exception handler: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )