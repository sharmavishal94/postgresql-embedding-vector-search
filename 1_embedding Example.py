import ollama

response = ollama.embed(
    model='jeffh/intfloat-multilingual-e5-large-instruct:f16',
    input='The sky is blue because of Rayleigh scattering',
)
# print(response.embeddings)
embedding_dimension = len(response.embeddings[0])

print(f"Embedding dimensions: {embedding_dimension}")
# print(response)