"""Custom exceptions for the Book Recommender System."""


class BookRecommenderError(Exception):
    """Base exception for Book Recommender System."""
    pass


class DataLoadError(BookRecommenderError):
    """Raised when data loading fails."""
    pass


class ModelInitError(BookRecommenderError):
    """Raised when model initialization fails."""
    pass


class RecommendationError(BookRecommenderError):
    """Raised when recommendation generation fails."""
    pass


class ConfigurationError(BookRecommenderError):
    """Raised when configuration is invalid."""
    pass
