"""Employee HTTP API. Thin layer: parse request, call service, return response."""

from fastapi import APIRouter, Depends, status

from app.dependencies import get_employee_service
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeListResponse
from app.services import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    """Add a new employee."""
    employee = await service.create(payload)
    return employee


@router.get("", response_model=EmployeeListResponse)
async def list_employees(
    service: EmployeeService = Depends(get_employee_service),
):
    """List all employees."""
    employees = await service.list_all()
    return EmployeeListResponse(
        employees=[EmployeeResponse.model_validate(e) for e in employees],
        total=len(employees),
    )


@router.get("/{employee_pk}", response_model=EmployeeResponse)
async def get_employee(
    employee_pk: int,
    service: EmployeeService = Depends(get_employee_service),
):
    """Get a single employee by primary key."""
    employee = await service.get_by_pk(employee_pk)
    return employee


@router.delete("/{employee_pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_pk: int,
    service: EmployeeService = Depends(get_employee_service),
):
    """Delete an employee. Attendance records are cascade-deleted."""
    await service.delete_by_pk(employee_pk)
