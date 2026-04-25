from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.academicSemester import AcademicSemesterCreate, AcademicSemesterUpdate
from Backend.crud.academicSemester import create_academic_semester, update_academic_semester, get_academic_semester, get_all_academic_semesters, get_current_semester, delete_academic_semester

router = APIRouter(
    prefix="/academic-semesters",
    tags=["academic-semesters"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_academic_semester_route(
    data: AcademicSemesterCreate,
    db: Session = Depends(get_db),
):
    return create_academic_semester(db=db, semester=data)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_academic_semesters_route(
    db: Session = Depends(get_db),
):
    return get_all_academic_semesters(db=db)


@router.get("/current", status_code=status.HTTP_200_OK)
def get_current_semester_route(
    db: Session = Depends(get_db),
):
    semester = get_current_semester(db=db)

    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No current semester found.",
        )

    return semester


@router.get("/{semester_name}", status_code=status.HTTP_200_OK)
def get_academic_semester_route(
    semester_name: str,
    db: Session = Depends(get_db),
):
    semester = get_academic_semester(db=db, semester_name=semester_name)

    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester '{semester_name}' not found.",
        )

    return semester


@router.patch("/{semester_name}", status_code=status.HTTP_200_OK)
def update_academic_semester_route(
    semester_name: str,
    data: AcademicSemesterUpdate,
    db: Session = Depends(get_db),
):
    semester = get_academic_semester(db=db, semester_name=semester_name)

    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester '{semester_name}' not found.",
        )

    return update_academic_semester(db=db, semester_name=semester_name, update=data)


@router.delete("/{semester_name}", status_code=status.HTTP_200_OK)
def delete_academic_semester_route(
    semester_name: str,
    db: Session = Depends(get_db),
):
    deleted = delete_academic_semester(db=db, semester_name=semester_name)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester '{semester_name}' not found.",
        )

    return deleted