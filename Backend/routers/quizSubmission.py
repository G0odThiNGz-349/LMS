from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from Backend.database import get_db                    
from Backend.auth.dep import get_current_user      
from Backend.models import User
import Backend.crud.quizSubmission as quizSubmissionCrud
import Backend.schemas.quizSubmission as quizSubmissionSchema
 
router = APIRouter()


submission_router = APIRouter(prefix="/submissions", tags=["Quiz Submissions"])
 
 
@submission_router.get("/quiz/{quiz_id}", response_model=list[quizSubmissionSchema.QuizSubmissionOut])
def list_submissions_for_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return quizSubmissionCrud.get_submissions_for_quiz(db, quiz_id)
 
 
@submission_router.get("/{submission_id}", response_model=quizSubmissionSchema.QuizSubmissionOut)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    return quizSubmissionCrud.get_submission(db, submission_id)
 
 
@submission_router.post("/", response_model=quizSubmissionSchema.QuizSubmissionOut, status_code=status.HTTP_201_CREATED)
def create_submission(data: quizSubmissionSchema.QuizSubmissionCreate, db: Session = Depends(get_db)):
    return quizSubmissionCrud.create_submission(db, data)
 
 
@submission_router.patch("/{submission_id}", response_model=quizSubmissionSchema.QuizSubmissionOut)
def update_submission(
    submission_id: int,
    data: quizSubmissionCrud.QuizSubmissionUpdate,
    db: Session = Depends(get_db),
):
    return quizSubmissionCrud.update_submission(db, submission_id, data)
 
 
@submission_router.delete("/{submission_id}")
def delete_submission(submission_id: int, db: Session = Depends(get_db)):
    return quizSubmissionCrud.delete_submission(db, submission_id)
 

 
my_quiz_router = APIRouter(prefix="/me/quiz-submissions", tags=["My Quiz Submissions"])
 
 
@my_quiz_router.get("/", response_model=list[quizSubmissionSchema.QuizSubmissionOut])
def my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return quizSubmissionCrud.get_my_quiz_submissions(db, current_user_id=current_user.id)
 
 