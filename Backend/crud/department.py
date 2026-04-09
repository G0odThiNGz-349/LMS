from sqlalchemy.orm import Session, joinedload
from Backend.models import Department, User
from Backend.schemas.department import DepartmentCreate, DepartmentUpdate

def create_department(db: Session, department: DepartmentCreate) -> Department:
    user = None
    if department.head_prof_university_id and department.head_prof_university_id.upper() != "NONE":
        user = db.query(User).filter(
            User.university_id == department.head_prof_university_id
        ).first()

    db_department = Department(
        name=department.name,
        head_prof_user_id=user.id if user else None
    )

    db.add(db_department)
    db.commit()
    db.refresh(db_department)

    db_department = db.query(Department).options(
        joinedload(Department.head_professor)
    ).filter(Department.id == db_department.id).first()

    return db_department

def update_department(db: Session, department_name: str, updates: DepartmentUpdate):

    department = db.query(Department).filter(
        Department.name == department_name
    ).first()

    if not department:
        return None
    
    update_data = updates.model_dump(exclude_unset=True)

    if "head_prof_university_id" in update_data:
        university_id = update_data["head_prof_university_id"]

        if university_id is not None:
            user = db.query(User).filter(
                User.university_id == university_id
            ).first()

            if not user:
                return None

            department.head_prof_user_id = user.id
        else:
            department.head_prof_user_id = None

        del update_data["head_prof_university_id"]

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


def get_department(db: Session, department_name: str):
    return db.query(Department).options(
        joinedload(Department.head_professor)
    ).filter(
        Department.name == department_name
    ).first()


def delete_department(db: Session, name: str):
    department = db.query(Department).filter(
        Department.name == name
    ).first()

    if not department:
        return None

    db.delete(department)
    db.commit()

    return department 
