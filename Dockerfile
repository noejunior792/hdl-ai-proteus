# HDL AI Proteus API Dockerfile
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ghdl \
    iverilog \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 hdluser && \
    chown -R hdluser:hdluser /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY docs/ ./docs/
COPY LICENSE ./
COPY README.md ./

# Create necessary directories
RUN mkdir -p build export temp logs && \
    chown -R hdluser:hdluser /app

# Switch to non-root user
USER hdluser

# Set default environment variables
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=5000
ENV SERVER_DEBUG=false
ENV DEFAULT_PROVIDER=azure_openai
ENV LOG_LEVEL=INFO
ENV TEMP_DIRECTORY=/app/temp
ENV EXPORT_DIRECTORY=/app/export
ENV GHDL_PATH=ghdl
ENV IVERILOG_PATH=iverilog

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python3", "src/app.py"]