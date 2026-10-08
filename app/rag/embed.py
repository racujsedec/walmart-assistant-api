# GCP adapter boundary: configure Vertex AI text embeddings and project credentials.
# No invented local embedding model is presented as a live Vertex AI call.
def vertex_embedding_not_configured():raise RuntimeError('Vertex AI embeddings require a configured GCP project and index')
