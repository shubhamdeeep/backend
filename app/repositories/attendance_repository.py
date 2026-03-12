"""Attendance data access. Single responsibility: persistence for Attendance entity."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Attendance
from app.repositories.base import BaseRepository


class AttendanceRepository(BaseRepository[Attendance]):
    """Repository for Attendance. All DB operations for attendance live here."""

    async def list_filtered(
        self,
        employee_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        order_desc: bool = True,
    ) -> list[Attendance]:
        """List attendance with optional filters."""
        q = select(Attendance)
        if employee_id is not None:
            q = q.where(Attendance.employee_id == employee_id)
        if from_date is not None:
            q = q.where(Attendance.date >= from_date)
        if to_date is not None:
            q = q.where(Attendance.date <= to_date)
        if order_desc:
            q = q.order_by(Attendance.date.desc(), Attendance.id.desc())
        else:
            q = q.order_by(Attendance.date.asc())

        result = await self._session.execute(q)
        return list(result.scalars().all())

    def add(self, record: Attendance) -> Attendance:
        """Attach attendance to session. Caller must flush/commit."""
        self._session.add(record)
        return record
