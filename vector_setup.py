import chromadb
import csv

client = chromadb.Client()
collection = client.get_or_create_collection(name='medical_notes')


def ingest_notes(csv_path: str):
    """Ingest medical notes from a CSV file into ChromaDB"""
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            patient_id = row["patient_id"]
            symptoms = row["symptoms"]
            collection.add(
                documents=[symptoms],
                metadatas=[row],
                ids=[patient_id]
            )

ingest_notes("healthcare_patient_records.csv")

def query_notes(symptoms: str, top_k: int = 1):
    """Query medical notes based on input symptoms"""
    results = collection.query(query_texts=[symptoms], n_results=top_k)

    output = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        result = {
            "Symptoms": doc,
            "Diagnosis": metadata.get("diagnosis", "N/A"),
            "Treatment": metadata.get("treatment", "N/A"),
            "Doctor Notes": metadata.get("doctor_notes", "N/A")
        }
        output.append(result)

    return output
