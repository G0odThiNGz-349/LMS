from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn

app = FastAPI(title="Student Performance API (Regression)", 
              description="API to predict a student's total score based on coursework.")

# Load the regression model
MODEL_PATH = "best_student_model_regression.pkl"
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Define the expected data format for a student
class StudentData(BaseModel):
    academic_year: str
    dept_name: str
    current_gpa: float
    passed_credits: int
    registered_credits: int
    gender: str
    enroll_year: int
    course_credits: int
    course_dept: str
    semester_season: str
    att_sessions: int
    att_present_pct: float
    att_late_pct: float
    att_absent_pct: float
    att_excused_pct: float
    quiz1_score: float = 0.0
    quiz1_pct: float = 0.0
    quiz1_status: str
    quiz2_score: float = 0.0
    quiz2_pct: float = 0.0
    quiz2_status: str
    midterm_score: float = 0.0
    midterm_pct: float = 0.0
    midterm_status: str

@app.post("/predict")
def predict_score(data: StudentData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    # Convert incoming data to a dictionary, then to a Pandas DataFrame
    # Note: using model_dump() for Pydantic V2
    input_data = pd.DataFrame([data.model_dump()])
    
    try:
        # Get the prediction
        prediction = model.predict(input_data)
        
        # Make sure the score makes sense (e.g., limit it between 0 and 100)
        predicted_score = max(0.0, min(100.0, float(prediction[0])))
        
        return {"predicted_total_score": round(predicted_score, 2)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Performance Prediction API! Use /docs to view the Swagger UI."}

if __name__ == "__main__":
    print("Starting API Server on http://127.0.0.1:8000")
    print("Interactive documentation available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
