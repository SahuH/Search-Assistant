import os
import json
import chromadb
from chromadb.config import Settings

# Load synonym mapping
BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "../data/metadata_searchDB.json", "r")) as f:
    synonym_mapping = json.load(f)

# Reverse lookup for synonyms
synonym_to_field = {}
for field, synonyms in synonym_mapping.items():
    for synonym in synonyms:
        synonym_to_field[synonym.lower()] = field

# Example function (mocking actual LLM usage)
def mock_llm_metadata_extraction(query: str):
    return [
    {"attribute": "bedrooms", "condition": "==", "value": 3},
    {"attribute": "guests", "condition": ">=", "value": 6},
    {"attribute": "baths", "condition": ">=", "value": 2}
    ]

# Metadata filtering using ChromaDB
def retrieve_with_metadata_filtering(query: str):
    filters = mock_llm_metadata_extraction(query)

    # client = chromadb.Client(Settings(
    #     chroma_db_impl="duckdb+parquet",
    #     persist_directory="./chroma_store"  # your path here
    # ))


    # collection = client.get_collection("real_estate")

    CHROMA_DIR = "../data/chroma_store"
    COLLECTION_NAME = "airbnb_properties"

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

    exact_filters = {}
    for f in filters:
        if f["condition"] == "==":
            exact_filters[f["attribute"]] = f["value"]
        elif f["condition"] == "includes":
            for val in f["value"]:
                exact_filters[f"{f['attribute']}_{val}"] = True

    results = collection.query(
        query_texts=[query],
        n_results=10,
        where=exact_filters
    )
    return results


import torch
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load same embedding model used earlier
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # or whatever you used

# ---- Step 1: Get query embedding ----
def embed_query(query: str):
    return embedding_model.encode(query, convert_to_tensor=True)

# ---- Step 2: Get property card embeddings from metadata-filtered results ----
def rerank_candidates(query: str, metadata_results: dict, top_k: int = 5):
    query_embedding = embed_query(query)

    property_texts = metadata_results["documents"][0]  # List of property cards (text)
    candidate_embeddings = embedding_model.encode(property_texts, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.cos_sim(query_embedding, candidate_embeddings)[0]  # shape: [n_candidates]

    # Get top-k indices
    top_k_indices = torch.topk(similarities, top_k).indices

    # Collect top-k results
    top_properties = []
    for idx in top_k_indices:
        idx = idx.item()
        top_properties.append({
            "property_text": property_texts[idx],
            "score": similarities[idx].item(),
            "metadata": metadata_results["metadatas"][0][idx],
            "id": metadata_results["ids"][0][idx]
        })

    return top_properties



# query = "Looking for a 3-bedroom place that can accommodate at least 6 guests, with 2 bathrooms."
# metadata_results = retrieve_with_metadata_filtering(query)
# top_properties = rerank_candidates(query, metadata_results, top_k=5)

# for i, prop in enumerate(top_properties):
#     print(f"\n🏠 Property #{i+1}")
#     print(f"Text: {prop['property_text']}")
#     print(f"Score: {prop['score']:.4f}")
#     print(f"Metadata: {prop['metadata']}")
#     print(f"ID: {prop['id']}")