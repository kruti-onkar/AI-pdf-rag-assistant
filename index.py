
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "my-profile.pdf"

# Load PDF
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=40
)

chunks = text_splitter.split_documents(documents=docs)

# Generate embeddings using Gemini
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# Store embeddings in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("Indexing of documents completed!")
