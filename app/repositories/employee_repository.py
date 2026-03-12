"""Employee data access. Single responsibility: persistence for Employee entity."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Employee
from app.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    """Repository for Employee. All DB operations for employees live here."""

    async def get_by_pk(self, pk: int) -> Employee | None:
        """Get employee by primary key."""
        result = await self._session.execute(select(Employee).where(Employee.id == pk))
        return result.scalar_one_or_none()

    async def exists_by_employee_id_or_email(self, employee_id: str, email: str) -> bool:
        """Check if employee_id or email already exists (for duplicate validation)."""
        result = await self._session.execute(
            select(Employee.id).where(
                (Employee.employee_id == employee_id) | (Employee.email == email)
            )
        )
        return result.scalar_one_or_none() is not None

    async def list_all(self) -> list[Employee]:
        """List all employees ordered by id."""
        result = await self._session.execute(select(Employee).order_by(Employee.id))
        return list(result.scalars().all())

    def add(self, employee: Employee) -> Employee:
        """Attach employee to session. Caller must flush/commit."""
        self._session.add(employee)
        return employee

    async def delete_by_pk(self, pk: int) -> bool:
        """Delete employee by primary key. Returns True if deleted, False if not found."""
        employee = await self.get_by_pk(pk)
        if not employee:
            return False
        await self._session.delete(employee)
        await self._session.flush()
        return True
