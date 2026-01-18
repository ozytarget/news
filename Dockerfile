FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install streamlit feedparser requests pandas numpy python-dateutil plotly

COPY app_simple.py .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8501

CMD ["bash", "start.sh"]
