import app.py

if __name__ == '__main__':
    ssl_cert = os.getenv('SSL_CERT_PATH', '/app/certs/cert.pem')
    ssl_key = os.getenv('SSL_KEY_PATH', '/app/certs/key.pem')

    port = int(os.getenv('HTTPS_PORT', 443))

    app.run(
        host='0.0.0.0',
        port=port,
        ssl_context=(ssl_cert, ssl_key),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )