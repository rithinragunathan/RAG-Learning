import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
from disease import main


folder_path = "folder/"

def get_embedding(text_content: str, emb_model: str) -> list[float]:
    """Generates an embedding for the given text content."""
    try:
        embedding = genai.embed_content(model=emb_model, content=text_content)["embedding"]
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

def logic():
    # ---- Step 0: Load environment variables ----
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    emb_model = "models/text-embedding-004" 
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    # ---- Step 1: Init ChromaDB ----
    db_client = chromadb.PersistentClient("VectorDB")

    collection_name = "Embeddings_fresh"
    if collection_name in [col.name for col in db_client.list_collections()]:
        db_client.delete_collection(collection_name)
    collection = db_client.get_or_create_collection(name=collection_name)

    # ---- Step 2: Load text file ----
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder not found at: {folder_path}")

    all_texts = [] # List to store content from all text files
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    all_texts.append(f.read()) # Append content to the list
            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    if not all_texts:
        return "No text files found or readable in the specified folder."

    # Join all texts into a single string for chunking
    # Alternatively, you could chunk each file's content individually
    combined_text = "\n".join(all_texts)

    # ---- Step 3: Chunk text ----
    chunk_size = 500
    overlap = 20
    chunks = [combined_text[i:i+chunk_size] for i in range(0, len(combined_text), chunk_size - overlap)]

    # ---- Step 4: Create embeddings and add to ChromaDB ----
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk, emb_model)
        if emb: # Only add if embedding was successful
            collection.add(ids=[f"chunk_{i}"], embeddings=[emb], documents=[chunk])
        else:
            print(f"Skipping chunk {i} due to embedding error.")

    # ---- Step 5: Query top chunks for fixed question ----
    query = main()
    query_emb = get_embedding(query, emb_model)
    if not query_emb:
        return "Error: Could not generate embedding for the query."

    results = collection.query(query_embeddings=[query_emb], n_results=3)
    
    if results and results.get('documents') and results['documents'][0]:
        context_text = " ".join(results['documents'][0])
    else:
        return "No relevant documents found for the query."

    # ---- Step 6: Ask model with retrieved context ----
    prompt = f"Here is some text from a document:\n{context_text}\n\nQuestion: {query} how to prevent it\nAnswer:"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content from model: {e}"

# Example usage
if __name__ == "__main__":
    print(logic())
    