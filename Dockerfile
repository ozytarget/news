FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY app_http.py .

EXPOSE 8501

CMD ["python", "app_http.py"]
