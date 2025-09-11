from .rag_database.index import RAGSQLQuery
from pathlib import Path
import tqdm
import os
from configs import get_config
from dotenv import load_dotenv

load_dotenv()

api_key = get_config().get("apikey", "")

SQL_FOLDER_DIR = Path(__file__).resolve().parent.parent / 'sql-files'

RAGSQL = RAGSQLQuery(
    user= os.getenv('DB_USER', "root"), 
    password= os.getenv('DB_PASSWORD', "password"), 
    host=os.getenv('DB_HOST', "rdbms"), 
    port=os.getenv('DB_PORT', 3306), 
    database=os.getenv('DB_DATABASE', "customer_service_db"),
    together_api_key=api_key
)

question = "ยาที่ใช้แก้ปวด"

def sql_files_to_string(folder_path):
    sql_statements = []
    for filename in tqdm.tqdm(os.listdir(folder_path)):
        if filename.endswith('.sql'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                sql_statements.append(f"{file.read()}\n")
    return "\n".join(sql_statements)



def rag_sql_query(question, sql_folder_dir=SQL_FOLDER_DIR):
    schemas = sql_files_to_string(sql_folder_dir)
    return RAGSQL.query(question, schemas)


# print(rag_sql_query("ยาที่ใช้แก้ปวด"))

