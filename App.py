from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    role: str | None = None
    department: str
    email: str
    date_of_joining: str


app = FastAPI(title="HRMS MVP Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "HRMS MVP Backend is running"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/add_employee")
async def add_employee(payload: EmployeeCreate):
    return {
        "message": "Employee added successfully",
        "employee": payload.model_dump(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("App:app", host="127.0.0.1", port=8000, reload=True)
