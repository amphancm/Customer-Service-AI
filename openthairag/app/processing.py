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
        # Check 'server' first, then 'local'
        if setting.get("server", {}).get("enabled", False):
            config = setting["server"]
        elif setting.get("local", {}).get("enabled", False):
            config = setting["local"]
        else:
            config = {}
        return {
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

def compute_model(query, arr_history, system_prompt, temperature):
    
    # --- Insert this after the environment variable assignments ---
    setting_info = get_model_env()
    LLM_API_DOMAIN = setting_info.get('domainname')
    LLM_API_KEY    = setting_info.get('apikey')
    LLM_MODEL_NAME = setting_info.get('modelname')
    # ollamaserver = os.environ.get('OLLAMA_HOST')
    
    print(LLM_API_DOMAIN)
    print(LLM_API_KEY)
    print(LLM_MODEL_NAME)
    # print(ollamaserver)

    
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

    # system_prompt = os.environ.get('SYSTEM_PROMPT', 'คุณคือ OpenThaiGPT พัฒนาโดยสมาคมผู้ประกอบการปัญญาประดิษฐ์ประเทศไทย (AIEAT)')
    prompt = f"จากเอกสารต่อไปนี้\n\n"
    prompt += "\n\n".join([doc.get('text') for doc in top_documents])

    prompt_chatml = []

    prompt_chatml.append({
        'role': 'system',
        'content': 'คุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์ โปรดเลือกใช้ function get_more_detail ก่อนการตัดสินใจในการตอบคำถาม และเชื่อในข้อมูลจาก เอกสารเหล่านี้เท่านั้น \n\n'+system_prompt+'\n\n'+prompt 
    })
    for dat in arr_history:
        prompt_chatml.append(dat)
    prompt_chatml.append({
        'role': 'user',
        'content': query
    })

    # client = OpenAI(
    #     base_url = 'http://localhost:11434/v1',
    #     api_key='ollama', # required, but unused
    # )
    
    client = OpenAI(
        base_url=f"{LLM_API_DOMAIN}",
        api_key=LLM_API_KEY,
    )

    while True:
        try:
            print("Creating ChatCompletion...")
            response = client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages=prompt_chatml,
                tools=get_tools(),
                temperature=float(temperature) if temperature != '' else 0.5,
            )
            assistant_message = response.choices[0].message
            print(f"Assistant message: {assistant_message}")
            prompt_chatml.append(assistant_message)

            tools_supported = get_tools() is not None and len(get_tools()) > 0
            tool_calls = getattr(assistant_message, "tool_calls", None)
            if tools_supported and tool_calls and isinstance(tool_calls, list) and len(tool_calls) > 0:
                print(f"Tool calls found: {tool_calls}")
                for tool_call in tool_calls:
                    call_id = getattr(tool_call, "id", None)
                    print(f"Processing tool call with id: {call_id}")
                    fn_call = getattr(tool_call, "function", None)
                    if fn_call:
                        print(f"Function call found: {fn_call}")
                        fn_name = getattr(fn_call, "name", None)
                        fn_args_str = getattr(fn_call, "arguments", "{}")
                        try:
                            fn_args = json.loads(fn_args_str)
                        except Exception as e:
                            print(f"Failed to parse function arguments: {e}")
                            fn_args = {}
                        print(f"Function call: {fn_name}, arguments: {fn_args}")

                        fn = get_function_by_name(fn_name)
                        fn_res = json.dumps(fn(**fn_args), ensure_ascii=False)
                        print(f"Function result: {fn_res}")

                        prompt_chatml.append({
                            "role": "tool",
                            "content": fn_res,
                            "tool_call_id": call_id,
                        })
                        print(f"Updated messages after tool call: {prompt_chatml}")
            else:
                if not tools_supported:
                    print("Tool calling not supported, processing as normal response.")
                    # เรียก LLM ใหม่โดยไม่ส่ง tools argument
                    response = client.chat.completions.create(
                        model=LLM_MODEL_NAME,
                        messages=prompt_chatml,
                        temperature=float(temperature) if temperature != '' else 0.5,
                    )
                    assistant_message = response.choices[0].message
                    print(f"Generated Text: {assistant_message.content}")
                    return assistant_message
                else:
                    print("No tool calls made, exiting loop")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            # If error message indicates tool calling is not supported, process as normal response
            if "does not support tools" in str(e):
                print("Model does not support tools. Processing as normal response.")
                # เรียก LLM ใหม่โดยไม่ส่ง tools argument
                response = client.chat.completions.create(
                    model=LLM_MODEL_NAME,
                    messages=prompt_chatml,
                    temperature=float(temperature) if temperature != '' else 0.5,
                )
                assistant_message = response.choices[0].message
                print(f"Generated Text: {assistant_message.content}")
                return assistant_message
            else:
                break

    try:
        if assistant_message and hasattr(assistant_message, "content"):
            print(f"Generated Text: {assistant_message.content}")
            return assistant_message
        else:
            print("No assistant message generated.")
            return {"content": "An error occurred and no response was generated."}
    except Exception as e:
        print(f"Final error: {e}")
        return {"content": "An error occurred and no response was generated."}

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

