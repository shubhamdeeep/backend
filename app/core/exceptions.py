"""Custom exceptions and HTTP error handling."""
from fastapi import HTTPException


class DuplicateEmployeeError(HTTPException):
    """Raised when employee_id or email already exists."""

    def __init__(self, detail: str = "An employee with this ID or email already exists."):
        super().__init__(status_code=409, detail=detail)


class EmployeeNotFoundError(HTTPException):
    """Raised when employee is not found."""

    def __init__(self, detail: str = "Employee not found."):
        super().__init__(status_code=404, detail=detail)


class DuplicateAttendanceError(HTTPException):
    """Raised when attendance for same employee and date already exists."""

    def __init__(self, detail: str = "Attendance for this employee on this date already exists."):
        super().__init__(status_code=409, detail=detail)
