# ingestion.py

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

def create_vector_store():

    files = ["data/ai.txt", "data/ml.txt"]
    documents = []

    for file in files:
        loader = TextLoader(file, encoding="utf-8")
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    # ⚡ Lightweight embeddings (no download needed)
    embeddings = FakeEmbeddings(size=384)

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vector_db")

    print("✅ Vector database created successfully!")

if __name__ == "__main__":
    create_vector_store()