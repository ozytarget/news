FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir streamlit feedparser requests pandas numpy python-dateutil plotly

COPY app_simple.py .

EXPOSE 8501

CMD ["streamlit", "run", "app_simple.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--client.showErrorDetails=true", "--logger.level=info"]
