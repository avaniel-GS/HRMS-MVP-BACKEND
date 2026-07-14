import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Prefer a single DATABASE_URL. Accept a full URL in DB_HOST as a fallback.
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL is not configured in environment variables")


def _get_connection():
    return psycopg2.connect(db_url)


def Connect():
    try:
        with _get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS employees(id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), role VARCHAR(100), department VARCHAR(100), date_of_joining DATE);"
                )
                connection.commit()
        return {"message": "Database initialized"}
    except Exception as e:
        return {"error": str(e)}


def Version():
    try:
        with _get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                pg_version = cursor.fetchone()
                if pg_version:
                    return {"version": pg_version[0]}
                return {"version": None}
    except Exception as e:
        return {"error": str(e)}


def Add_Employee(payload):
    try:
        with _get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO employees (name, email, role, department, date_of_joining) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (payload.name, payload.email, payload.role, payload.department, payload.date_of_joining),
                )
                employee_id = cursor.fetchone()[0]
                connection.commit()
                return {"message": "Employee added successfully", "employee_id": employee_id}
    except Exception as e:
        return {"error": str(e)}
