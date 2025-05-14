# 📚 Book Recommender System

A semantic book recommendation web app that suggests books based on your mood, preferences, and a natural language description — powered by sentence embeddings, LangChain, and ChromaDB.

---

## 🌟 Features

- 🔍 **Semantic Search**: Uses sentence-level embeddings to find books similar to your query.
- 🎭 **Emotion-Based Filtering**: Filter results based on emotional tone (Happy, Sad, Angry, etc.).
- 🧠 **AI-Driven**: Embeddings powered by HuggingFace (`all-MiniLM-L6-v2`).
- 🎨 **Clean UI**: Built with Gradio for an interactive, modern frontend.
- 📦 **Self-contained**: Uses local ChromaDB for fast retrieval.

---

## 🚀 Demo

![Book Recommender UI](screenshot.png)

> 📌 _Replace `screenshot.png` with your actual screenshot file name or a link._

---

## 🧠 How It Works

1. **Text Data**: Book descriptions are pre-tagged with emotional sentiment scores.
2. **Text Embeddings**: Descriptions are converted into vector embeddings.
3. **Vector Search**: Query is embedded and compared using cosine similarity via ChromaDB.
4. **Filtering**: Users can refine results by category and tone.

---

## 🛠 Tech Stack

- 🐍 Python
- 🤗 HuggingFace Transformers (`all-MiniLM-L6-v2`)
- 🧱 ChromaDB (vector store)
- 🔗 LangChain for semantic search
- 📊 Pandas & NumPy for data wrangling
- 🌐 Gradio for the web UI

---

## 📁 Project Structure

book-recommender-system/
│
├── main.py # Main app file (Gradio + logic)
├── books_with_emotions.csv # CSV dataset with book metadata & emotion scores
├── tagged_description.txt # Preprocessed tagged descriptions
├── requirements.txt # Required dependencies
└── README.md # This file
