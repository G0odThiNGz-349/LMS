from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from Backend.database import get_db
from Backend.schemas.student import StudentCreate, StudentAdminUpdate, StudentDetailedResponse, StudentResponse, StudentListResponse
import Backend.crud.student as student_crud
from Backend.auth.dep import get_current_active_user, get_current_user
from typing import Annotated
from Backend.models import User


router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/me", response_model=StudentDetailedResponse)
def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = student_crud.get_current_student(db, current_user)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return student


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_crud.create_student(db, student)


@router.get("/", response_model=List[StudentListResponse])
def list_students(
    skip: int = Query(default=1, ge=1),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return student_crud.get_students(db, page=skip, page_size=limit)


@router.get("/search", response_model=List[StudentListResponse])
def search_students(
    university_id: str | None = Query(default=None),
    full_name: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if university_id:
        return student_crud.search_students_by_university_id(db, university_id)
    if full_name:
        return student_crud.search_students_by_full_name(db, full_name)
    raise HTTPException(
        status_code=400,
        detail="Provide at least one search parameter: 'university_id' or 'full_name'.",
    )


@router.get("/year/{academic_year}", response_model=List[StudentListResponse])
def get_students_by_year(academic_year: str, db: Session = Depends(get_db)):
    return student_crud.get_students_by_year(db, academic_year)


@router.get("/{university_id}", response_model=StudentDetailedResponse)
def get_student(university_id: str, db: Session = Depends(get_db)):
    student = student_crud.get_student(db, university_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.patch("/{university_id}", response_model=StudentResponse)
def update_student(
    university_id: str,
    updates: StudentAdminUpdate,
    db: Session = Depends(get_db),
):
    student = student_crud.update_student_by_university_id(db, university_id, updates)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.delete("/{university_id}", response_model=StudentResponse)
def delete_student(university_id: str, db: Session = Depends(get_db)):
    student = student_crud.delete_student_by_university_id(db, university_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student