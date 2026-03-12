"""
Attendance business logic. Single responsibility: rules and orchestration for attendance.
Depends on AttendanceRepository and EmployeeRepository (Dependency Inversion).
"""

from datetime import date

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DuplicateAttendanceError, EmployeeNotFoundError
from app.models import Attendance
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.attendance import AttendanceCreate


class AttendanceService:
    """Service for attendance use cases. Reusable from API or other entrypoints."""

    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        employee_repository: EmployeeRepository,
    ):
        self._attendance_repo = attendance_repository
        self._employee_repo = employee_repository

    async def mark(self, payload: AttendanceCreate) -> Attendance:
        """Mark attendance. Validates employee exists and uniqueness (employee+date)."""
        employee = await self._employee_repo.get_by_pk(payload.employee_id)
        if not employee:
            raise EmployeeNotFoundError()

        record = Attendance(
            employee_id=payload.employee_id,
            date=payload.date,
            status=payload.status,
        )
        self._attendance_repo.add(record)
        try:
            await self._attendance_repo.session.flush()
        except IntegrityError:
            await self._attendance_repo.session.rollback()
            raise DuplicateAttendanceError()

        await self._attendance_repo.session.refresh(record)
        return record

    async def list_filtered(
        self,
        employee_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Attendance]:
        """List attendance with optional filters."""
        return await self._attendance_repo.list_filtered(
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
        )

    async def list_by_employee(
        self,
        employee_pk: int,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Attendance]:
        """List attendance for one employee. Raises EmployeeNotFoundError if employee missing."""
        employee = await self._employee_repo.get_by_pk(employee_pk)
        if not employee:
            raise EmployeeNotFoundError()

        return await self._attendance_repo.list_filtered(
            employee_id=employee_pk,
            from_date=from_date,
            to_date=to_date,
        )
