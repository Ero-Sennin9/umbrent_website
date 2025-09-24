import os
import uvicorn
from app import app

if __name__ == '__main__':
    ssl_cert = os.getenv('SSL_CERT_PATH', '/app/certs/cert.pem')
    ssl_key = os.getenv('SSL_KEY_PATH', '/app/certs/key.pem')
    port = int(os.getenv('HTTPS_PORT', 443))

    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=port,
        ssl_certfile=ssl_cert if os.path.exists(ssl_cert) else None,
        ssl_keyfile=ssl_key if os.path.exists(ssl_key) else None,
        reload=os.getenv('FASTAPI_DEBUG', 'False').lower() == 'true'
    )