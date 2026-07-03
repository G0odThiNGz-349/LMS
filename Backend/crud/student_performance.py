import joblib
import pandas as pd
from Backend.schemas.student_performance import StudentData

MODEL_PATH = "Backend/crud/best_student_model_regression.pkl"


try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

def predict_total_score(student_data: StudentData) -> float:
    """
    Predict total score from student data.
    Raises ValueError if model is not loaded or prediction fails.
    """
    if model is None:
        raise ValueError("Model is not loaded.")
    

    input_df = pd.DataFrame([student_data.model_dump()])
    
    try:
        pred = model.predict(input_df)
        clamped = max(0.0, min(100.0, float(pred[0])))
        return round(clamped, 2)
    except Exception as e:
        raise ValueError(f"Prediction failed: {e}")