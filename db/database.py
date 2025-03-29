# db/database.py
import psycopg2
from config import DB_PARAMS

def get_db_connection():
    """Establish a connection to PostgreSQL."""
    return psycopg2.connect(**DB_PARAMS)
