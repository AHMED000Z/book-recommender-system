"""Test configuration for the Book Recommender System."""

import pytest
import tempfile
from pathlib import Path

from book_recommender.core.config import Config, load_config


class TestConfig:
    """Test configuration loading and validation."""

    def test_default_config(self):
        """Test default configuration creation."""
        config = Config()

        assert config.app.name == "Book Recommender System"
        assert config.app.version == "1.0.0"
        assert config.model.embedding_model == "all-MiniLM-L6-v2"
        assert config.search.final_top_k == 12

    def test_load_config_nonexistent_file(self):
        """Test loading config from non-existent file returns defaults."""
        config = load_config("/path/that/does/not/exist.yaml")

        assert isinstance(config, Config)
        assert config.app.name == "Book Recommender System"

    def test_load_config_from_file(self):
        """Test loading config from YAML file."""
        # Create temporary config file
        config_data = """
app:
  name: "Test App"
  port: 8080
search:
  final_top_k: 20
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_data)
            temp_path = f.name

        try:
            config = load_config(temp_path)

            assert config.app.name == "Test App"
            assert config.app.port == 8080
            assert config.search.final_top_k == 20
            # Verify defaults are preserved
            assert config.model.embedding_model == "all-MiniLM-L6-v2"

        finally:
            Path(temp_path).unlink()  # Clean up
