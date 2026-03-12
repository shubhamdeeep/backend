"""Employee request/response schemas."""
from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    """Payload for creating an employee."""

    employee_id: str = Field(..., min_length=1, max_length=50, description="Unique employee ID")
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=255)


class EmployeeResponse(BaseModel):
    """Employee in API responses."""

    id: int
    employee_id: str
    full_name: str
    email: str
    department: str

    model_config = {"from_attributes": True}


class EmployeeListResponse(BaseModel):
    """List of employees."""

    employees: list[EmployeeResponse]
    total: int
