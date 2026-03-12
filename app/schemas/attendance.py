"""Attendance request/response schemas."""
from datetime import date

from pydantic import BaseModel, Field


class AttendanceCreate(BaseModel):
    """Payload for marking attendance."""

    employee_id: int = Field(..., description="Internal employee ID (from employees list)")
    date: date
    status: str = Field(..., pattern="^(Present|Absent)$", description="Present or Absent")


class AttendanceResponse(BaseModel):
    """Single attendance record in API responses."""

    id: int
    employee_id: int
    date: date
    status: str

    model_config = {"from_attributes": True}


class AttendanceListResponse(BaseModel):
    """List of attendance records."""

    records: list[AttendanceResponse]
    total: int
