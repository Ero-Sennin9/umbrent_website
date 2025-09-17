import os
import sys
import logging
from flask import Flask, send_from_directory
from dotenv import load_dotenv

load_dotenv()

# Configure logging to stderr with immediate flushing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)  # Log to stderr
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')


# Custom filter to flush after each log
class FlushingHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


# Replace default handler with flushing handler
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

flushing_handler = FlushingHandler(sys.stderr)
flushing_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logging.root.addHandler(flushing_handler)
logging.root.setLevel(logging.INFO)


@app.route('/')
def serve_index():
    logger.info('Serving index.html')
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    logger.info(f'Serving static file: {path}')
    return send_from_directory('static', path)


@app.route('/health')
def health_check():
    logger.info('Health check requested')
    try:
        with open('static/index.html', 'r'):
            pass
        logger.info('Health check passed')
        return {"status": "healthy", "message": "OK"}, 200
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        return {"status": "unhealthy", "error": str(e)}, 500


if __name__ == '__main__':
    ssl_cert = os.getenv('SSL_CERT_PATH', '/app/certs/cert.pem')
    ssl_key = os.getenv('SSL_KEY_PATH', '/app/certs/key.pem')

    logger.info(f'Starting Flask server on port {os.getenv("PORT", 443)}')

    # Configure Flask built-in logger to use stderr
    import flask.cli

    flask.cli.show_server_banner = lambda *args: None

    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 443)),
        ssl_context=(ssl_cert, ssl_key),
        # Force immediate flushing
        debug=False  # debug=False for production
    )