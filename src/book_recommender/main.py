"""Main application entry point for the Book Recommender System."""

from loguru import logger
from book_recommender.utils.exceptions import BookRecommenderError
from book_recommender.utils.logging import setup_logging
from book_recommender.ui import BookRecommenderUI
from book_recommender.core import config, BookRecommender
import sys
from pathlib import Path
from typing import Optional
import argparse

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))


def main(
    data_dir: Optional[str] = None,
    config_path: Optional[str] = None,
    share: bool = False,
    debug: bool = False
) -> None:
    """
    Main application entry point.

    Args:
        data_dir: Directory containing data files
        config_path: Path to configuration file
        share: Whether to create a public Gradio link
        debug: Enable debug mode
    """
    try:
        # Setup logging
        if debug:
            config.app.debug = True
            config.logging.level = "DEBUG"

        setup_logging()
        logger.info(f"Starting {config.app.name} v{config.app.version}")

        # Initialize recommender
        data_path = Path(data_dir) if data_dir else Path(".")
        recommender = BookRecommender(data_dir=data_path)
        recommender.initialize()

        # Create and launch UI
        ui = BookRecommenderUI(recommender)
        ui.create_interface()
        ui.launch(share=share)

    except BookRecommenderError as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


def cli() -> None:
    """Command line interface."""
    parser = argparse.ArgumentParser(
        description="Book Recommender System",
        prog="book-recommender"
    )

    parser.add_argument(
        "--data-dir",
        type=str,
        help="Directory containing data files"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public Gradio link"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {config.app.version}"
    )

    args = parser.parse_args()

    main(
        data_dir=args.data_dir,
        config_path=args.config,
        share=args.share,
        debug=args.debug
    )


if __name__ == "__main__":
    cli()
