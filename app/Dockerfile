# FROM python:3.10-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["python", "main.py"]

############################
# Stage 1: Builder
############################
FROM python:3.10-slim AS builder

# Prevent Python cache files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Install only build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list only (cache-friendly)
COPY requirements.txt .

# Install dependencies into a temporary directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


############################
# Stage 2: Runtime (SECURE)
############################
FROM python:3.10-slim

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user (SECURITY)
RUN useradd -m -u 10001 appuser

WORKDIR /app

# Copy only runtime dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Fix ownership (important for Kubernetes)
RUN chown -R appuser:appuser /app

# Drop root privileges
USER appuser

# Expose app port (documentation)
EXPOSE 5000

# Run application
CMD ["python", "main.py"]
