import fitz
import os
import chromadb
from sentence_transformers import SentenceTransformer
import ollama

chromadb_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "pdf_base"
collection = chromadb_client.get_or_create_collection(name=collection_name)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
DOCS_FOLDER = "./base"

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text() + "\n"
    except Exception as e:
        print(f"Error read PDF {pdf_path}: {e}")
    return text

if not os.path.exists(DOCS_FOLDER):
    os.makedirs(DOCS_FOLDER)
    print(f"{DOCS_FOLDER} was created")

else:
    files_index = 0
    for filename in os.listdir(DOCS_FOLDER):
        file_path = os.path.join(DOCS_FOLDER, filename)
        file_content = ""
        doc_id = f"file_{filename}"

        try:
            existing = collection.get(ids=[doc_id])
            if existing and existing["ids"]:
                continue
        except Exception:
            pass

        if filename.endswith(".pdf"):
            file_content = extract_text_from_pdf(file_path)
        else:
            continue

        if not file_content.strip():
            print("file is empty")
            continue

        vector = embedding_model.encode([file_content]).tolist()

        collection.add(
            documents=[file_content],
            embeddings=vector,
            ids=[doc_id],
            metadatas=[{"source": filename}],
        )
        files_index += 1

if collection.count() == 0:
    print("Base is empty. Put .pdf files into ./base and restart.")
    exit()

user_query = input("Input your query: ").strip()

if not user_query:
    print("no user query")
    exit()

query_embedding = embedding_model.encode([user_query]).tolist()

results = collection.query(query_embeddings=query_embedding, n_results=2)

retrived_chunks = results["documents"][0]
sources = results["metadatas"][0]

for i, (chunk, meta) in enumerate(zip(retrived_chunks, sources)):
    print(f"[{i+1}] Document: {meta['source']}")

context = "\n\n".join(retrived_chunks)

promt = f"""Use ONLY the following contextual data from the files to answer the question.
If the context does not answer the question, say: "I don't have that information in my knowledge base."

Context:
{context}

User query:
{user_query}"""

responce = ollama.chat(
    model="qwen2.5",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a clever assistant who gives answers only in English and only about the provided files."
            )
        },
        {
            "role": "user",
            "content": promt
        }
    ]
)

print("\n--- Response ---")
print(responce["message"]["content"])