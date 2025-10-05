# HDL AI Proteus - Makefile
# Provides convenient commands for development, testing, and deployment

.PHONY: help install install-dev install-system run run-dev run-prod test lint format clean docker docker-build docker-run docker-stop logs check-deps setup-env docs

# Default target
help:
	@echo "HDL AI Proteus - Available Commands"
	@echo "=================================="
	@echo ""
	@echo "Development:"
	@echo "  install        Install Python dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  install-system Install system dependencies (Ubuntu/Debian)"
	@echo "  setup-env      Setup development environment"
	@echo "  run            Run the API server"
	@echo "  run-dev        Run in development mode"
	@echo "  run-prod       Run in production mode with Gunicorn"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  test           Run tests (when available)"
	@echo "  lint           Run code linting"
	@echo "  format         Format code with black"
	@echo "  check-deps     Check for missing dependencies"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"
	@echo "  docker-stop    Stop Docker container"
	@echo "  docker-logs    View Docker logs"
	@echo ""
	@echo "Utilities:"
	@echo "  clean          Clean temporary files and cache"
	@echo "  logs           View application logs"
	@echo "  docs           Generate/update documentation"
	@echo ""

# Installation targets
install:
	@echo "Installing Python dependencies..."
	pip3 install -r requirements.txt

install-dev:
	@echo "Installing development dependencies..."
	pip3 install -r requirements.txt
	pip3 install black flake8 mypy pytest pytest-cov

install-system:
	@echo "Installing system dependencies (Ubuntu/Debian)..."
	sudo apt update
	sudo apt install -y python3 python3-pip python3-venv ghdl iverilog curl

setup-env:
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env.template .env; \
		echo "Please edit .env file with your configuration"; \
	fi
	@mkdir -p build export temp logs
	@echo "Environment setup complete!"

# Running targets
run:
	@echo "Starting HDL AI Proteus API..."
	python3 run.py

run-dev:
	@echo "Starting in development mode..."
	export SERVER_DEBUG=true && export LOG_LEVEL=DEBUG && python3 run.py

run-prod:
	@echo "Starting in production mode with Gunicorn..."
	@which gunicorn > /dev/null || (echo "Gunicorn not installed. Run: pip install gunicorn" && exit 1)
	cd src && gunicorn -c ../gunicorn.conf.py app:app

# Testing and quality targets
test:
	@echo "Running tests..."
	@if [ -d tests ]; then \
		python3 -m pytest tests/ -v; \
	else \
		echo "No tests directory found. Create tests/ directory and add test files."; \
	fi

lint:
	@echo "Running code linting..."
	@which flake8 > /dev/null || (echo "flake8 not installed. Run: make install-dev" && exit 1)
	flake8 src/ --max-line-length=100 --ignore=E203,W503

format:
	@echo "Formatting code with black..."
	@which black > /dev/null || (echo "black not installed. Run: make install-dev" && exit 1)
	black src/ --line-length=100

check-deps:
	@echo "Checking dependencies..."
	@echo "Python dependencies:"
	@python3 -c "import flask, requests; print('✓ Python dependencies OK')" || echo "✗ Missing Python dependencies"
	@echo "System dependencies:"
	@which ghdl > /dev/null && echo "✓ GHDL available" || echo "✗ GHDL not found"
	@which iverilog > /dev/null && echo "✓ Icarus Verilog available" || echo "✗ Icarus Verilog not found"
	@which curl > /dev/null && echo "✓ curl available" || echo "✗ curl not found"

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t hdl-ai-proteus:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -d \
		--name hdl-ai-proteus-api \
		-p 5000:5000 \
		-v $(PWD)/logs:/app/logs \
		-v $(PWD)/export:/app/export \
		hdl-ai-proteus:latest

docker-stop:
	@echo "Stopping Docker container..."
	docker stop hdl-ai-proteus-api || true
	docker rm hdl-ai-proteus-api || true

docker-logs:
	@echo "Viewing Docker logs..."
	docker logs -f hdl-ai-proteus-api

docker-compose-up:
	@echo "Starting with Docker Compose..."
	docker-compose up -d

docker-compose-down:
	@echo "Stopping Docker Compose..."
	docker-compose down

# Utility targets
clean:
	@echo "Cleaning temporary files and cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	rm -rf .mypy_cache 2>/dev/null || true
	rm -rf build/* 2>/dev/null || true
	rm -rf temp/* 2>/dev/null || true
	@echo "Cleanup complete!"

logs:
	@echo "Viewing application logs..."
	@if [ -f logs/hdl_proteus.log ]; then \
		tail -f logs/hdl_proteus.log; \
	else \
		echo "No log file found. Start the application to generate logs."; \
	fi

docs:
	@echo "Documentation locations:"
	@echo "  Main docs: docs/DOCS.md"
	@echo "  API context: docs/api_context.json"
	@echo "  README: README.md"

# Health check
health:
	@echo "Checking API health..."
	@curl -s http://localhost:5000/health | python3 -m json.tool || echo "API not responding"

# Development workflow
dev-setup: install-system setup-env install install-dev
	@echo "Development environment setup complete!"
	@echo "Next steps:"
	@echo "  1. Edit .env file with your configuration"
	@echo "  2. Run 'make run-dev' to start the server"

# Production setup
prod-setup: install setup-env
	@echo "Production environment setup complete!"
	@echo "Configure your environment variables and run 'make run-prod'"

# Quick start for new developers
quick-start:
	@echo "HDL AI Proteus - Quick Start"
	@echo "==========================="
	@echo ""
	@echo "1. Setting up environment..."
	@make setup-env
	@echo ""
	@echo "2. Installing dependencies..."
	@make install
	@echo ""
	@echo "3. Checking dependencies..."
	@make check-deps
	@echo ""
	@echo "✓ Setup complete! Run 'make run' to start the server"

# Version info
version:
	@echo "HDL AI Proteus v1.0.0"
	@python3 --version
	@docker --version 2>/dev/null || echo "Docker not installed"