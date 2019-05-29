from sqlalchemy import create_engine
import os

def get_engine():
    host = os.getenv("MB_DB_HOST", default="localhost")
    port = os.getenv("MB_DB_PORT", default=5432)
    user = os.getenv("MB_DB_USER", default="metabase")
    password = os.getenv("MB_DB_PASS", default="metabase")
    dbname = os.getenv("MB_DB_DBNAME", default="metabase")

    return create_engine(f"postgresql://#{user}:#{password}@#{host}:#{port}/#{dbname}")

