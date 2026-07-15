from fastapi import FastAPI

from cors import add_cors_middleware
from models import EmployeeCreate
from Database import Database, Employees

app = FastAPI(title="HRMS MVP Backend")
add_cors_middleware(app)

db = Database()
employees = Employees(db)
connected = db.Connect()


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "HRMS MVP Backend is running"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/db_version")
async def db_version():
    return db.Version()


@app.post("/api/add_employee")
async def add_employee(payload: EmployeeCreate):
    return employees.Add_Employee(payload)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("App:app", host="127.0.0.1", port=8000, reload=True)
