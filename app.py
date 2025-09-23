import os
import sys
import logging
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET', 'PROPFIND', 'PROPPATCH', 'MKCOL', 'LOCK', 'UNLOCK'])
def serve_index():
    if request.method == 'GET':
        logger.info('Serving index.html')
        return send_from_directory('static', 'index.html')
    else:
        logger.info(f'Handling WebDAV method: {request.method}')
        return '', 200


@app.route('/<path:path>', methods=['GET', 'PROPFIND', 'PROPPATCH', 'MKCOL', 'LOCK', 'UNLOCK'])
def serve_static(path):
    if request.method == 'GET':
        logger.info(f'Serving static file: {path}')
        return send_from_directory('static', path)
    else:
        logger.info(f'Handling WebDAV method: {request.method} for path: {path}')
        return '', 200


@app.route('/health')
def health_check():
    logger.info('Health check requested')
    try:
        with open('static/index.html', 'r'):
            pass
        return {"status": "healthy", "message": "OK"}, 200
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        return {"status": "unhealthy", "error": str(e)}, 500


# Явно обрабатываем OPTIONS для CORS
@app.route('/', methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path=None):
    response = jsonify({"message": "OK"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response, 200


if __name__ == '__main__':
    ssl_cert = os.getenv('SSL_CERT_PATH', '/app/certs/cert.pem')
    ssl_key = os.getenv('SSL_KEY_PATH', '/app/certs/key.pem')

    logger.info(f'Starting Flask server on port {os.getenv("PORT", 443)}')

    # Используем production WSGI server вместо development server
    from werkzeug.serving import run_simple
    from werkzeug.middleware.dispatcher import DispatcherMiddleware

    application = DispatcherMiddleware(app)

    run_simple(
        hostname='0.0.0.0',
        port=int(os.getenv("PORT", 443)),
        application=application,
        ssl_context=(ssl_cert, ssl_key),
        threaded=True,
    )