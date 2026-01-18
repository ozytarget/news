FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true

RUN pip install --upgrade pip --quiet

RUN pip install streamlit feedparser requests pandas numpy python-dateutil plotly --quiet

COPY app_simple.py .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8501

ENTRYPOINT ["bash", "-c"]
CMD ["exec streamlit run app_simple.py --server.port=8501 --server.address=0.0.0.0 --logger.level=info --client.showErrorDetails=true"]
