"""Core recommendation engine for the Book Recommender System."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple
from loguru import logger

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from .config import config
from .models import Book, RecommendationRequest, BookRecommendation, RecommendationResponse
from ..utils.exceptions import DataLoadError, ModelInitError, RecommendationError


class BookRecommender:
    """Main recommendation engine for books."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the book recommender.

        Args:
            data_dir: Directory containing data files. If None, uses config default.
        """
        self.data_dir = data_dir or Path(".")
        self.books_df: Optional[pd.DataFrame] = None
        self.vector_store: Optional[Chroma] = None
        self.embedding_model: Optional[HuggingFaceEmbeddings] = None
        self._is_initialized = False

    def initialize(self) -> None:
        """Initialize the recommender with data and models."""
        try:
            logger.info("Initializing Book Recommender...")
            self._load_data()
            self._setup_embeddings()
            self._setup_vector_store()
            self._is_initialized = True
            logger.info("Book Recommender initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Book Recommender: {e}")
            raise ModelInitError(f"Initialization failed: {e}")

    def _load_data(self) -> None:
        """Load books data from CSV file."""
        books_file = self.data_dir / config.data.books_file

        if not books_file.exists():
            raise DataLoadError(f"Books file not found: {books_file}")

        try:
            self.books_df = pd.read_csv(books_file)

            # Process thumbnail URLs
            self.books_df['large_thumbnail'] = self.books_df['thumbnail'] + "&fife=w800"
            self.books_df['large_thumbnail'] = np.where(
                self.books_df['large_thumbnail'].isna(),
                str(self.data_dir / config.data.missing_cover_image),
                self.books_df['large_thumbnail']
            )

            logger.info(f"Loaded {len(self.books_df)} books from {books_file}")

        except Exception as e:
            raise DataLoadError(f"Failed to load books data: {e}")

    def _setup_embeddings(self) -> None:
        """Setup embedding model."""
        try:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=config.model.embedding_model
            )
            logger.info(f"Loaded embedding model: {config.model.embedding_model}")
        except Exception as e:
            raise ModelInitError(f"Failed to load embedding model: {e}")

    def _setup_vector_store(self) -> None:
        """Setup vector store from descriptions."""
        descriptions_file = self.data_dir / config.data.descriptions_file

        if not descriptions_file.exists():
            raise DataLoadError(f"Descriptions file not found: {descriptions_file}")

        try:
            # Load and split documents
            raw_document = TextLoader(str(descriptions_file), encoding='utf-8').load()
            text_splitter = CharacterTextSplitter(
                chunk_size=config.model.chunk_size,
                chunk_overlap=config.model.chunk_overlap,
                separator=config.model.separator
            )
            documents = text_splitter.split_documents(raw_document)

            # Create vector store
            self.vector_store = Chroma.from_documents(documents, self.embedding_model)
            logger.info(f"Created vector store with {len(documents)} documents")

        except Exception as e:
            raise ModelInitError(f"Failed to setup vector store: {e}")

    def get_categories(self) -> List[str]:
        """Get available book categories."""
        if not self._is_initialized or self.books_df is None:
            raise RecommendationError("Recommender not initialized")

        categories = ["All"] + sorted(self.books_df['simplified_categories'].unique())
        return categories

    def get_tones(self) -> List[str]:
        """Get available emotional tones."""
        return config.emotions.tones

    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        """
        Get book recommendations based on the request.

        Args:
            request: Recommendation request with query, filters, etc.

        Returns:
            RecommendationResponse with recommended books.
        """
        if not self._is_initialized:
            raise RecommendationError("Recommender not initialized")

        try:
            # Get semantic recommendations
            recommendations = self._get_semantic_recommendations(
                query=request.query,
                category=request.category,
                tone=request.tone,
                initial_top_k=config.search.initial_top_k,
                final_top_k=request.top_k
            )

            # Convert to response format
            book_recommendations = []
            for _, row in recommendations.iterrows():
                book = Book(**row.to_dict())

                # Create caption
                caption = self._create_book_caption(book)

                book_rec = BookRecommendation(
                    book=book,
                    thumbnail_url=row['large_thumbnail'],
                    caption=caption
                )
                book_recommendations.append(book_rec)

            return RecommendationResponse(
                recommendations=book_recommendations,
                query=request.query,
                category=request.category,
                tone=request.tone,
                total_found=len(book_recommendations)
            )

        except Exception as e:
            logger.error(f"Recommendation failed: {e}")
            raise RecommendationError(f"Failed to get recommendations: {e}")

    def _get_semantic_recommendations(
        self,
        query: str,
        category: str = "All",
        tone: str = "All",
        initial_top_k: int = 50,
        final_top_k: int = 12
    ) -> pd.DataFrame:
        """
        Get semantic recommendations based on query and filters.

        Args:
            query: User's search query
            category: Category filter
            tone: Emotional tone filter
            initial_top_k: Initial number of results to retrieve
            final_top_k: Final number of results to return

        Returns:
            DataFrame with recommended books.
        """
        if self.vector_store is None or self.books_df is None:
            raise RecommendationError("Vector store or books data not available")

        # Get semantic matches
        search_results = self.vector_store.similarity_search(query, k=initial_top_k)

        # Extract book IDs from search results
        book_ids = []
        for result in search_results:
            try:
                book_id = int(result.page_content.strip('"').split()[0])
                book_ids.append(book_id)
            except (ValueError, IndexError):
                continue

        # Filter books by IDs
        filtered_books = self.books_df[
            self.books_df["isbn13"].isin(book_ids)
        ].head(initial_top_k).copy()

        # Apply category filter
        if category != "All":
            filtered_books = filtered_books[
                filtered_books['simplified_categories'] == category
            ]

        # Apply tone filter (sort by emotion)
        if tone != "All" and tone in config.emotions.emotion_mapping:
            emotion_column = config.emotions.emotion_mapping[tone]
            if emotion_column in filtered_books.columns:
                filtered_books = filtered_books.sort_values(
                    by=emotion_column, ascending=False
                )

        return filtered_books.head(final_top_k)

    def _create_book_caption(self, book: Book) -> str:
        """
        Create a caption for a book recommendation.

        Args:
            book: Book object

        Returns:
            Formatted caption string.
        """
        # Truncate description
        description = book.description or ""
        max_length = config.ui.description_truncate_length
        truncated_description = (
            description[:max_length] + '...'
            if len(description) > max_length
            else description
        )

        # Format authors
        authors_list = book.authors.split(";")
        if len(authors_list) == 2:
            authors_str = f"{authors_list[0]} and {authors_list[1]}"
        elif len(authors_list) > 2:
            authors_str = f"{', '.join(authors_list[:-1])} and {authors_list[-1]}"
        else:
            authors_str = book.authors

        return f"{book.title} by {authors_str}\n\n{truncated_description}"
