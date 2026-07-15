import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL is not configured in environment variables")

    def _get_connection(self):
        return psycopg2.connect(self.db_url)

    def Connect(self):
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS employees(id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), role VARCHAR(100), department VARCHAR(100), date_of_joining DATE);"
                    )
                    connection.commit()
            return {"message": "Database initialized"}
        except Exception as e:
            return {"error": str(e)}

    def Version(self):
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    pg_version = cursor.fetchone()
                    if pg_version:
                        return {"version": pg_version[0]}
                    return {"version": None}
        except Exception as e:
            return {"error": str(e)}


class Employees:
    def __init__(self, database: Database):
        self.database = database

    def Add_Employee(self, payload):
        try:
            with self.database._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO employees (name, email, role, department, date_of_joining) VALUES (%s, %s, %s, %s, %s) RETURNING id, name, email, role, department, date_of_joining;",
                        (payload.name, payload.email, payload.role, payload.department, payload.date_of_joining),
                    )
                    saved_employee = cursor.fetchone()
                    connection.commit()
                    return {
                        "message": "Employee added successfully",
                        "employee": {
                            "id": saved_employee[0],
                            "name": saved_employee[1],
                            "email": saved_employee[2],
                            "role": saved_employee[3],
                            "department": saved_employee[4],
                            "date_of_joining": saved_employee[5],
                        },
                    }
        except Exception as e:
            return {"error": str(e)}
    
    def Get_Latest_Employees(self, limit=4):
        try:
            with self.database._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, name, email, role, department, date_of_joining FROM employees ORDER BY id DESC LIMIT %s;",
                        (limit,),
                    )
                    employees = cursor.fetchall()
                    return [
                        {
                            "id": emp[0],
                            "name": emp[1],
                            "email": emp[2],
                            "role": emp[3],
                            "department": emp[4],
                            "date_of_joining": emp[5],
                        }
                        for emp in employees
                    ]
        except Exception as e:
            return {"error": str(e)}

    def Get_Employees(self):
        try:
            with self.database._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, name, email, role, department, date_of_joining FROM employees;")
                    employees = cursor.fetchall()
                    return [
                        {
                            "id": emp[0],
                            "name": emp[1],
                            "email": emp[2],
                            "role": emp[3],
                            "department": emp[4],
                            "date_of_joining": emp[5],
                        }
                        for emp in employees
                    ]
        except Exception as e:
            return {"error": str(e)}