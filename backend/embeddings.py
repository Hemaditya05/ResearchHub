import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="research_papers"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def store_paper(paper_id, content):
    embedding = model.encode(content).tolist()

    collection.add(
        ids=[str(paper_id)],
        embeddings=[embedding],
        documents=[content]
    )


def search_papers(query):
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    return results
    