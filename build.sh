#!/bin/bash

# Book Recommender System Build Script
# This script helps build and run the application

set -e

echo "🚀 Book Recommender System Build Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python version: $python_version"
}

# Create virtual environment
create_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    else
        print_status "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
}

# Install dependencies
install_deps() {
    print_status "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Run tests
run_tests() {
    print_status "Running tests..."
    python -m pytest tests/ -v || print_warning "Some tests failed"
}

# Build documentation
build_docs() {
    print_status "Building documentation..."
    # Add documentation build commands here if needed
}

# Main function
main() {
    case "$1" in
        "setup")
            check_python
            create_venv
            activate_venv
            install_deps
            print_status "Setup complete! Run './build.sh run' to start the application."
            ;;
        "run")
            activate_venv
            python src/book_recommender/main.py
            ;;
        "test")
            activate_venv
            run_tests
            ;;
        "clean")
            print_status "Cleaning up..."
            rm -rf venv __pycache__ .pytest_cache .mypy_cache
            find . -name "*.pyc" -delete
            print_status "Cleanup complete"
            ;;
        "docker")
            print_status "Building Docker image..."
            docker build -t book-recommender .
            print_status "Docker image built. Run 'docker run -p 7860:7860 book-recommender' to start."
            ;;
        *)
            echo "Usage: $0 {setup|run|test|clean|docker}"
            echo ""
            echo "Commands:"
            echo "  setup  - Set up virtual environment and install dependencies"
            echo "  run    - Run the application"
            echo "  test   - Run tests"
            echo "  clean  - Clean up generated files"
            echo "  docker - Build Docker image"
            exit 1
            ;;
    esac
}

main "$@"
