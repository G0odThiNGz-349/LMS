from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.models import User
from Backend.schemas.user import UserCreate, UserAdminUpdate, UserSelfUpdate, UserResponse
from Backend.auth.dep import get_current_active_user
import Backend.crud.users as user_crud

router = APIRouter(prefix="/users", tags=["Users"])

CurrentUser = Annotated[User, Depends(get_current_active_user)]




@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    updates: UserSelfUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if updates.email and updates.email != current_user.email:
        if user_crud.get_user_by_email(db, updates.email):
            raise HTTPException(status_code=409, detail="Email already in use.")

    return user_crud.update_user_self(db, current_user, updates)




@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    _: CurrentUser,  
    db: Session = Depends(get_db),
):
    if user_crud.get_user_by_university_id(db, user.university_id):
        raise HTTPException(status_code=409, detail="University ID already registered.")
    if user.email and user_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already in use.")
    return user_crud.create_user(db, user)


@router.get("/", response_model=List[UserResponse])
def list_users(
    _: CurrentUser,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return user_crud.get_users(db, skip=skip, limit=limit)


@router.get("/{university_id}", response_model=UserResponse)
def get_user(
    university_id: str,
    _: CurrentUser,
    db: Session = Depends(get_db),
):
    user = user_crud.get_user_by_university_id(db, university_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.patch("/{university_id}", response_model=UserResponse)
def update_user(university_id: str, updates: UserAdminUpdate, _: CurrentUser, db: Session = Depends(get_db)):
    if updates.email:
        existing = user_crud.get_user_by_email(db, updates.email)
        if existing and existing.university_id != university_id:
            raise HTTPException(status_code=409, detail="Email already in use.")

    user = user_crud.update_user_admin(db, university_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.delete("/{university_id}", response_model=UserResponse)
def delete_user(
    university_id: str,
    _: CurrentUser,
    db: Session = Depends(get_db),
):
    user = user_crud.delete_user(db, university_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user