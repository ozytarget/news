FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Create .streamlit config directory
RUN mkdir -p .streamlit

# Create streamlit config
RUN echo "[server]\nheadless = true\nport = 8501\nenableXsrfProtection = false\n[client]\ntoolbarMode = \"minimal\"" > .streamlit/config.toml

# Expose port
EXPOSE 8501

# Run streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
