# services/llm_service.py
from openai import OpenAI
from config import OPENAI_API_KEY
from db.schema import get_relevant_tables

client = OpenAI()
def generate_sql_query(nl_query: str) -> str:
    """Use GPT to convert natural language query into SQL."""
    relevant_schema = "\n".join(get_relevant_tables(nl_query))

    prompt = f"""
You are an AI that converts natural language queries into SQL for a PostgreSQL database.
Return only the SQL query with no additional text, explanations, or formatting.

Here is the relevant database schema:
{relevant_schema}

Convert the following query: "{nl_query}"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
