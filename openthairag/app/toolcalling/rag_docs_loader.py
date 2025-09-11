from .rag_documents.index import QdrantRAG
from pathlib import Path

rag = QdrantRAG(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",dimension=384,storage_path="./qdrant_storage", collection_name="Base-Knowledge")
DOC_DIR = Path(__file__).resolve().parent.parent / 'documents'
doc_dir = Path(DOC_DIR)


def load_docs():
    rag.add_data(DOC_DIR, reload=True)

def rag_docs_query(question, top_k=3):
    """
    Query the RAG document index and return the top-k matching snippets.

    Args:
        question (str): Natural-language question (TH/EN supported).
        top_k (int, optional): Number of results to return. Defaults to 3.

    Returns:
        List[str]: Ranked snippets answering the question.

    Example:
        >>> rag_docs_query("ยาที่ใช้แก้ปวด", top_k=5)
        ["ยา A ...", "ยา B ...", ...]
    """
    rag.add_data(DOC_DIR, reload=False)
    return rag.query(question, top_k=10)
