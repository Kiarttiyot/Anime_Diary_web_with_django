# Simple dev Dockerfile for Django
FROM python:3.13-slim

# System deps (build tools for common Python wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Workdir
WORKDIR /app

# Install deps first for better caching
COPY requirements.txt /tmp/requirements.txt
RUN if [ -f /tmp/requirements.txt ]; then pip install -r /tmp/requirements.txt; fi

# Copy project
COPY . /app

# Create non-root user (still root at this point)
RUN useradd -m appuser && chown -R appuser:appuser /app

# Entrypoint (ยังเป็น root → แก้ CRLF/BOM + chmod ได้)
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh \
 && sed -i '1s/^\xEF\xBB\xBF//' /entrypoint.sh \
 && chmod +x /entrypoint.sh

EXPOSE 8000

# สลับเป็น user ปกติ หลังจากจัดการ permission แล้ว
USER appuser

ENTRYPOINT ["/entrypoint.sh"]
