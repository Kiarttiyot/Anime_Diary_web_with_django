# Simple, working dev Dockerfile for Django + ERD
FROM python:3.13-slim

# ---- System deps: build tools, MySQL client headers, Graphviz (for ERD), tzdata ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev libmariadb-dev-compat \
    libpq-dev \
    graphviz \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# ---- Environment ----
ENV TZ=Asia/Bangkok \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DJANGO_DEBUG=1

WORKDIR /app

# ---- Install Python deps (cache-friendly) ----
# ✅ ให้แน่ใจว่าใน requirements.txt มี:
#    django-extensions
#    pydot
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ---- Copy project ----
COPY . /app

# ---- Non-root user ----
RUN useradd -m appuser && chown -R appuser:appuser /app

# ---- Entrypoint (optional but recommended) ----
# ถ้ามีไฟล์ entrypoint.sh ในโปรเจกต์อยู่แล้ว จะถูกคัดลอกและเคลียร์ CRLF/BOM ให้
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh \
 && sed -i '1s/^\xEF\xBB\xBF//' /entrypoint.sh \
 && chmod +x /entrypoint.sh

EXPOSE 8000
USER appuser

# ถ้าใช้ entrypoint.sh ให้คงบรรทัดนี้ไว้
ENTRYPOINT ["/entrypoint.sh"]

# ถ้า **ไม่มี** entrypoint.sh ให้คอมเมนต์ ENTRYPOINT ด้านบน แล้วใช้บรรทัดนี้แทน:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
