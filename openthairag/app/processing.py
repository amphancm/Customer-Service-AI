from flask import Flask, request, jsonify, Response
from toolcalling.tools import get_tools
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, utility, DataType
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import os
import datetime
import numpy as np
import logging
from db import Connection
from bson.json_util import dumps
from openai import OpenAI
import json
from toolcalling.tool_function import *
from db import Connection

from together import Together
from toolcalling import rag_docs_query, get_time_context, rag_sql_query
from dotenv import load_dotenv
load_dotenv()

mongo=Connection('otg_db')

MILVUS_HOST = os.environ.get('MILVUS_HOST', 'milvus')
MILVUS_PORT = os.environ.get('MILVUS_PORT', '19530')
# VLLM_HOST   = os.environ.get('VLLM_HOST', '172.17.0.1:8000')
# SYSTEM_PROMPT = os.environ.get('SYSTEM_PROMPT', 'คุณคือ OpenThaiGPT พัฒนาโดยสมาคมผู้ประกอบการปัญญาประดิษฐ์ประเทศไทย (AIEAT)')


# LLM_API_DOMAIN = os.environ.get('LLM_API_DOMAIN')
# LLM_API_KEY    = os.environ.get('LLM_API_KEY')
# LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME')

# connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

def get_model_env():
    """
    Fetch 'server' and 'local' configs from the settings collection.
    Returns the enabled config's apikey, domainname, and modelname.
    """
    setting = mongo.setting.find_one({}, {"_id": 0, "server": 1, "local": 1})
    if setting:
        if setting.get("server", {}).get("enabled", False):
            config = setting["server"]
        elif setting.get("local", {}).get("enabled", False):
            config = setting["local"]
        else:
            config = {}
        return {
            "isServer": config.get("enabled", False),
            "isLocal": not config.get("enabled", False),
            "apikey": config.get("apikey", ""),
            "domainname": config.get("domainname", ""),
            "modelname": config.get("modelname", "")
        }
    return {"apikey": "", "domainname": "", "modelname": ""}



# Example usage:
# env = get_model_env()
# print(env["domainname"], env["apikey"], env["modelname"])

# print(f"LLM_API_DOMAIN: {LLM_API_DOMAIN}")
# print(f"LLM_API_KEY: {LLM_API_KEY}")
# print(f"LLM_MODEL_NAME: {LLM_MODEL_NAME}")


# Function to initialize Milvus collection
def initialize_milvus_collection():
    # Check if collection exists
    if not utility.has_collection("document_embeddings"):
        # Create collection if it doesn't exist
        # You may need to adjust the schema based on your specific requirements

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),  # Adjust dim if needed
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields, "Document embeddings for Information database")
        collection = Collection("document_embeddings", schema)
        
        # Create an IVF_FLAT index for the embedding field
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index("embedding", index_params)
    else:
        collection = Collection("document_embeddings")
    
    return collection

connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
collection = initialize_milvus_collection()
logger.info("Successfully connected with MILVUS database.")

logger.info("Loading... BAAI/bge-m3 embedding model")
# Load BAAI/bge-m3 model and tokenizer
bge_model = AutoModel.from_pretrained("BAAI/bge-m3")
logger.info("Loading... BAAI/bge-m3 tokenizer model")
bge_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
logger.info("Successfully Load BAAI/bge-m3 embedding and tokenizer.")
logger.info("Now it is ready to serve.")

# Function to generate embeddings
def generate_embedding(text):
    inputs = bge_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = bge_model(**inputs).pooler_output
    return embeddings

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
    
    logger.debug(f"Query embedding shape: {query_embedding.shape}, Document embeddings shape: {document_embeddings.shape}")
    logger.debug(f"Query embedding: {query_embedding}, Document embeddings: {document_embeddings}")
    
    similarities = cosine_similarity(query_embedding, document_embeddings)
    ranked_documents = sorted(enumerate(similarities.flatten()), key=lambda x: x[1], reverse=True)
    return ranked_documents

SYSTEM_PROMPT = """
You are a **Customer Service AI assistant**.  
Your role is to answer questions politely and accurately, using only the provided context.  
You are an expert in customer service and must never invent information.  

## Context Sources
There are 5 possible context types:
1. **Time context** → Current date and time in Thailand timezone.  
2. **Document context** → Extracted from user documents.  
3. **CSV/PDF/TXT context** → Extracted from structured/unstructured files.  
4. **Database context** → Extracted from SQL databases.  
5. **Empty context** → When no relevant data is provided.  

The context will be passed inside XML tags:  

- `<time_context>...</time_context>`  
- `<document_context>...</document_context>`  
- `<csv_pdf_txt_context>...</csv_pdf_txt_context>`  
- `<database_context>...</database_context>`  

If no context is provided, the tags will contain `"Empty"`.  

### Rules for Answering
- **Always answer in the same language as the user’s question.**  
- **Only use the provided context.** Do not make up answers.  
- If the context is missing or irrelevant, reply with:  
  - `"I don't know"` (English)  
  - `"ไม่ทราบค่ะ/ครับ"` (Thai)  

### Example
```xml
<time_context>Empty</time_context>
<document_context>Empty</document_context>
<database_context>Empty</database_context>
<csv_pdf_txt_context>Empty</csv_pdf_txt_context>

## Extra Prompt Handling
The user may provide **extra instructions** after the main system prompt.  
If an extra prompt is given, you must **follow it strictly in addition to the main rules above**.  
When conflicts occur, prioritize the **main system rules** first, then apply extra instructions if they don’t break the rules.

the extra prompt will be tag in xml like this 
```xml
<extra_prompt>...</extra_prompt>

```

Remember this:
- Answer the question directly and concisely, without repeating the context or instructions.
"""

def compute_model(query, arr_history, system_prompt, temperature):
    prompt = [
        {'role':'system', 'content': SYSTEM_PROMPT},
        {'role':'user', 'content': f"""
<extra_prompt>{system_prompt if system_prompt else "Empty"}</extra_prompt>       
         """.strip()
         }
    ]
    
    try: 
        logger.info(f"Getting context from Milvus for query: {query}")
        assistant_message = None  # Initialize to avoid UnboundLocalError

        query_embedding = generate_embedding(query).numpy().flatten().tolist()
        
        # Prepare search parameters
        search_param = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }

        if not collection.is_empty:
        # Step 2: Retrieve top-10 documents from Milvus

            try:
                collection.load()
                search_results = collection.search(
                    data=[query_embedding],
                    anns_field="embedding",
                    param=search_param,
                    limit=10,
                    output_fields=["id", "text", "embedding"],
                    expr=None
                )
            except Exception as e:
                logger.error(f"Milvus search error: {e}")
                return {"content": "Milvus search error: " + str(e)}

        # Extract document texts and embeddings
        retrieved_documents = []
        document_embeddings = []
        for hits in search_results:
            for hit in hits:

                retrieved_documents.append(hit.entity)
                embedding = hit.entity.get('embedding')

                if embedding is not None:
                    document_embeddings.append(embedding)

        ranked_indices = rerank_documents(query_embedding, document_embeddings)
        top_documents = [retrieved_documents[i] for i, _ in ranked_indices[:3]]
        prompt = prompt.append({'role':'user', 'content': f"""
<document_context>{' '.join([doc.get('text') for doc in top_documents]) if top_documents else "Empty"}</document_context>
        """}.strip())
        logger.info(f"Top documents retrieved: {[doc.get('text') for doc in top_documents]}")
        if len(top_documents) == 0:
            return {"content": "No relevant documents found in the database."}
    except Exception as e:
        logger.error(f"Error during Milvus retrieval: {e}")
        prompt.append({
            'role':'user', 
            'content': f"<document_context>Empty</document_context>"
        })
        
    # get context from time 
    try:
        logger.info("Getting time context")
        time_context = get_time_context()
        prompt.append({
            'role':'user', 
            'content': f"""
<time_context>{time_context if time_context else "Empty"}</time_context>
""".strip()})
        logger.info(f"Time context: {time_context}")
    except Exception as e:
        logger.error(f"Error getting time context: {e}")
        prompt.append({
            'role':'user', 
            'content': f"<time_context>Empty</time_context>"
        })

    # get context from rag document
    try:
        logger.info("Getting RAG document context")
        rag_doc_context = rag_docs_query(query, top_k=3)
        prompt.append({
            'role':'user', 
            'content': f"""
<csv_pdf_txt_context>{' '.join(rag_doc_context) if rag_doc_context else "Empty"}</csv_pdf_txt_context>
""".strip()})
        logger.info(f"RAG document context: {rag_doc_context}")
    except Exception as e:
        logger.error(f"Error getting RAG document context: {e}")
        prompt.append({
            'role':'user', 
            'content': f"<csv_pdf_txt_context>Empty</csv_pdf_txt_context>"
        })

    # get context from rag sql database
    try:
        logger.info("Getting RAG SQL database context")
        rag_sql_context = rag_sql_query(query)
        prompt.append({
            'role':'user', 
            'content': f"""
<database_context>{rag_sql_context if rag_sql_context else "Empty"}</database_context>
""".strip()})
        logger.info(f"RAG SQL database context: {rag_sql_context}")
    except Exception as e:
        logger.error(f"Error getting RAG SQL database context: {e}")
        prompt.append({
            'role':'user', 
            'content': f"<database_context>Empty</database_context>"
        })    
    setting_info = get_model_env()

    temp = setting_info.get("temperature", 0.7)
    try:
        temp = float(temp)
    except (ValueError, TypeError):
        temp = 0.7
    if setting_info.get("isServer"):
        try:
            logger.info("Sending request to Together API")
            client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
            response = client.chat.completions.create(
                model=setting_info.get("modelname", "Qwen/Qwen2.5-72B-Instruct-Turbo"),
                messages=prompt,
                temperature=temp,
                max_tokens=2048,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during Together API call: {e}")
            return {"content": "Together API error: " + str(e)}
    elif setting_info.get("isLocal"):
        try:
            logger.info("Sending request Local LLM")
            client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
            response = client.chat.completions.create(
                model=setting_info.get("modelname", "Qwen/Qwen2.5-72B-Instruct-Turbo"),
                messages=prompt,
                temperature=temp,
                max_tokens=2048,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during Together API call: {e}")
            return {"content": "Together API error: " + str(e)}
    else:
        logger.error("No valid model configuration found.")
        return {"content": "No valid model configuration found."}
    

def get_function_by_name(name):
    print(f"Getting function by name: {name}")
    result = globals()[name]
    print(f"Function retrieved: {result}")
    return result

def convertTextFromRes(res):
    result = []
    lines = res.splitlines()
    for line in lines:
        if ':' in line:
            _, data = line.split(':', 1)  # Split on the first occurrence of ':'
            result.append(data.strip().replace('"', ''))
    return "".join(result)

