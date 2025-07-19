"""Gradio UI for the Book Recommender System."""

from typing import List, Tuple, Any
import gradio as gr
from loguru import logger

from ..core import config, BookRecommender, RecommendationRequest
from ..utils.exceptions import RecommendationError


class BookRecommenderUI:
    """Gradio UI for the Book Recommender System."""

    def __init__(self, recommender: BookRecommender):
        """
        Initialize the UI.

        Args:
            recommender: Initialized BookRecommender instance.
        """
        self.recommender = recommender
        self.interface = None

    def create_interface(self) -> gr.Blocks:
        """Create and return the Gradio interface."""
        # Get available options
        categories = self.recommender.get_categories()
        tones = self.recommender.get_tones()

        with gr.Blocks(
            theme=gr.themes.Glass(),
            title=config.app.name,
            css=self._get_custom_css()
        ) as interface:

            # Header
            gr.Markdown(
                f"""
                <h1 style="text-align: center;">📚 {config.app.name}</h1>
                <p style="text-align: center;">Find your next read based on your mood and preferences!</p>
                """,
                elem_classes="header"
            )

            # Input components
            with gr.Row():
                with gr.Column(scale=2):
                    query = gr.Textbox(
                        label="Describe the book you're looking for",
                        placeholder="E.g., 'A heartwarming romantic story with a twist'",
                        lines=3,
                        info="Be as descriptive as possible for better recommendations",
                        elem_classes="input-textbox"
                    )

                with gr.Column(scale=1):
                    category = gr.Dropdown(
                        label="Category",
                        choices=categories,
                        value="All",
                        elem_classes="dropdown"
                    )
                    tone = gr.Dropdown(
                        label="Emotional Tone",
                        choices=tones,
                        value="All",
                        elem_classes="dropdown"
                    )

            # Submit button
            submit_button = gr.Button(
                "🔍 Get Recommendations",
                variant="primary",
                size="lg",
                elem_classes="submit-button"
            )

            # Loading indicator
            loading_msg = gr.Text(
                value="",
                visible=False,
                elem_classes="loading-text"
            )

            # Output gallery
            output = gr.Gallery(
                label="Recommended Books",
                columns=config.ui.gallery_columns,
                rows=config.ui.gallery_rows,
                show_label=False,
                elem_id="recommendations-gallery",
                elem_classes="gallery"
            )

            # Footer
            gr.Markdown(
                """
                <p style="text-align: center; margin-top: 20px; color: #666;">
                Powered by LangChain, HuggingFace, and ChromaDB
                </p>
                """,
                elem_classes="footer"
            )

            # Event handlers
            submit_button.click(
                fn=self._show_loading,
                inputs=[],
                outputs=[loading_msg]
            ).then(
                fn=self._get_recommendations,
                inputs=[query, category, tone],
                outputs=[output]
            ).then(
                fn=self._hide_loading,
                inputs=[],
                outputs=[loading_msg]
            )

        self.interface = interface
        return interface

    def _get_recommendations(
        self,
        query: str,
        category: str,
        tone: str
    ) -> List[Tuple[str, str]]:
        """
        Get book recommendations and format for Gradio gallery.

        Args:
            query: User's search query
            category: Selected category
            tone: Selected tone

        Returns:
            List of (image_url, caption) tuples for Gradio gallery.
        """
        try:
            if not query.strip():
                return []

            # Create recommendation request
            request = RecommendationRequest(
                query=query,
                category=category,
                tone=tone,
                top_k=config.search.final_top_k
            )

            # Get recommendations
            response = self.recommender.recommend(request)

            # Format for Gradio gallery
            results = []
            for rec in response.recommendations:
                results.append((rec.thumbnail_url, rec.caption))

            logger.info(
                f"Generated {len(results)} recommendations for query: '{query}'")
            return results

        except RecommendationError as e:
            logger.error(f"Recommendation error: {e}")
            gr.Warning(f"Recommendation failed: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            gr.Warning("An unexpected error occurred. Please try again.")
            return []

    def _show_loading(self) -> gr.update:
        """Show loading message."""
        return gr.update(value="⏳ Loading recommendations...", visible=True)

    def _hide_loading(self) -> gr.update:
        """Hide loading message."""
        return gr.update(value="", visible=False)

    def _get_custom_css(self) -> str:
        """Get custom CSS for the interface."""
        return """
        .header {
            margin-bottom: 2rem;
        }
        
        .input-textbox {
            border-radius: 8px;
        }
        
        .dropdown {
            border-radius: 8px;
        }
        
        .submit-button {
            margin: 1rem 0;
            border-radius: 8px;
            font-weight: bold;
        }
        
        .loading-text {
            text-align: center;
            color: #007bff;
            font-weight: bold;
        }
        
        .gallery {
            margin-top: 1rem;
            border-radius: 8px;
        }
        
        .footer {
            margin-top: 2rem;
            font-size: 0.9em;
        }
        
        #recommendations-gallery .thumbnail {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        """

    def launch(
        self,
        share: bool = False,
        server_name: str = None,
        server_port: int = None,
        **kwargs
    ) -> None:
        """
        Launch the Gradio interface.

        Args:
            share: Whether to create a public link
            server_name: Server host
            server_port: Server port
            **kwargs: Additional Gradio launch arguments
        """
        if self.interface is None:
            self.create_interface()

        server_name = server_name or config.app.host
        server_port = server_port or config.app.port

        logger.info(f"Launching {config.app.name} on {server_name}:{server_port}")

        self.interface.launch(
            share=share,
            server_name=server_name,
            server_port=server_port,
            **kwargs
        )
