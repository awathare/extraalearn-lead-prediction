# Lightweight Python image for the Flask API
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Hugging Face Spaces expects the web service on port 7860
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "app:app"]
