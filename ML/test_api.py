import requests

# URL of our local API
URL = "http://127.0.0.1:8000/predict"

# Sample student data taken from the top of the dataset
sample_student = {
    "academic_year": "sophomore",
    "dept_name": "Mechanical Engineering",
    "current_gpa": 3.28,
    "passed_credits": 57,
    "registered_credits": 16,
    "gender": "M",
    "enroll_year": 2019,
    "course_credits": 3,
    "course_dept": "Mechanical Engineering",
    "semester_season": "Fall",
    "att_sessions": 8,
    "att_present_pct": 100.0,
    "att_late_pct": 0.0,
    "att_absent_pct": 0.0,
    "att_excused_pct": 0.0,
    "quiz1_score": 7.49,
    "quiz1_pct": 74.9,
    "quiz1_status": "graded",
    "quiz2_score": 7.08,
    "quiz2_pct": 70.8,
    "quiz2_status": "graded",
    "midterm_score": 13.06,
    "midterm_pct": 43.53,
    "midterm_status": "graded"
}

def test_api():
    print("Sending student data to the API...")
    try:
        response = requests.post(URL, json=sample_student)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ API Success!")
            print(f"Predicted Total Score: {result.get('predicted_total_score')} / 100")
        else:
            print("\n❌ API Error!")
            print(f"Status Code: {response.status_code}")
            print(f"Details: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Could not connect to the API. Make sure api.py is running!")

if __name__ == "__main__":
    test_api()
