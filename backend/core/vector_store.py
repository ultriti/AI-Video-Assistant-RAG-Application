from dotenv import load_dotenv

load_dotenv()

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document

CHROMA_DB = r"backend\vector_db"
COLLECTION_NAME = "meeting_transcription"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------
# get embeddings from model
def get_embedding():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"device": "cpu"})


# ---------------------------
# vector store ( embedding creation ) - store it


def build_vector_store(transcript: str) -> Chroma:
    print("vector store")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(transcript)

    docs = [
        Document(page_content=chunk, metadata={"chunk_index": i})
        for i, chunk in enumerate(chunks)
    ]

    embeddings = get_embedding()
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,   # singular
        persist_directory=CHROMA_DB,
    )

    return vector_store


# -----------------------------------
# load the vector store


def load_vector_store() -> Chroma:
    embeddings = get_embedding()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_funtion=embeddings,
        persist_directory=CHROMA_DB,
    )

    return vector_store


# ----------------------------------
# retriver from vector store


def get_retriver(vector_store: Chroma, k: int = 4):
    retriver = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    return retriver
