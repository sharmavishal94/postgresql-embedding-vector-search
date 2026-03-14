import psycopg2
import ollama

# Update these with your local Postgres credentials
DB_PARAMS = {
    "dbname": "postgres",           # <-- Check this too! Default is usually "postgres"
    "user": "postgres",             
    "password": "",  # <-- Put the password from Step 1 here
    "host": "localhost",
    "port": "5432"
}

# Using the model you tested earlier
EMBEDDING_MODEL = 'jeffh/intfloat-multilingual-e5-large-instruct:f16'

def main():
    # 1. Connect to PostgreSQL
    print("Connecting to database...")
    # Note: Even if you pip install psycopg2-binary, the import is just psycopg2
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    # 2. Fetch movies that don't have an embedding yet
    print("Fetching movies...")
    cursor.execute("""
        SELECT id, name, description 
        FROM omdb.movies
    """)
    movies = cursor.fetchall()
    
    print(f"Found {len(movies)} movies to process.")

    # 3. Iterate over each movie
    for row in movies:
        movie_id = row[0]
        name = row[1] if row[1] else ""
        description = row[2] if row[2] else ""
        
        # Combine name and description into one string
        combined_text = f"{name} {description}".strip()
        print(combined_text)
        
        if not combined_text:
            continue
            
        # 4. Generate embedding using Ollama's embed function
        response = ollama.embed(
            model=EMBEDDING_MODEL, 
            input=combined_text
        )
        
        # ollama.embed returns a list of lists, so we grab the first item [0]
        embedding = response.embeddings[0] 
        print(embedding)
        
        # 5. Update the database securely using %s
        cursor.execute("""
            UPDATE omdb.movies 
            SET movie_embedding = %s 
            WHERE id = %s
        """, (embedding, movie_id))
        
        print(f"Processed movie ID: {movie_id}")

    # 6. Commit the transaction and close connections
    conn.commit()
    cursor.close()
    conn.close()
    print("Successfully updated all movie embeddings!")

if __name__ == "__main__":
    main()