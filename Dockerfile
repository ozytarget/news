FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install streamlit feedparser requests pandas numpy python-dateutil plotly

COPY app_simple.py .

EXPOSE 8501

CMD ["streamlit", "run", "app_simple.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
