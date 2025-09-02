from rag_documents.index import QdrantRAG
from pathlib import Path

rag = QdrantRAG(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",dimension=384,storage_path="./qdrant_storage", collection_name="Base-Knowledge")

doc_dir = Path(r"C:\Users\tonkl\OneDrive\Documents\llm_agent\openthairag\app\documents")

"""
rag.add_data(doc_dir, reload=False)
print(rag.query("สินค้า?",top_k=3))
"""
