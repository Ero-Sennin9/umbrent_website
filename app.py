import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="WebDAV Server", docs_url=None, redoc_url=None)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_index():
    """Главная страница - отдаем index.html"""
    logger.info('Serving index.html')
    return FileResponse('static/index.html')


@app.api_route("/{path:path}", methods=["GET", "PROPFIND", "PROPPATCH", "MKCOL", "LOCK", "UNLOCK"])
async def serve_static_or_handle_webdav(path: str):
    """Обработка статических файлов и WebDAV методов"""
    if path == "health":
        # Перенаправляем health check на специальный endpoint
        return await health_check()

    if path.startswith("static/"):
        path = path[7:]

    file_path = f"static/{path}" if path else "static/index.html"

    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")

    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, "index.html")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Directory index not found")

    if request.method != "GET":
        logger.info(f'Handling WebDAV method: {request.method} for path: {path}')
        return JSONResponse(content={"message": "WebDAV method handled"}, status_code=200)

    logger.info(f'Serving static file: {path}')
    return FileResponse(file_path)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info('Health check requested')
    try:
        if os.path.exists('static/index.html'):
            return {"status": "healthy", "message": "OK"}
        else:
            logger.error('Health check failed: static/index.html not found')
            raise HTTPException(status_code=500, detail="Static files not available")
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


# OPTIONS методы обрабатываются автоматически через CORS middleware

if __name__ == "__main__":
    ssl_cert = os.getenv('SSL_CERT_PATH', '/app/certs/cert.pem')
    ssl_key = os.getenv('SSL_KEY_PATH', '/app/certs/key.pem')
    port = int(os.getenv("PORT", 443))

    logger.info(f'Starting FastAPI server on port {port}')

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        ssl_certfile=ssl_cert if os.path.exists(ssl_cert) else None,
        ssl_keyfile=ssl_key if os.path.exists(ssl_key) else None,
        reload=os.getenv('FASTAPI_DEBUG', 'False').lower() == 'true'
    )