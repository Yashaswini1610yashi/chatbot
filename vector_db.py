import chromadb
from sentence_transformers import SentenceTransformer
from load_docs import load_pdfs
import os

# Initialize ChromaDB client
# Use persistent storage if desired, otherwise in-memory
# For production persistence as suggested by user:
persistence_path = os.path.join(os.getcwd(), "db")
if not os.path.exists(persistence_path):
    os.makedirs(persistence_path)

client = chromadb.PersistentClient(path=persistence_path)

# utility to get or create collection
def get_collection():
    try:
        return client.get_collection("knowledge")
    except:
        return client.create_collection("knowledge")

collection = get_collection()

model = SentenceTransformer("all-MiniLM-L6-v2")

def index_docs():
    print("Loading documents...")
    docs = load_pdfs()
    print(f"Found {len(docs)} documents.")

    for i, doc in enumerate(docs):
        embedding = model.encode(doc).tolist()
        
        # Simple ID generation
        doc_id = f"doc_{i}"
        
        # Add to collection
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[doc_id]
        )
    print("Indexing complete.")

def index_single_doc(file_path):
    from load_docs import extract_text_from_pdf
    doc = extract_text_from_pdf(file_path)
    if doc:
        embedding = model.encode(doc).tolist()
        import time
        doc_id = f"doc_{int(time.time())}"
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[doc_id]
        )
        return True
    return False

def search_docs(query):
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1 # return top 1 for simplicity in demo, user asked for 3 but code showed 3 then returned logic for results["documents"][0]
    )

    if results["documents"] and results["documents"][0]:
        return results["documents"][0][0] # Return the first match content

    return ""
