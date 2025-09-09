# rag_database/index.py
import os
import re
import mysql.connector
from together import Together


class RAGSQLQuery:
    def __init__(
        self,
        model_id: str = None,
        user: str = None,
        password: str = None,
        host: str = None,
        port: int | str = 3306,
        database: str | None = None,
        ssl_ca: str | None = None,
        together_api_key: str | None = None,
        connect_on_init: bool = True,
    ):
        """
        SQL generator + executor using TogetherAI and MySQL.

        Args:
            model_id: TogetherAI model ID. If None, read FROM env TOGETHER_MODEL_ID
                      or default to "Qwen/Qwen2.5-7B-Instruct-Turbo".
            user/password/host/port/database/ssl_ca: MySQL connection params.
            together_api_key: TogetherAI API key. If None, read from env TOGETHER_API_KEY.
            connect_on_init: Connect to DB immediately if params are provided.
        """
        # --- Safe defaults so __del__/close never crash ---
        self.conn = None
        self.cursor = None

        # --- Together client ---
        if together_api_key is None:
            together_api_key = os.getenv("TOGETHER_API_KEY")
        if not together_api_key:
            raise ValueError("TogetherAI API key is required (env TOGETHER_API_KEY).")

        self.client = Together(api_key=together_api_key)

        # Model: allow override via env
        self.model_id = (
            model_id
            or os.getenv("TOGETHER_MODEL_ID")
            or "Qwen/Qwen2.5-7B-Instruct-Turbo"
        )

        # --- DB params ---
        self.user = user
        self.password = password
        self.host = host
        self.port = int(port) if isinstance(port, str) else port
        self.database = database
        self.ssl_ca = ssl_ca

        # Optional auto-connect
        if connect_on_init and self.user and self.password and self.host and self.database:
            self._connect_db()

    # ---------------------- DB ----------------------
    def _connect_db(self):
        """Open MySQL connection."""
        kwargs = dict(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        if self.ssl_ca:
            kwargs["ssl_ca"] = self.ssl_ca

        self.conn = mysql.connector.connect(**kwargs)
        self.cursor = self.conn.cursor()
        print("Database connection established.")

    def ensure_connection(self):
        """Connect if not already connected (useful if connect_on_init=False)."""
        if not self.conn or not self.cursor:
            if not (self.user and self.password and self.host and self.database):
                raise ConnectionError("Missing DB params; cannot connect.")
            self._connect_db()

    # ---------------------- LLM -> SQL ----------------------
    def generate_sql_query(self, question: str, schema: str) -> str:
        """
        Ask the LLM to produce a single MySQL SELECT query. Robust parsing + 1 retry.
        """
        base_prompt = f"""You are a MySQL expert.
Return ONLY a single valid MySQL query. No explanations, no markdown, no code fences.
The query MUST start with SELECT and end with a semicolon.

Question: {question}

Schema:
{schema}
"""

        def call_llm(extra: str = "") -> str:
            resp = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": "Only output SQL. No prose. No code fences."},
                    {"role": "user", "content": base_prompt + ("\n" + extra if extra else "")},
                ],
                max_tokens=256,
                temperature=0,
            )
            return resp.choices[0].message.content.strip()

        # 1st attempt
        text = call_llm()
        sql = self._extract_sql(text)

        # Retry once with a stricter reminder if needed
        if not sql:
            text = call_llm("Reminder: Output ONLY one SQL statement that starts with SELECT and ends with ';'.")
            sql = self._extract_sql(text)

        if not sql:
            # Surface the raw model output to help you debug quickly
            raise ValueError(f"No SQL query found in the model output:\n{text}")

        sql = sql.strip()
        if not sql.endswith(";"):
            sql += ";"
        return sql

    @staticmethod
    def _extract_sql(text: str) -> str | None:
        """
        Try multiple patterns to pull SQL out of model text answer.
        Accepts: fenced blocks, 'SQL:' anchors, first SELECT...; etc.
        """
        # ```sql ... ```
        m = re.search(r"```sql\s*(SELECT[\s\S]+?)```", text, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        # ``` ... ```
        m = re.search(r"```\s*(SELECT[\s\S]+?)```", text, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        # SQL: <query>
        m = re.search(r"SQL\s*:?\s*(SELECT[\s\S]+)$", text, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        # First SELECT ... ; occurrence
        m = re.search(r"(SELECT[\s\S]+?;)", text, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        # Fallback: first line starting with SELECT
        for line in text.splitlines():
            if line.strip().upper().startswith("SELECT"):
                return line.strip()

        return None

    # ---------------------- Execute ----------------------
    def execute_query(self, sql_query: str):
        """Execute SQL and fetch all rows."""
        self.ensure_connection()
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def query(self, question: str, schema: str):
        """Generate SQL from LLM, print it, and execute."""
        sql = self.generate_sql_query(question, schema)
        print("Generated SQL:", sql)
        return self.execute_query(sql)

    # ---------------------- Cleanup ----------------------
    def close(self):
        try:
            if getattr(self, "cursor", None):
                self.cursor.close()
        finally:
            if getattr(self, "conn", None):
                self.conn.close()
                print("Database connection closed.")

    def __del__(self):
        # Be defensive; don't raise during GC
        try:
            self.close()
        except Exception:
            pass
