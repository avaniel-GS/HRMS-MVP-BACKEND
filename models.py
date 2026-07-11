from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    role: str | None = None
    department: str
    email: str
    date_of_joining: str
