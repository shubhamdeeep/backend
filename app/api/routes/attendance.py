"""Attendance HTTP API. Thin layer: parse request, call service, return response."""

from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_attendance_service
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceListResponse
from app.services import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    payload: AttendanceCreate,
    service: AttendanceService = Depends(get_attendance_service),
):
    """Mark attendance for an employee on a date."""
    record = await service.mark(payload)
    return record


@router.get("", response_model=AttendanceListResponse)
async def list_attendance(
    service: AttendanceService = Depends(get_attendance_service),
    employee_id: int | None = Query(None, description="Filter by employee ID"),
    from_date: date | None = Query(None, alias="from_date"),
    to_date: date | None = Query(None, alias="to_date"),
):
    """List attendance records, optionally filtered by employee and date range."""
    records = await service.list_filtered(
        employee_id=employee_id,
        from_date=from_date,
        to_date=to_date,
    )
    return AttendanceListResponse(
        records=[AttendanceResponse.model_validate(r) for r in records],
        total=len(records),
    )


@router.get("/by-employee/{employee_pk}", response_model=AttendanceListResponse)
async def list_attendance_by_employee(
    employee_pk: int,
    service: AttendanceService = Depends(get_attendance_service),
    from_date: date | None = Query(None, alias="from_date"),
    to_date: date | None = Query(None, alias="to_date"),
):
    """List attendance records for a specific employee."""
    records = await service.list_by_employee(
        employee_pk,
        from_date=from_date,
        to_date=to_date,
    )
    return AttendanceListResponse(
        records=[AttendanceResponse.model_validate(r) for r in records],
        total=len(records),
    )
