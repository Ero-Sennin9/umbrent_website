import os
import uvicorn
from app import app

if __name__ == '__main__':
    ssl_cert = os.getenv('SSL_CERT_PATH', '/app/certs/cert.pem')
    ssl_key = os.getenv('SSL_KEY_PATH', '/app/certs/key.pem')
    port = int(os.getenv('HTTPS_PORT', '443'))

    ssl_certfile = ssl_cert if os.path.exists(ssl_cert) else None
    ssl_keyfile = ssl_key if os.path.exists(ssl_key) else None

    # Если SSL сертификатов нет, используем HTTP
    if not ssl_certfile or not ssl_keyfile:
        port = int(os.getenv('HTTP_PORT', '80'))
        print(f"SSL certificates not found. Using HTTP on port {port}")
    else:
        print(f"Using HTTPS on port {port}")

    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=port,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile,
        workers=int(os.getenv('WORKERS', '1')),
        access_log=os.getenv('ACCESS_LOG', 'False').lower() == 'true'
    )