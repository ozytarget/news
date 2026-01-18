#!/bin/bash
set -e

echo "Starting Institutional News Scanner..."
echo "Python version:"
python --version

echo "Checking Streamlit installation..."
python -m streamlit version

echo "Listing installed packages:"
pip list | grep -i streamlit

echo "Running Streamlit app..."
exec python -m streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --logger.level=debug
