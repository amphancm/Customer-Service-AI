# Import necessary libraries
import numpy as np
import pandas as pd
from pathlib import Path
import os
import json
import hashlib
import time
import PyPDF2
from typing import List, Optional, Union, Dict, Any

from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointsSelector, Filter
from tqdm import tqdm


class QdrantRAG:
    """A class to manage a RAG pipeline using Qdrant with disk-based storage."""

    def __init__(
        self,
        storage_path: str,
        model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        dimension: int = 768,
        collection_name: str = "Base-Knowledge",
    ):
        """
        Initialize the RAG pipeline with disk-based Qdrant storage.

        Args:
            storage_path (str): Path to store Qdrant data on disk.
            model_name (str): HF embedding model name.
            dimension (int): Vector dimension (must match embedding model output).
            collection_name (str): Name of the Qdrant collection.
        """
        self.model_name = model_name
        self.dimension = dimension
        self.storage_path = Path(storage_path)
        self.collection_name = collection_name
        self.qdrant_client = None
        self.index = None

        # manifest path to record what has been ingested
        self.manifest_path = self.storage_path / f"{self.collection_name}_manifest.jsonl"
        self._manifest_cache = set()  # in-memory set of keys for fast lookup

        self._setup_environment()
        self._initialize_qdrant()
        self._initialize_index()
        self._load_manifest()

    # ---------------------- internal utilities (manifest) ----------------------

    def _load_manifest(self) -> None:
        """Load (or create) the ingestion manifest."""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            if self.manifest_path.exists():
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                            key = rec.get("key")
                            if key:
                                self._manifest_cache.add(key)
                        except json.JSONDecodeError:
                            # Skip bad lines (rare)
                            continue
            else:
                # create empty file
                self.manifest_path.touch(exist_ok=True)
        except Exception as e:
            print(f"Warning: could not load manifest: {e}")

    def _append_manifest(self, record: Dict[str, Any]) -> None:
        """Append a record to the manifest and update cache."""
        try:
            key = record.get("key")
            if key and key not in self._manifest_cache:
                with open(self.manifest_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                self._manifest_cache.add(key)
        except Exception as e:
            print(f"Warning: could not append to manifest: {e}")

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _file_fingerprint(self, path: Path) -> str:
        """Create a stable key from file path + size + mtime (no file read needed)."""
        try:
            stat = path.stat()
            size = stat.st_size
            mtime = int(stat.st_mtime)
            return f"file://{str(path.resolve())}|{size}|{mtime}"
        except FileNotFoundError:
            # fallback—include current time to avoid collisions
            return f"file://{str(path.resolve())}|missing|{int(time.time())}"

    # ---------------------- environment / qdrant / index ----------------------

    def _setup_environment(self) -> None:
        """Set up the environment with necessary configurations and embeddings."""
        try:
            Settings.llm = None
            Settings.embed_model = HuggingFaceEmbedding(model_name=self.model_name)  # e.g., BAAI/bge-m3 if you switch
            Settings.node_parser = SentenceSplitter(chunk_size=256, chunk_overlap=32)
            print("Environment setup completed successfully")
        except Exception as e:
            print(f"Error setting up environment: {str(e)}")
            raise

    def _initialize_qdrant(self) -> None:
        """Initialize Qdrant client in disk-based mode."""
        try:
            # Ensure storage path exists and is writable
            self.storage_path.mkdir(parents=True, exist_ok=True)
            if not os.access(self.storage_path, os.W_OK):
                raise PermissionError(f"No write permission for storage path: {self.storage_path}")

            # Initialize Qdrant client in disk-based mode
            self.qdrant_client = QdrantClient(path=str(self.storage_path))
            print(f"Qdrant client initialized with disk storage at {self.storage_path}")

            if not self.qdrant_client.collection_exists(self.collection_name):
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=self.dimension, distance=models.Distance.COSINE),
                )
                print(f"Collection '{self.collection_name}' created successfully")
            else:
                print(f"Collection '{self.collection_name}' already exists (reusing)")
        except Exception as e:
            print(f"Error initializing Qdrant client: {str(e)}")
            print("Ensure the storage path is valid and writable. Check qdrant-client version compatibility.")
            raise

    def _initialize_index(self) -> None:
        """Initialize a VectorStoreIndex with Qdrant."""
        print(f"Initializing index for collection '{self.collection_name}'")
        try:
            vector_store = QdrantVectorStore(client=self.qdrant_client, collection_name=self.collection_name)
            # If collection already has vectors, VectorStoreIndex will wrap it; otherwise it remains empty.
            self.index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
            print(f"Index ready for collection '{self.collection_name}'")
        except Exception as e:
            print(f"Error initializing index: {str(e)}")
            raise


    def add_data(
        self,
        data: Union[str, List[str], Path, List[Path]],
        reload: bool = True,
    ) -> None:
        try:
            if not self.index:
                raise ValueError("Index not initialized. Call constructor first.")

            documents: List[Document] = []
            planned_records: List[Dict[str, Any]] = []

            def _maybe_queue_doc(key: str, make_doc_fn, meta: Dict[str, Any]) -> None:
                if not reload and key in self._manifest_cache:
                    print(f"Reload=False → Skipping already ingested item: {meta.get('source','<unknown>')}")
                    return
                doc = make_doc_fn()
                if doc is not None and doc.text and doc.text.strip():
                    documents.append(doc)
                    rec = {"key": key, **meta, "ts": int(time.time())}
                    planned_records.append(rec)

            # ---------------- Handle raw strings ----------------
            if isinstance(data, str) and not Path(data).exists():
                text = data
                key = f"str://{self._hash_text(text)}"
                _maybe_queue_doc(key, lambda: Document(text=text), {"type": "string"})

            elif isinstance(data, list) and all(isinstance(item, str) and not Path(item).exists() for item in data):
                for text in data:
                    key = f"str://{self._hash_text(text)}"
                    _maybe_queue_doc(key, lambda t=text: Document(text=t), {"type": "string_list"})

            else:
                # ---------------- Handle files/folders ----------------
                file_paths: List[Path] = []
                if isinstance(data, (str, Path)) and Path(data).is_dir():
                    folder_path = Path(data)
                    print(f"Scanning folder {folder_path} for files...")
                    if not folder_path.exists():
                        raise FileNotFoundError(f"Folder {folder_path} does not exist")
                    for ext in ["*.txt", "*.pdf", "*.csv"]:
                        file_paths.extend(folder_path.rglob(ext))
                else:
                    if isinstance(data, (str, Path)):
                        file_paths = [Path(data)]
                    else:
                        file_paths = [Path(item) for item in data]

                for file_path in file_paths:
                    if not file_path.exists():
                        print(f"Warning: File {file_path} does not exist, skipping")
                        continue

                    suffix = file_path.suffix.lower()
                    fp_key = self._file_fingerprint(file_path)

                    if suffix == ".txt":
                        _maybe_queue_doc(
                            fp_key,
                            lambda p=file_path: Document(text=open(p, "r", encoding="utf-8").read()),
                            {"type": "file_txt", "source": str(file_path)},
                        )

                    elif suffix == ".pdf":
                        def _make_doc_pdf(p=file_path):
                            text = ""
                            with open(p, "rb") as f:
                                pdf_reader = PyPDF2.PdfReader(f)
                                for page in pdf_reader.pages:
                                    page_text = page.extract_text()
                                    if page_text:
                                        text += page_text
                            if not text.strip():
                                print(f"Warning: No text extracted from {p}, skipping")
                                return None
                            return Document(text=text)

                        _maybe_queue_doc(fp_key, _make_doc_pdf, {"type": "file_pdf", "source": str(file_path)})

                    elif suffix == ".csv":
                        df = pd.read_csv(file_path)

                        for idx, row in df.iterrows():
                            # join all non-NaN column values into one string
                            values = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip()]
                            if not values:
                                continue
                            text = " | ".join(values)   # or use "," / "\t" depending on your style

                            row_key = f"csv://{str(file_path.resolve())}|{idx}|{self._hash_text(text)}"
                            _maybe_queue_doc(
                                row_key,
                                lambda v=text: Document(text=v),
                                {
                                    "type": "file_csv_row",
                                    "source": str(file_path),
                                    "row_index": int(idx)
                                },
                            )

                    else:
                        print(f"Warning: Unsupported file type {suffix} for {file_path}, skipping")

            # ---------------- Insert with tqdm ----------------
            if documents:
                print(f"Preparing to insert {len(documents)} document(s) into '{self.collection_name}' ...")
                for doc in tqdm(documents, desc="Inserting documents", unit="doc"):
                    self.index.insert(doc)

                # update manifest only after successful inserts
                for rec in planned_records:
                    self._append_manifest(rec)

                # log collection size
                coll_info = self.qdrant_client.get_collection(self.collection_name)
                total_points = coll_info.points_count
                print(
                    f"✅ Successfully added {len(documents)} new document(s). "
                    f"Current total in collection '{self.collection_name}': {total_points}"
                )
            else:
                print("No new documents to add (empty or skipped with reload=False).")

        except Exception as e:
            print(f"Error adding data to collection: {str(e)}")
            raise

    # ---------------------- querying ----------------------

    def query(self, query: str, top_k: int = 10) -> str:
        """
        Perform RAG query on the indexed data.

        Args:
            query (str): The query string.
            top_k (int): Number of top results to retrieve.

        Returns:
            str: Query response.
        """
        try:
            if not self.index:
                raise ValueError("Index not initialized.")
            query_engine = self.index.as_query_engine(similarity_top_k=top_k)
            response = query_engine.query(query)
            return str(response)
        except Exception as e:
            print(f"Error performing RAG query: {str(e)}")
            return f"Error: {str(e)}"

    # ---------------------- destructive ops ----------------------

    def deleteCollection(self) -> None:
        """Delete the Qdrant collection and its local manifest."""
        try:
            self.qdrant_client.delete_collection(collection_name=self.collection_name)
            if not self.qdrant_client.collection_exists(self.collection_name):
                print("Collection successfully deleted.")
            else:
                print("Collection still exists (delete may have failed).")
        except Exception as e:
            print(f"Error deleting collection: {e}")

        # Also remove manifest so a future reload=False won't think old items exist
        try:
            if self.manifest_path.exists():
                self.manifest_path.unlink()
            self._manifest_cache.clear()
            print("Ingestion manifest removed.")
        except Exception as e:
            print(f"Warning: could not remove manifest: {e}")
