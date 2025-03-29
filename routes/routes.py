# routes/query_routes.py
from fastapi import APIRouter, HTTPException
from models.model import QueryRequest
from services.llm_generator import generate_sql_query
from services.sql_executor import execute_sql

router = APIRouter()

@router.post("/query")
def process_query(request: QueryRequest):
    try:
        sql_query = generate_sql_query(request.natural_language_query)
        result = execute_sql(sql_query)
        return {"sql_query": sql_query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
