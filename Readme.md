# 📚 Book Recommender System

A professional, semantic book recommender system built with LangChain, HuggingFace embeddings, Gradio, and ChromaDB. This system provides intelligent book recommendations based on natural language queries, emotional tone preferences, and category filters.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🚀 Features

- **Semantic Search**: Advanced vector search using HuggingFace embeddings
- **Emotion-based Filtering**: Filter books by emotional tone (Happy, Sad, Angry, etc.)
- **Category Classification**: Browse books by simplified categories
- **Modern UI**: Clean, responsive Gradio interface with dark theme support
- **Professional Architecture**: Well-structured, modular codebase with proper separation of concerns
- **Type Safety**: Full type hints and Pydantic models
- **Configuration Management**: YAML-based configuration with environment variable support
- **Comprehensive Testing**: Unit tests with pytest
- **Development Tools**: Pre-commit hooks, linting, formatting, and type checking

---

## 🏗️ Project Structure

```
book-recommender-system/
├── src/book_recommender/           # Main package
│   ├── core/                       # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── models.py              # Pydantic data models
│   │   └── recommender.py         # Main recommendation engine
│   ├── ui/                        # User interface
│   │   ├── __init__.py
│   │   └── gradio_app.py          # Gradio UI implementation
│   ├── utils/                     # Utilities
│   │   ├── __init__.py
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── logging.py             # Logging configuration
│   ├── __init__.py
│   └── main.py                    # Application entry point
├── config/
│   └── config.yaml                # Application configuration
├── data/                          # Data files
│   ├── books.csv                  # Raw dataset
│   ├── books_cleaned.csv          # Cleaned dataset
│   ├── books_with_emotions.csv    # Dataset with emotion scores
│   ├── books_with_categories.csv  # Dataset with categories
│   └── tagged_description.txt     # Vector search descriptions
├── notebooks/                     # Jupyter notebooks
│   ├── data-exploration.ipynb     # EDA and data cleaning
│   ├── sentiment_analysis.ipynb   # Emotion analysis
│   ├── text_classification.ipynb  # Category classification
│   └── vector_search.ipynb        # Semantic search implementation
├── tests/                         # Unit tests
│   ├── __init__.py
│   ├── test_config.py
│   └── test_models.py
├── assets/                        # Static assets
│   └── missing_cover.png          # Default book cover
├── pyproject.toml                 # Package configuration
├── requirements.txt               # Dependencies
├── setup.cfg                      # Development tools config
├── .pre-commit-config.yaml       # Pre-commit hooks
├── dev.py                         # Development helper script
├── main.py                        # Legacy entry point
└── README.md
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/book-recommender-system.git
   cd book-recommender-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/book_recommender/main.py
   ```

4. **Open your browser** and navigate to `http://localhost:7860`

### Development Installation

For development with all tools and pre-commit hooks:

```bash
# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Or use the development helper script
python dev.py install --dev
```

---

## 📖 Usage

### Basic Usage

```python
from book_recommender import BookRecommender, RecommendationRequest

# Initialize the recommender
recommender = BookRecommender()
recommender.initialize()

# Create a recommendation request
request = RecommendationRequest(
    query="A thrilling mystery with a strong female protagonist",
    category="Mystery",
    tone="Suspensful",
    top_k=10
)

# Get recommendations
response = recommender.recommend(request)

# Display results
for rec in response.recommendations:
    print(f"{rec.book.title} by {rec.book.authors}")
```

### Command Line Interface

```bash
# Basic usage
python src/book_recommender/main.py

# Enable public sharing
python src/book_recommender/main.py --share

# Enable debug mode
python src/book_recommender/main.py --debug

# Custom data directory
python src/book_recommender/main.py --data-dir /path/to/data

# Show help
python src/book_recommender/main.py --help
```

### Using the Development Helper

```bash
# Run the application
python dev.py run

# Run with public sharing
python dev.py run --share

# Run tests
python dev.py test

# Format code
python dev.py format

# Lint code
python dev.py lint

# Type check
python dev.py typecheck
```

---

## ⚙️ Configuration

The application uses a YAML configuration file (`config/config.yaml`) that can be customized:

```yaml
app:
  name: "Book Recommender System"
  host: "0.0.0.0"
  port: 7860

data:
  books_file: "data/books_with_emotions.csv"
  descriptions_file: "data/tagged_description.txt"

model:
  embedding_model: "all-MiniLM-L6-v2"

search:
  initial_top_k: 50
  final_top_k: 12
```

Environment variables can also be used:
```bash
export APP_HOST=127.0.0.1
export APP_PORT=8080
export EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src/book_recommender

# Or use the development helper
python dev.py test
```

---

## 🔧 Development

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pre-commit**: Git hooks for automated checks

### Development Workflow

1. **Make changes** to the code
2. **Run tests** to ensure functionality
3. **Format code** with Black
4. **Run linting** to check for issues
5. **Type check** with MyPy
6. **Commit changes** (pre-commit hooks will run automatically)

```bash
# Format code
python dev.py format

# Check linting
python dev.py lint

# Type check
python dev.py typecheck

# Run all checks
python dev.py format && python dev.py lint && python dev.py typecheck && python dev.py test
```

---

## 📊 Data

The system uses several data files:

- `books.csv`: Raw book dataset
- `books_cleaned.csv`: Preprocessed data
- `books_with_emotions.csv`: Books with emotion scores
- `tagged_description.txt`: Processed descriptions for vector search

### Data Pipeline

1. **Data Exploration** (`notebooks/data-exploration.ipynb`)
2. **Sentiment Analysis** (`notebooks/sentiment_analysis.ipynb`)
3. **Text Classification** (`notebooks/text_classification.ipynb`)
4. **Vector Search Setup** (`notebooks/vector_search.ipynb`)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`python dev.py install --dev`)
4. Make your changes
5. Run tests and quality checks
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines (enforced by Black)
- Add type hints to all functions
- Write tests for new functionality
- Update documentation as needed
- Ensure all pre-commit hooks pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain**: For the semantic search framework
- **HuggingFace**: For embedding models and transformers
- **Gradio**: For the intuitive UI framework
- **ChromaDB**: For vector storage and retrieval
- **Contributors**: Thanks to all contributors who have helped improve this project

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/book-recommender-system/issues) page
2. Create a new issue with detailed information
3. For urgent matters, contact [your.email@example.com](mailto:your.email@example.com)

---

## 🗺️ Roadmap

- [ ] Add more emotion categories
- [ ] Implement user rating system
- [ ] Add book similarity clustering
- [ ] Create REST API endpoints
- [ ] Add Docker containerization
- [ ] Implement caching for better performance
- [ ] Add user authentication and preferences
- [ ] Create mobile-responsive design
