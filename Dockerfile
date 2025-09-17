FROM python:3.11-slim

WORKDIR /umbrent-website
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $HTTPS_PORT

CMD ["python", "app.py"]