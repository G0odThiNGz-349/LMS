from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.combinedCreate import CreateUserStudent, CreateUserProfessor
from Backend.crud import combiend

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/students")
def create_student(student: CreateUserStudent, db: Session = Depends(get_db)):
    try:
        return combiend.create_user_student(db, student)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/professors")
def create_professor(professor: CreateUserProfessor, db: Session = Depends(get_db)):
    try:
        return combiend.create_user_professor(db, professor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))