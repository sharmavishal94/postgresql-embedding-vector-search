


# import psycopg2
# import ollama

# # Update these with your local Postgres credentials
# DB_PARAMS = {
#     "dbname": "your_database_name", 
#     "user": "postgres",             
#     "password": "your_password",    
#     "host": "localhost",
#     "port": "5432"
# }

# # The model you downloaded via Ollama
# EMBEDDING_MODEL = 'nomic-embed-text'

# def main():
#     # 1. Connect to PostgreSQL
#     print("Connecting to database...")
#     conn = psycopg2.connect(**DB_PARAMS)
#     cursor = conn.cursor()

#     # 2. Fetch movies (Added a check so it only fetches rows that don't have an embedding yet)
#     print("Fetching movies...")
#     cursor.execute("""
#         SELECT id, name, description 
#         FROM omdb.movies 
#         WHERE movie_embedding IS NULL
#     """)
#     movies = cursor.fetchall()
    
#     print(f"Found {len(movies)} movies to process.")

#     # 3. Iterate over each movie
#     for row in movies:
#         movie_id = row[0]
#         name = row[1] if row[1] else ""
#         description = row[2] if row[2] else ""
        
#         # Combine name and description
#         combined_text = f"{name} {description}".strip()
        
#         if not combined_text:
#             continue
            
#         # 4. Generate embedding using Ollama
#         response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=combined_text)
#         embedding = response['embedding']
        
#         # 5. Update the database
#         # psycopg2 will automatically format the Python list into a Postgres array
#         cursor.execute("""
#             UPDATE omdb.movies 
#             SET movie_embedding = %s 
#             WHERE id = %s
#         """, (embedding, movie_id))
        
#         print(f"Processed movie ID: {movie_id}")

#     # 6. Commit the transaction and close connections
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("Successfully updated all movie embeddings!")

# if __name__ == "__main__":
#     main()


import ollama

response = ollama.embed(
    model='jeffh/intfloat-multilingual-e5-large-instruct:f16',
    input='The sky is blue because of Rayleigh scattering',
)
# print(response.embeddings)
embedding_dimension = len(response.embeddings[0])

print(f"Embedding dimensions: {embedding_dimension}")
# print(response)