import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Prefer a single DATABASE_URL. Accept a full URL in DB_HOST as a fallback.
db_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(db_url)

cursor = connection.cursor()
try:
    # Simple version check to verify the server and connection
    cursor.execute("SELECT version();")
    pg_version = cursor.fetchone()
    if pg_version:
        print("Postgres version:", pg_version[0])
        
except Exception as e:
    print("Error while connecting to PostgreSQL:", e)

finally:
    cursor.close()
    connection.close()