# Natural Language to SQL Backend API

This document describes the backend API that converts natural language queries into SQL queries for a PostgreSQL database.

## Overview

The backend is built using FastAPI and integrates with OpenAI's GPT models and Pinecone for schema indexing. It provides an API endpoint to receive natural language queries, generate corresponding SQL queries, and execute them against a PostgreSQL database.

## Project Structure

```
nl2sql_backend/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration settings (DB, API keys)
│   ├── db/
│   │   ├── database.py     # PostgreSQL connection logic
│   │   ├── schema_index.py # Pinecone schema indexing & retrieval
│   ├── models/
│   │   ├── request_models.py # Pydantic request models
│   ├── services/
│   │   ├── llm_service.py    # OpenAI LLM query generation
│   │   ├── sql_executor.py   # Executes SQL queries on PostgreSQL
│   │   ├── schema_retriever.py # Retrieve relevant schema from pinecone
│   ├── routes/
│   │   ├── query_routes.py   # API endpoints
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
```

## Dependencies

-   `fastapi`: Web framework for building APIs.
-   `uvicorn`: ASGI server for running FastAPI applications.
-   `openai`: OpenAI Python library for interacting with GPT models.
-   `psycopg2`: PostgreSQL adapter for Python.
-   `pinecone-client`: Pinecone client library for vector database interaction.
-   `python-dotenv`: Load environment variables from a `.env` file.
-   `pydantic`: Data validation and settings management using Python type annotations.

## Configuration

Environment variables are used for configuration. Create a `.env` file in the project root with the following variables:

```
PINECONE_API_KEY=<your_pinecone_api_key>
OPENAI_API_KEY=<your_openai_api_key>
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
```

## Components

### `app/main.py`

-   Initializes the FastAPI application.
-   Includes the `query_routes` router.
-   Provides an entry point for running the application using Uvicorn.

### `app/config.py`

-   Loads environment variables using `python-dotenv`.
-   Defines configuration settings for Pinecone, OpenAI, and the PostgreSQL database.

### `app/db/database.py`

-   Provides a function `get_db_connection()` to establish a connection to the PostgreSQL database.

### `app/db/schema_index.py`

-   Initializes the Pinecone client.
-   Provides a function `index_schema()` to index the database schema in Pinecone.
    -   Retrieves table and column names from the PostgreSQL database.
    -   Stores schema information in Pinecone with table names as IDs and schema descriptions as metadata.

### `app/services/schema_retriever.py`

-   Provides a function `get_relevant_tables(nl_query: str)` to retrieve the most relevant database schema details for a given query from Pinecone.

### `app/services/llm_service.py`

-   Uses OpenAI's GPT models to convert natural language queries into SQL.
-   `generate_sql_query(nl_query: str)`:
    -   Retrieves relevant schema from Pinecone using `get_relevant_tables`.
    -   Constructs a prompt with the schema and the natural language query.
    -   Sends the prompt to the GPT model and returns the generated SQL query.

### `app/services/sql_executor.py`

-   Executes SQL queries on the PostgreSQL database.
-   `execute_sql(query: str)`:
    -   Establishes a database connection.
    -   Executes the SQL query.
    -   Returns the query result.
    -   Handles exceptions and returns an error message if the query fails.

### `app/routes/query_routes.py`

-   Defines the API endpoint for processing natural language queries.
-   `process_query(request: QueryRequest)`:
    -   Receives a `QueryRequest` object containing the natural language query.
    -   Generates the SQL query using `generate_sql_query`.
    -   Executes the SQL query using `execute_sql`.
    -   Returns the generated SQL query and the query result.
    -   Handles exceptions and returns an HTTP 500 error if an error occurs.

### `app/models/request_models.py`

-   Defines the Pydantic model `QueryRequest` for the request body.
-   `QueryRequest`:
    -   `natural_language_query`: The natural language query string.

## Setup and Usage

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment Variables:**

    -   Create a `.env` file in the project root with the required environment variables.

3.  **Index Database Schema:**

    -   Run the `index_schema()` function to index the database schema in Pinecone. This needs to be done once after setting up the database.

    ```bash
    python -m app.db.schema_index
    ```

4.  **Start the API Server:**

    ```bash
    uvicorn main:app --reload
    ```

5.  **Send Queries:**

    -   Send POST requests to `http://127.0.0.1:8000/query` with a JSON payload containing the natural language query:

    ```json
    {
      "natural_language_query": "Show all students enrolled in Mathematics"
    }
    ```

    -   The API will respond with a JSON object containing the generated SQL query and the query result:

    ```json
    {
      "sql_query": "SELECT * FROM students WHERE course = 'Mathematics';",
      "result": [["student1", "Mathematics"], ["student2", "Mathematics"]]
    }
    ```

## Notes

-   Ensure that the PostgreSQL database and Pinecone index are properly configured and accessible.
-   The GPT model used is `gpt-4`, which requires an OpenAI API key with access to GPT-4.
-   Error handling is implemented to catch exceptions and return appropriate error messages.
-   The `schema_index.py` needs to be run once to index the database schema.
-   The Pinecone environment is set to `us-west1-gcp` in this example. Modify it if needed.
