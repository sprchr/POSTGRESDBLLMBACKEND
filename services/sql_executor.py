# services/sql_executor.py
from db.database import get_db_connection

def execute_sql(query: str):
    """Executes a SQL query and returns the result."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}
