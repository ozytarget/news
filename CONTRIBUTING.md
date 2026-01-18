# Contributing to Institutional News Scanner

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/news.git
   cd news
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install dev dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Make changes**
   - Edit `app.py` or create new modules
   - Test locally: `streamlit run app.py`

5. **Commit & Push**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub → Compare & Pull Request
   - Describe your changes
   - Wait for review

## Code Style

- Python 3.11+
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings for functions

## Testing

```bash
# Check syntax
python -m py_compile app.py

# Run locally
streamlit run app.py

# Docker build
docker build -t test .
```

## Issues & Discussions

- **Bug Report**: Include error message, steps to reproduce, Python version
- **Feature Request**: Explain use case and expected behavior
- **Question**: Check existing issues first

## License

By contributing, you agree your code will be licensed under MIT License.

---

Thanks for contributing! 🎉
