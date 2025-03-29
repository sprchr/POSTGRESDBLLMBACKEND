from pinecone import Pinecone
import psycopg2
from config import PINECONE_API_KEY, DB_PARAMS,OPENAI_API_KEY

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("db-schema")

from openai import OpenAI



def get_embedding(text: str):
    """Generate a 1536-dimensional vector using OpenAI's embedding model"""
    client = OpenAI()
    response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
    )
    return response.data[0].embedding  # Returns a 1536-dimensional float vector

def index_schema():
    """Indexes database schema in Pinecone for retrieval."""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = [col[0] for col in cursor.fetchall()]
        schema_info = f"Table: {table_name}, Columns: {', '.join(columns)}"

        # Generate 1536-dimensional embedding
        embedding = get_embedding(schema_info)

        # Store schema info in Pinecone
        index.upsert(vectors=[{"id": table_name, "values": embedding, "metadata": {"schema": schema_info}}])

    cursor.close()
    conn.close()
    print("Schema indexed successfully!")

# Fix query function
def get_relevant_tables(nl_query: str):
    """Retrieve the most relevant database schema details for a given query."""
    embedding = get_embedding(nl_query)  # Generate a matching 1536D vector
    results = index.query(vector=embedding, top_k=3, include_metadata=True)
    return [match["metadata"]["schema"] for match in results["matches"]]


# Run this once after setting up the database
index_schema()
