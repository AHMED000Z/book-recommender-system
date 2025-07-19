"""Configuration management for the Book Recommender System."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration."""
    name: str = "Book Recommender System"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 7860


class DataConfig(BaseModel):
    """Data configuration."""
    books_file: str = "data/books_with_emotions.csv"
    descriptions_file: str = "data/tagged_description.txt"
    missing_cover_image: str = "assets/missing_cover.png"


class ModelConfig(BaseModel):
    """Model configuration."""
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 0
    chunk_overlap: int = 0
    separator: str = "\n"


class SearchConfig(BaseModel):
    """Search configuration."""
    initial_top_k: int = 50
    final_top_k: int = 12


class UIConfig(BaseModel):
    """UI configuration."""
    theme: str = "glass"
    gallery_columns: int = 2
    gallery_rows: int = 5
    description_truncate_length: int = 50


class EmotionConfig(BaseModel):
    """Emotion configuration."""
    tones: list[str] = Field(default_factory=lambda: [
        "All", "Happy", "Sad", "Angry", "Suspensful", "Surprising", "Neutral"
    ])
    emotion_mapping: Dict[str, str] = Field(default_factory=lambda: {
        "Happy": "joy",
        "Sad": "sad",
        "Angry": "angry",
        "Suspensful": "fear",
        "Surprising": "surprise",
        "Neutral": "neutral"
    })


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    format: str = "{time} | {level} | {name} | {message}"
    file: str = "logs/app.log"


class Config(BaseModel):
    """Main configuration class."""
    app: AppConfig = Field(default_factory=AppConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    emotions: EmotionConfig = Field(default_factory=EmotionConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to configuration file. If None, uses default.

    Returns:
        Config object with loaded configuration.
    """
    if config_path is None:
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "config.yaml"

    config_path = Path(config_path)

    if not config_path.exists():
        # Return default configuration if file doesn't exist
        return Config()

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)

        return Config(**config_data)
    except Exception as e:
        # Fall back to default configuration if loading fails
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return Config()


# Global configuration instance
config = load_config()
