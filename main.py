"""
Legacy main.py file for backward compatibility.

This file is kept for backward compatibility. 
The main application has been moved to src/book_recommender/main.py

For new installations, please use:
    python src/book_recommender/main.py
    
Or install the package and use:
    pip install -e .
    book-recommender
"""

import sys
import warnings
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from book_recommender.main import main

    warnings.warn(
        "Using legacy main.py. Please use 'python src/book_recommender/main.py' or install the package.",
        DeprecationWarning,
        stacklevel=2
    )

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error importing main application: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)
