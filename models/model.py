# models/request_models.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    natural_language_query: str
