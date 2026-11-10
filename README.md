# AI PDF RAG Assistant

A command-line Retrieval-Augmented Generation (RAG) application that answers questions about a PDF. It splits the document into text chunks, creates embeddings with Google's Gemini embedding model, and stores them in a local Qdrant vector database. For each question, it retrieves relevant chunks and asks Gemini to generate an answer grounded in that content.

## How it works

1. `index.py` loads `my-profile.pdf`, splits its text into overlapping chunks, generates Gemini embeddings, and stores the chunks in Qdrant.
2. `chat.py` searches Qdrant for chunks relevant to your question and sends them as context to Gemini.
3. The response includes source page information to help you locate the relevant content in the PDF.

## Requirements

- Python 3.10 or later
- Docker Desktop or Docker Engine with Docker Compose
- A Google AI API key with access to the configured Gemini models

## Run locally

### 1. Get the project

Clone the repository and change into the project directory:

```bash
git clone <repository-url>
cd Rag
```

### 2. Add a PDF

Place a PDF named `my-profile.pdf` in the project directory, alongside `index.py`.

> PDF files are excluded from Git, so the document may not be included when you clone the repository. Add your own PDF and name it `my-profile.pdf`.

### 3. Configure your API key

Create a `.env` file in the project directory:

```env
GOOGLE_API_KEY=your_google_api_key
```

Keep your API key private. Do not commit `.env` to Git.

### 4. Create a virtual environment and install dependencies

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install langchain-community langchain-text-splitters langchain-google-genai langchain-qdrant openai python-dotenv pypdf
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install langchain-community langchain-text-splitters langchain-google-genai langchain-qdrant openai python-dotenv pypdf
```

### 5. Start Qdrant

From the project directory, start the local vector database:

```bash
docker compose up -d
```

Qdrant's HTTP API will be available at `http://localhost:6333`.

### 6. Index the PDF

With Qdrant running and your virtual environment activated, run:

```bash
python index.py
```

Wait for the indexing-completed message before proceeding.

### 7. Ask a question

Run the chat script:

```bash
python chat.py
```

Enter a question at the prompt to receive an answer based on the indexed PDF.

When finished, stop Qdrant with:

```bash
docker compose down
```

## Project files

- `index.py` — loads, chunks, embeds, and indexes the PDF.
- `chat.py` — retrieves relevant content and generates an answer.
- `docker-compose.yml` — defines the local Qdrant service.
- `.gitignore` — excludes `.env` and PDF files from Git.

## Notes

- Run `index.py` before `chat.py`. The chat script expects the `learning_rag` collection to exist in Qdrant.
- Both scripts use `GOOGLE_API_KEY` from `.env` for Gemini API access.
- The embedding and chat model names are configured in `index.py` and `chat.py`.
