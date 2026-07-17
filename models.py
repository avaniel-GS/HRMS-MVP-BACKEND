from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    role: str | None = None
    department: str
    email: EmailStr
    date_of_joining: str