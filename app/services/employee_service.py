"""
Employee business logic. Single responsibility: rules and orchestration for employees.
Depends on EmployeeRepository (Dependency Inversion); no direct DB access.
"""

from app.core.exceptions import DuplicateEmployeeError, EmployeeNotFoundError
from app.models import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate


class EmployeeService:
    """Service for employee use cases. Reusable from API, CLI, or other entrypoints."""

    def __init__(self, employee_repository: EmployeeRepository):
        self._repo = employee_repository

    async def create(self, payload: EmployeeCreate) -> Employee:
        """Create employee after validating uniqueness. Raises DuplicateEmployeeError if conflict."""
        employee_id = payload.employee_id.strip()
        email = payload.email.strip().lower()
        if await self._repo.exists_by_employee_id_or_email(employee_id, email):
            raise DuplicateEmployeeError(
                "An employee with this Employee ID or Email already exists."
            )

        employee = Employee(
            employee_id=employee_id,
            full_name=payload.full_name.strip(),
            email=email,
            department=payload.department.strip(),
        )
        self._repo.add(employee)
        await self._repo.session.flush()
        await self._repo.session.refresh(employee)
        return employee

    async def get_by_pk(self, pk: int) -> Employee:
        """Get employee by id. Raises EmployeeNotFoundError if not found."""
        employee = await self._repo.get_by_pk(pk)
        if not employee:
            raise EmployeeNotFoundError()
        return employee

    async def list_all(self) -> list[Employee]:
        """List all employees."""
        return await self._repo.list_all()

    async def delete_by_pk(self, pk: int) -> None:
        """Delete employee. Raises EmployeeNotFoundError if not found."""
        deleted = await self._repo.delete_by_pk(pk)
        if not deleted:
            raise EmployeeNotFoundError()
