"""
Dependency injection for FastAPI. Single place to wire repositories and services.
Open/Closed: add new repos/services here without changing route code.
"""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import EmployeeRepository, AttendanceRepository
from app.services import EmployeeService, AttendanceService


async def get_employee_repository(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[EmployeeRepository, None]:
    """Provide EmployeeRepository bound to current session."""
    yield EmployeeRepository(session)


async def get_attendance_repository(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[AttendanceRepository, None]:
    """Provide AttendanceRepository bound to current session."""
    yield AttendanceRepository(session)


async def get_employee_service(
    repo: EmployeeRepository = Depends(get_employee_repository),
) -> AsyncGenerator[EmployeeService, None]:
    """Provide EmployeeService with injected repository."""
    yield EmployeeService(repo)


async def get_attendance_service(
    attendance_repo: AttendanceRepository = Depends(get_attendance_repository),
    employee_repo: EmployeeRepository = Depends(get_employee_repository),
) -> AsyncGenerator[AttendanceService, None]:
    """Provide AttendanceService with injected repositories."""
    yield AttendanceService(attendance_repo, employee_repo)
