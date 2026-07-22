from fastapi import FastAPI

from cors import add_cors_middleware
from models import EmployeeCreate
from Database import Database, Employees

app = FastAPI(title="HRMS MVP Backend", docs_url=False)
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


@app.get("/api/get_employees/limit={limit}/offset={offset}")
async def latest_employees(limit: int, offset: int):
    return employees.Get_Employees(limit , offset)

@app.get("/api/get_head_count")
async def get_head_count():
    return employees.get_head_count()

@app.get("/api/get_department_count")
async def get_department_count():
    return employees.get_department_count()

@app.post("/api/delete_employees/{id}")
def Delete(id: int):
    return employees.deleteEmployee(id)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("App:app", host="127.0.0.1", port=8000, reload=True)
