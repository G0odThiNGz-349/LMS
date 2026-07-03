from fastapi import APIRouter, HTTPException
from Backend.schemas.student_performance import StudentData
from Backend.crud.student_performance import predict_total_score

student_performance_router = APIRouter(prefix="/performance", tags=["performance"])

@student_performance_router.post("/predict")
def predict_score(data: StudentData):
    try:
        score = predict_total_score(data)
        return {"predicted_total_score": score}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@student_performance_router.get("/")
def read_root():
    return {"message": "Welcome to the Student Performance Prediction API! Use /docs to view the Swagger UI."}