import csv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load sentence transformer model for embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FAISS index (assumes 384-dim from above model)
dimension = 384
index = faiss.IndexFlatL2(dimension)

# Metadata store
metadata_store = {}  # key: vector index, value: metadata dict
vector_id = 0

def ingest_notes(csv_path: str):
    global vector_id
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        vectors = []
        for row in reader:
            symptoms = row["symptoms"]
            embedding = model.encode(symptoms)
            vectors.append(embedding)

            # Save metadata
            metadata_store[vector_id] = {
                "Symptoms": symptoms,
                "Diagnosis": row.get("diagnosis", "N/A"),
                "Treatment": row.get("treatment", "N/A"),
                "Doctor Notes": row.get("doctor_notes", "N/A")
            }
            vector_id += 1

        # Convert list to numpy array and add to FAISS
        vectors_np = np.array(vectors).astype("float32")
        index.add(vectors_np)
ingest_notes('healthcare_patient_records.csv')

def query_notes(symptom_query: str, top_k: int = 1):
    embedding = model.encode([symptom_query]).astype("float32")
    distances, indices = index.search(embedding, top_k)

    output = []
    for idx in indices[0]:
        if idx in metadata_store:
            output.append(metadata_store[idx])

    return output
