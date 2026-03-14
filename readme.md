# PostgreSQL + Ollama Movie Embeddings

Status - In-Progress

This project fetches movie records from a PostgreSQL database, generates text embeddings for their titles and descriptions using a local LLM via Ollama, and saves the embeddings back into the database using the `pgvector` extension.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed and running:
1. **Docker:** To run the PostgreSQL database with the `pgvector` extension.
2. **Ollama:** To run the embedding model locally.
3. **Python 3.x:** To run the embedding pipeline script.

## 🚀 Setup Instructions

### 1. Database Setup (Docker & pgvector)
Ensure your PostgreSQL container (e.g., `postgres-pgvector`) is running. 

You must enable the `pgvector` extension and add the embedding column to your `movies` table. The model we are using outputs exactly **1024 dimensions**. Run the following SQL in your database:

```sql
-- Enable the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add the embedding column to the table
ALTER TABLE omdb.movies ADD COLUMN IF NOT EXISTS movie_embedding vector(1024);

Note - I am using movie data set from just-use-postgres-book - https://github.com/dmagda/just-use-postgres-book/blob/main/data/movie/omdb_movies_data.sql

2. Install Python Dependencies
Install the required Python packages for database connection and Ollama integration:

Bash
pip install psycopg2-binary ollama
3. Pull the Ollama Embedding Model
This project uses the intfloat-multilingual-e5-large-instruct model. You need to download it to your local Ollama instance before running the script:

Bash
ollama pull jeffh/intfloat-multilingual-e5-large-instruct:f16
⚙️ Configuration
Open databaseExample.py (or whatever you named your script) and update the DB_PARAMS dictionary with your actual PostgreSQL Docker credentials:

Python
DB_PARAMS = {
    "dbname": "postgres",           # Your database name
    "user": "postgres",             # Your database user
    "password": "YOUR_PASSWORD",    # Password set in your Docker run command
    "host": "localhost",
    "port": "5432"
}
▶️ Usage
Once everything is configured, run the script:

Bash
python3 databaseExample.py
What the script does:
Connects to your PostgreSQL database.

Fetches all rows from omdb.movies where movie_embedding IS NULL (so it only processes new or un-embedded movies).

Combines the name and description of each movie.

Sends the combined text to Ollama to generate a 1024-dimensional vector embedding.

Updates the database record with the new embedding array.