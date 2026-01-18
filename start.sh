#!/bin/bash
echo "=== RAILWAY DIAGNOSTICS ==="
echo "Python version:"
python --version

echo ""
echo "Installed packages:"
pip list

echo ""
echo "Testing imports:"
python -c "import streamlit; print('✓ Streamlit OK')"
python -c "import feedparser; print('✓ Feedparser OK')"
python -c "import requests; print('✓ Requests OK')"

echo ""
echo "Streamlit version:"
streamlit --version

echo ""
echo "Starting Streamlit..."
streamlit run app_simple.py --server.port 8501 --server.address 0.0.0.0
