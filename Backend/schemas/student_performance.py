from pydantic import BaseModel


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