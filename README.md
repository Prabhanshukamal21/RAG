# Local RAG Chatbot

## Features
- Upload PDF, TXT, and DOCX files
- Extract text, split into overlapping chunks, embed with Sentence Transformers
- Persist embeddings in ChromaDB
- Semantic Top-K retrieval
- Answer using a local Ollama LLM and display retrieved evidence

## Windows PowerShell setup
Python 3.10 or 3.11 is recommended.

```powershell
cd path\to\rag_chatbot_system
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Ollama from https://ollama.com/download, then run:

```powershell
ollama pull llama3.2
streamlit run app.py
```

Open the Streamlit URL shown in the terminal, usually http://localhost:8501. Keep Ollama running while using the chatbot.

## Pipeline
Documents -> text extraction -> chunking -> embeddings -> ChromaDB.
Question -> query embedding -> semantic retrieval -> context + question -> Ollama -> answer.

## Notes
- First run downloads the embedding model.
- Scanned PDFs need OCR; this starter handles PDFs with selectable text.
- ChromaDB persists under `data/chroma_db`.
- This is a starter project: it uses dense semantic retrieval, not hybrid BM25 search or reranking.
