from sqlalchemy.orm import session
from Backend import models
from Backend.schemas import user
from sqlalchemy.orm import Session
from Backend.models import User
from Backend.schemas.user import UserCreate, UserAdminUpdate, UserSelfUpdate
from Backend.auth.dep import hash_password


def create_user(db: Session, user: UserCreate) :
    data = user.model_dump(exclude={"password"})
    db_user = User(**data, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) :
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_university_id(db: Session, university_id: str):
    return db.query(User).filter(User.university_id == university_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).order_by(User.id).offset(skip).limit(limit).all()


def update_user_self(db: Session, user: User, updates: UserSelfUpdate):
    data = updates.model_dump(exclude_unset=True, exclude={"confirm_password"})

    if "password" in data and data["password"]:
        data["hashed_password"] = hash_password(data.pop("password"))
    else:
        data.pop("password", None)

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def update_user_admin(db: Session, university_id: str, updates: UserAdminUpdate):
    user = get_user_by_university_id(db, university_id)
    if not user:
        return None

    data = updates.model_dump(exclude_unset=True)

    if "password" in data and data["password"]:
        data["hashed_password"] = hash_password(data.pop("password"))
    else:
        data.pop("password", None)

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, university_id: str):
    user = get_user_by_university_id(db, university_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user