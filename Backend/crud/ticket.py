from sqlalchemy.orm import Session, aliased
from Backend.models import Ticket, User
from Backend.schemas.ticket import TicketCreate, TicketUpdate

def create_ticket(db: Session, ticket: TicketCreate, created_by_user_id: int):
    ticket = Ticket(**ticket.model_dump(), created_by_user_id=created_by_user_id)

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def update_ticket(db: Session, ticket_id: int, data: TicketUpdate):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket



def get_tickets_by_user(db: Session, user_id: int):
    created_by = aliased(User)
    assigned_to = aliased(User)

    results = (
        db.query(
            Ticket,
            created_by.name.label("created_by_name"),
            created_by.university_id.label("created_by_university_id"),
            assigned_to.name.label("assigned_to_name"),
        )
        .join(created_by, Ticket.created_by_user_id == created_by.id)
        .outerjoin(assigned_to, Ticket.assigned_to_user_id == assigned_to.id)
        .filter(Ticket.created_by_user_id == user_id)
        .all()
    )

    return [
        {
            "id": t.Ticket.id,
            "title": t.Ticket.title,
            "description": t.Ticket.description,
            "created_by_user_university_id": t.created_by_university_id,
            "created_by_user_name": t.created_by_name,
            "assigned_to_user_name": t.assigned_to_name,
            "status": t.Ticket.status,
            "created_at": t.Ticket.created_at,
            "updated_at": t.Ticket.updated_at,
        }
        for t in results
    ]