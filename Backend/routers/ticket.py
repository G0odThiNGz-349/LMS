from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.ticket import TicketCreate, TicketUpdate
from Backend.crud.ticket import create_ticket, update_ticket, get_tickets_by_user, get_tickets_by_current_user
from Backend.auth.dep import get_current_user
from Backend.models import User

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ticket_route(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return create_ticket(db=db, ticket=ticket, current_user=current_user)


@router.patch("/{ticket_id}", status_code=status.HTTP_200_OK)
def update_ticket_route(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
):
    updated = update_ticket(db=db, ticket_id=ticket_id, data=data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} not found.",
        )

    return updated


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_user_tickets_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_tickets_by_user(db=db, user_id=user_id)



@router.get("/me", status_code=status.HTTP_200_OK)
def get_current_user_tickets_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_tickets_by_current_user(
        db=db,
        current_user=current_user,
    )