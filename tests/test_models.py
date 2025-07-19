"""Test models for the Book Recommender System."""

import pytest
from pydantic import ValidationError

from book_recommender.core.models import (
    Book,
    RecommendationRequest,
    BookRecommendation,
    RecommendationResponse
)


class TestBook:
    """Test Book model."""

    def test_book_creation(self):
        """Test creating a valid book."""
        book = Book(
            isbn13=9780123456789,
            title="Test Book",
            authors="Test Author",
            description="A test book description",
            simplified_categories="Fiction"
        )

        assert book.isbn13 == 9780123456789
        assert book.title == "Test Book"
        assert book.authors == "Test Author"
        assert book.joy == 0.0  # Default value

    def test_book_with_emotions(self):
        """Test book with emotion scores."""
        book = Book(
            isbn13=9780123456789,
            title="Happy Book",
            authors="Joy Author",
            description="A very happy book",
            simplified_categories="Fiction",
            joy=0.9,
            sad=0.1
        )

        assert book.joy == 0.9
        assert book.sad == 0.1


class TestRecommendationRequest:
    """Test RecommendationRequest model."""

    def test_valid_request(self):
        """Test creating a valid recommendation request."""
        request = RecommendationRequest(
            query="romantic comedy book",
            category="Romance",
            tone="Happy",
            top_k=10
        )

        assert request.query == "romantic comedy book"
        assert request.category == "Romance"
        assert request.tone == "Happy"
        assert request.top_k == 10

    def test_request_with_defaults(self):
        """Test request with default values."""
        request = RecommendationRequest(query="mystery book")

        assert request.query == "mystery book"
        assert request.category == "All"
        assert request.tone == "All"
        assert request.top_k == 12

    def test_empty_query_validation(self):
        """Test that empty query is still valid (will be handled by business logic)."""
        request = RecommendationRequest(query="")
        assert request.query == ""
