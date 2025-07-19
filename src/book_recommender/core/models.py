"""Data models for the Book Recommender System."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Book(BaseModel):
    """Book data model."""
    isbn13: int
    title: str
    authors: str
    description: str
    thumbnail: Optional[str] = None
    large_thumbnail: Optional[str] = None
    simplified_categories: str
    joy: float = 0.0
    sad: float = 0.0
    angry: float = 0.0
    fear: float = 0.0
    surprise: float = 0.0
    neutral: float = 0.0

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True


class RecommendationRequest(BaseModel):
    """Request model for book recommendations."""
    query: str = Field(..., description="User's search query")
    category: str = Field(default="All", description="Book category filter")
    tone: str = Field(default="All", description="Emotional tone filter")
    top_k: int = Field(default=12, description="Number of recommendations to return")


class BookRecommendation(BaseModel):
    """Model for a single book recommendation."""
    book: Book
    similarity_score: Optional[float] = None
    thumbnail_url: str
    caption: str


class RecommendationResponse(BaseModel):
    """Response model for book recommendations."""
    recommendations: List[BookRecommendation]
    query: str
    category: str
    tone: str
    total_found: int
