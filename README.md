


# Customer Service AI 

This project is a **full-stack AI system** for customer service, powered by:
- **Vue 3 (Vite)** for the frontend (port **5173**).
- **Flask** backend with REST APIs (port **5500**).
- **Milvus** vector database for RAG.
- **MongoDB** for metadata storage.
- **MySQL** for structured data.
- Optional **Ollama** for local model serving.
- **Docker Compose** for container orchestration.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-org/llm_agent.git
cd llm_agent
````

### 2. Environment Variables

Create the following environment files in the project root:

* **.env**


⚠️ These files should be kept **private**. They include keys like:

```ini
SERVER_IP=localhost
TOGETHER_API_KEY=your_togetherai_key
DB_USER=root
DB_PASSWORD=password
DB_HOST=rdbms
DB_PORT=3306
DB_DATABASE=customer_service_db
MYSQL_ROOT_PASSWORD=password
```

---

### 3. Run with Docker

Build and start all services:

```bash
docker compose up -d
```

Check logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

## 📂 Services

| Service               | Port  | Description                               |
| --------------------- | ----- | ----------------------------------------- |
| **Frontend (Vue 3)**  | 5173  | User interface (Vite dev server)          |
| **Backend (Flask)**   | 5500  | REST API & AI logic                       |
| **MongoDB**           | 27017 | Stores user data, docs metadata, settings |
| **MySQL**             | 3306  | RDBMS for structured data                 |
| **Milvus**            | 19530 | Vector DB for embeddings/RAG              |
| **MinIO**             | 9000  | Object storage backend for Milvus         |
| **Etcd**              | 2379  | Metadata store for Milvus                 |
| **Ollama (optional)** | 11434 | Local LLM server                          |

---

## 🌐 Access

* **Frontend** → [http://localhost:5173](http://localhost:5173)
* **Backend API** → [http://localhost:5500](http://localhost:5500)
* Example API routes:

  * `POST /auth/login`
  * `GET /upload/documents` (list uploaded files)
  * `POST /upload/documents` (upload file)
  * `DELETE /upload/documents/<id>` (delete file)

---

## 🛠 Development

* **Frontend (Vue 3)**

  ```bash
  cd otg-docs-prompt
  npm install
  npm run dev
  ```

  Runs at [http://localhost:5173](http://localhost:5173).

* **Backend (Flask)**

  ```bash
  cd openthairag
  flask run --host=0.0.0.0 --port=5000
  ```

  Runs at [http://localhost:5500](http://localhost:5500).

---

## ⚠️ Notes

* Ensure `.env` files are set correctly before running.
* Default admin account is created automatically:

  * **username**: `admin`
  * **password**: `admin`
* Use **Postman** or frontend UI to test API endpoints.


---

## 🗄️ Database Setup (MySQL)

The MySQL service runs on **port 3306**. You can connect using **MySQL Workbench** (or any client) with the credentials from `.env`.

**Example `.env`:**

```ini
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=customer_service_db
MYSQL_ROOT_PASSWORD=password
```

### 1. Connect in MySQL Workbench

* **Hostname**: `localhost`
* **Port**: `3306`
* **Username**: `root`
* **Password**: from `.env` (`MYSQL_ROOT_PASSWORD`)
* **Default schema**: `customer_service_db`

### 2. Create schema table

Run the following SQL in Workbench:

```sql
USE customer_service_db;

CREATE TABLE `health_products` (
  `id` INT AUTO_INCREMENT,
  `Type` VARCHAR(255) COMMENT 'ประเภทสินค้า เช่น ยา หรืออาหารเสริม',
  `ProductName` VARCHAR(255) COMMENT 'ชื่อสินค้า',
  `Price` VARCHAR(255) COMMENT 'ราคาพร้อมหน่วย เช่น บาท/ปริมาณ',
  `Description` TEXT COMMENT 'รายละเอียดสินค้า',
  `HowtoUse` TEXT COMMENT 'วิธีใช้สินค้า',
  `Caution` TEXT COMMENT 'ข้อควรระวัง',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3. Verify

```sql
SHOW TABLES;
DESCRIBE health_products;
```

You should now see the **`health_products`** table ready for use.

---







