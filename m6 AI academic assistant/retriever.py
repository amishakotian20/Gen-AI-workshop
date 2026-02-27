# retriever.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

def get_retriever():

    embeddings = FakeEmbeddings(size=384)

    db = FAISS.load_local(
        "vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db.as_retriever(search_kwargs={"k": 3})