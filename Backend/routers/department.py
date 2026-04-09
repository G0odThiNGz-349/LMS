from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentDetailedResponse
import Backend.crud.department as crud

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/", response_model=DepartmentDetailedResponse, status_code=status.HTTP_201_CREATED)
def create_department_endpoint(data: DepartmentCreate, db: Session = Depends(get_db)):

    department = crud.create_department(db, data)

    return department


@router.put("/{department_name}", response_model=DepartmentDetailedResponse)
def update_department(department_name: str, data: DepartmentUpdate, db: Session = Depends(get_db)):
    department = crud.update_department(db, department_name, data)

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found or invalid head_prof_university_id"
        )

    return department


@router.get("/{department_name}", response_model=DepartmentDetailedResponse)
def get_department(department_name: str, db: Session = Depends(get_db)):
    department = crud.get_department(db, department_name)

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


@router.delete("/{department_name}", status_code=status.HTTP_200_OK)
def delete_department(
    department_name: str,
    db: Session = Depends(get_db)
):
    department = crud.delete_department(db, department_name)

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return {"message": "Department deleted successfully"}