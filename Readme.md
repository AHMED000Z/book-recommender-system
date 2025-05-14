# 📚 Book Recommender System

A semantic book recommender system using LangChain, HuggingFace embeddings, Gradio, and ChromaDB. This project takes user input in natural language and recommends books based on semantic similarity, emotional tone, and simplified categories.

---

## 🚀 Features

- Vector search using LangChain + HuggingFace embeddings
- Sentiment-based filtering (Happy, Sad, Angry, etc.)
- Category classification using Zero-shot learning
- Clean and responsive Gradio UI with dark mode
- Text truncation and thumbnail preview for visual appeal

---

## 🗂️ Project Structure

book-recommender-system/
├── data/
│ ├── books.csv # Raw dataset
│ ├── books cleaned.csv # Cleaned dataset
│ ├── books with emotions.csv # Dataset enriched with emotion scores
│ └── tagged_description.txt # Descriptions used for vector search
│
├── notebooks/
│ ├── data-exploration.ipynb # EDA and data cleaning
│ ├── vector_search.ipynb # Building semantic search
│ ├── sentiment_analysis.ipynb # Adding emotions to data
│ └── text_classification.ipynb # Category simplification using zero-shot
│
│
├── main.py # Main Gradio app
├── requirements.txt # Dependencies
├── .gitignore
├──missing_cover.png
└── README.md
