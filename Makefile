# Makefile for Intent-Based Network Generation Augmentation toolkit

.PHONY: help install install-dev test lint format clean build upload docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package and dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build the package"
	@echo "  upload       - Upload to PyPI"
	@echo "  docs         - Generate documentation"
	@echo "  setup-models - Download required models"
	@echo "  generate     - Generate sample dataset"

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

# Setup models
setup-models:
	python -c "import spacy; spacy.cli.download('en_core_web_md')"
	python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

# Testing
test:
	pytest tests/ -v

# Code quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Build and distribution
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "Documentation available in docs/ directory"

# Generate sample dataset
generate:
	python src/main.py --num_records 100 --use_paraphrasing --paraphrase_ratio 0.2

# Development workflow
dev-setup: install-dev setup-models
	@echo "Development environment ready!"

# Quick test run
quick-test:
	python src/main.py --num_records 10 --output_file test_output.csv

# Full pipeline test
full-test:
	python src/main.py --num_records 50 --use_paraphrasing --paraphrase_ratio 0.3 --use_backtranslation --backtranslate_ratio 0.2