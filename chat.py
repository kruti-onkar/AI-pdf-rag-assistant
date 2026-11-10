from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI
import os
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# Generate embeddings using Gemini
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

#take user input
user_input = input("ask user query-->")
search_results = vector_db.similarity_search(query= user_input)
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
You are a helpful AI assistent who answers user query based on available context, Retrived from a pdf file along weit page contents and page number.

you should only answer the user based on the following context and navigate the user to open the right page to know more.

Context:{context}
 """

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

interactions = client.chat.completions.create(
                    model="gemini-3.5-flash-lite",
                    messages= [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input},
                    ]
                )
print(f"🤖-> {interactions.choices[0].message.content}")
