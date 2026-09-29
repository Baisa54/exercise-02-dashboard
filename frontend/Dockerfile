FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /install /usr/local
RUN python -c "import streamlit as st, os; p = os.path.join(os.path.dirname(st.__file__), 'static', 'index.html'); c = open(p, 'r', encoding='utf-8').read().replace('<title>Streamlit</title>', '<title>Node Registry Dashboard — Nodes</title>'); open(p, 'w', encoding='utf-8').write(c)"
RUN useradd -m appuser
USER appuser
COPY . .
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
