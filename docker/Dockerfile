# Dockerfile for Intent-Based Network Generation Augmentation toolkit

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download required models
RUN python -c "import spacy; spacy.cli.download('en_core_web_md')" || echo "spaCy model download failed"
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')" || echo "NLTK data download failed"

# Copy source code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data output logs cache models

# Set environment variables
ENV PYTHONPATH=/app/src
ENV TOKENIZERS_PARALLELISM=false

# Expose port for potential web interface
EXPOSE 8000

# Default command
CMD ["python", "src/main.py", "--help"]