from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, utility, DataType
from transformers import AutoTokenizer, AutoModel
import logging
import torch ,sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

MILVUS_HOST = '172.18.0.5'
MILVUS_PORT = '19530'
# Rerank documents based on cosine similarity
def rerank_documents(query_embedding, document_embeddings):
    # Ensure query_embedding is a 2D array
    if isinstance(query_embedding, list):
        query_embedding = np.array(query_embedding).reshape(1, -1)
    elif isinstance(query_embedding, np.ndarray):
        query_embedding = query_embedding.reshape(1, -1)
    
    # Ensure document_embeddings is a 2D array
    if isinstance(document_embeddings, list):
        document_embeddings = np.array(document_embeddings)
    if len(document_embeddings.shape) == 1:
        document_embeddings = document_embeddings.reshape(1, -1)
    
    # Check if document_embeddings is empty
    if document_embeddings.size == 0:
        logging.warning("Document embeddings array is empty")
        return []
    
    # logger.debug(f"Query embedding shape: {query_embedding.shape}, Document embeddings shape: {document_embeddings.shape}")
    # logger.debug(f"Query embedding: {query_embedding}, Document embeddings: {document_embeddings}")
    
    similarities = cosine_similarity(query_embedding, document_embeddings)
    ranked_documents = sorted(enumerate(similarities.flatten()), key=lambda x: x[1], reverse=True)
    return ranked_documents

def generate_embedding(text, free=False):
    logger.debug("Generating embedding for chunk of length %d", len(text))
    inputs = bge_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = bge_model(**inputs).pooler_output
    return embeddings

def initialize_milvus_collection():
    logger.info("Initializing Milvus collection...")
    if not utility.has_collection("document_embeddings"):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="chunk_index", dtype=DataType.INT64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields, "Document embeddings for Information database")
        collection = Collection("document_embeddings", schema)
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index("embedding", index_params)
        logger.info("Created new collection and index.")
    else:
        collection = Collection("document_embeddings")
        logger.info("Using existing collection.")
    return collection

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n", "\n", " ", ".", ",",
        "\u200b", "\uff0c", "\u3001", "\uff0e", "\u3002", ""
    ],
)

def split_and_print_chunks(text, text_splitter, collection, document_id="pride_and_prejudice", max_length=200, batch_size=1000):
    logger.info("Splitting document into chunks...")
    initial_chunks = text_splitter.create_documents([text])
    final_chunks = []
    for doc in initial_chunks:
        if len(doc.page_content) > max_length:
            logger.debug("Chunk length %d exceeds max_length %d, splitting further.", len(doc.page_content), max_length)
            sub_chunks = text_splitter.create_documents([doc.page_content])
            final_chunks.extend(sub_chunks)
        else:
            final_chunks.append(doc)
    logger.info("Total chunks to insert: %d", len(final_chunks))

    # Batch insert
    document_ids = []
    chunk_indexes = []
    embeddings = []
    texts = []
    for idx, doc in enumerate(final_chunks):
        logger.debug("Processing chunk %d, length %d", idx, len(doc.page_content))
        embedding = generate_embedding(doc.page_content).squeeze().tolist()
        document_ids.append(document_id)
        chunk_indexes.append(idx)
        embeddings.append(embedding)
        texts.append(doc.page_content)
        # Insert in batches
        if (idx + 1) % batch_size == 0 or (idx + 1) == len(final_chunks):
            logger.debug("Batch inserting %d chunks into Milvus...", len(document_ids))
            collection.insert([
                document_ids,
                chunk_indexes,
                np.array(embeddings, dtype=np.float32),
                texts
            ], flush=False)
            document_ids, chunk_indexes, embeddings, texts = [], [], [], []
    collection.flush()
    logger.info("All chunks batch inserted.")
    return final_chunks

logger.info("Connecting to Milvus at %s:%s...", MILVUS_HOST, MILVUS_PORT)
connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
collection = initialize_milvus_collection()
logger.info("Successfully connected with MILVUS database.")

logger.info("Loading BAAI/bge-m3 embedding model and tokenizer...")
bge_model = AutoModel.from_pretrained("BAAI/bge-m3")
bge_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
logger.info("Successfully loaded BAAI/bge-m3 embedding and tokenizer. Ready to serve.")


def query_documents(query, collection, top_k=10, rerank_top_n=3, system_prompt="", arr_history=None):
    logger.info("Querying documents for: %s", query)
    query_embedding = generate_embedding(query).numpy().flatten().tolist()

    search_param = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }

    if not collection.is_empty:
        collection.load()

    search_results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_param,
        limit=top_k,
        output_fields=["id", "document_id", "chunk_index", "embedding", "text"],
        expr=None
    )

    retrieved_documents = []
    document_embeddings = []
    for hits in search_results:
        for hit in hits:
            retrieved_documents.append(hit.entity)
            embedding = hit.entity.get('embedding')
            if embedding is not None:
                document_embeddings.append(embedding)

    ranked_indices = rerank_documents(query_embedding, document_embeddings)
    top_documents = [retrieved_documents[i] for i, _ in ranked_indices[:rerank_top_n]]

    prompt = f"จากเอกสารต่อไปนี้\n\n"
    prompt += "\n\n".join([doc.get('text') for doc in top_documents])

    # --- Added ChatML prompt construction ---
    prompt_chatml = []
    if arr_history is None:
        arr_history = []
    prompt_chatml.append({
        'role': 'system',
        'content': 'คุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์ โปรดเลือกใช้ function get_more_detail ก่อนการตัดสินใจในการตอบคำถาม และเชื่อในข้อมูลจาก เอกสารเหล่านี้เท่านั้น \n\n' + system_prompt + '\n\n' + prompt
    })
    for dat in arr_history:
        prompt_chatml.append(dat)
    prompt_chatml.append({
        'role': 'user',
        'content': query
    })
    # --- End ChatML prompt construction ---
    logger.info("prompt_chatml", prompt_chatml)

    return prompt, top_documents, prompt_chatml

def insert_document(document_path, collection, document_id="pride_and_prejudice", max_length=200):
    logger.info("Inserting document from %s with ID %s", document_path, document_id)
    with open(document_path) as f:
        state_of_the_union = f.read()
        VARCHAR_LIMIT = 65535
        if len(state_of_the_union) > VARCHAR_LIMIT:
            logger.info("Document exceeds VARCHAR limit (%d), splitting and inserting...", VARCHAR_LIMIT)
            split_and_print_chunks(state_of_the_union, text_splitter, collection, document_id=document_id, max_length=max_length)
        else:
            logger.info("Document within VARCHAR limit, no chunking required.")
            
    # with open(document_path, "r", encoding="utf-8") as f:
    #     text = f.read()
    # split_and_print_chunks(text, text_splitter, collection, document_id=document_id, max_length=max_length)


def process_openai_chat(prompt_chatml, 
                        api_domain="https://openrouter.ai/api/v1", 
                        api_key='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', 
                        model_name="deepseek/deepseek-chat-v3-0324:free", 
                        temperature=0.01):
    """
    Calls the OpenAI chat completion API and returns the assistant's message.
    """
    from openai import OpenAI
    client = OpenAI(
        base_url=api_domain,
        api_key=api_key,
    )
    try:
        print("Creating ChatCompletion...")
        response = client.chat.completions.create(
            model=model_name,
            messages=prompt_chatml,
            temperature=float(temperature) if temperature != '' else 0.5,
        )
        assistant_message = response.choices[0].message
        print("Assistant:", assistant_message.content)
        return assistant_message.content
    except Exception as e:
        print("Error during chat completion:", e)
        return None

def  process():
    prompt, docs, prompt_chatml = query_documents("เทพชื่ออะไรที่ชาวดิกเมอร์ยกย่องท่านในฐานะผู้นาพวกเขาออกจากดินแดนของชาวอัลต์เมอร์", collection)
    LLM_API_DOMAIN = "https://openrouter.ai/api/v1"
    LLM_API_KEY = "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"
    LLM_MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"
    temperature = 0.1

    process_openai_chat(
        prompt_chatml,
        api_domain=LLM_API_DOMAIN,
        api_key=LLM_API_KEY,
        model_name=LLM_MODEL_NAME,
        temperature=temperature
    )
try:
    #insert_document('/home/meownani/llm_agent/skyrim_story_chapters_1_50.txt', collection, document_id="pride_and_prejudice", max_length=200)
    process()
except Exception as e:
    logger.error("Error inserting document: %s", e)
    sys.exit()

