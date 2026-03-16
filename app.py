from mymodels import Base, Student, Course, Enrollment
from database import engine, SessionLocal
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

app= FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Student_create(BaseModel):
    full_name: str

@app.post("/students")
def create_student(student:Student_create , db: Session=Depends(get_db)):
    new_student= Student(full_name=student.full_name)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students")
def get_students(db: Session=Depends(get_db)):
    students = db.query(Student).all()
    return students
