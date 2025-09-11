import google.generativeai as genai
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

emb_model = "models/text-embedding-004"
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

db_client = chromadb.PersistentClient("VectorDB")

collections = db_client.get_or_create_collection(
    name="Embeddings",
    configuration=emb_model)

