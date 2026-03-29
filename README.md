University LMS with Integrated Ticketing & Analytics  (Work in progress)
Overview
This project is a Learning Management System (LMS) designed to address a real-world problem in universities:
unstructured and unreliable communication through informal platforms like WhatsApp.
We built a system that replaces fragmented communication with a structured ticketing workflow, while also supporting core academic operations and enabling data-driven insights.

Problem Statement
In many universities:
Students rely on messaging apps to contact professors and staff
Messages are often lost, ignored, or delayed
There is no tracking or accountability
No data exists to analyze communication efficiency

Solution
Our system introduces a centralized LMS platform with:
Structured Ticketing System (Core Feature)
Students submit requests as tickets
Tickets are assigned to responsible staff (professors, TAs, admin)
Status tracking:
Open → In Progress → Resolved → Closed
Full history and accountability
Optional categorization (academic, technical, administrative)
This ensures:
No lost messages
Clear responsibility
Transparent communication

System Features
Core LMS
User roles (Student, Professor, TA, Admin, IT Staff)
Course management
Course offerings per semester
Enrollment system
Attendance tracking
Resources (files, materials)

Ticketing System
Create, assign, and manage tickets
Status tracking
Role-based handling
comments & discussion per ticket(later feature)

Analytics & Data Layer
Dedicated analytics endpoints
Student performance logging
Attendance and GPA tracking
Data extraction APIs for analysis

Machine Learning 
Predict student performance (e.g., risk of failure)
Analyze patterns in attendance and engagement

Architecture Overview
The system is designed with scalability in mind:
Core LMS Service → handles academic operations
Ticketing Module → structured communication layer
Analytics API Layer → exposes data for analysis
ML Component → consumes analytics data
This separation allows:
Independent scaling of services
Integration with national-level systems
Secure data access via APIs instead of direct DB access

API Design
The system exposes APIs for:
Core Operations
Users, Courses, Enrollments
Attendance, Resources, Quizzes
Ticketing
Create ticket
Assign ticket
Update status
Analytics
Attendance rates
GPA statistics
Student performance logs

Tech Stack
Backend
Python
FastAPI
SQLAlchemy
MySQL 
Data & ML
Python (Pandas, Scikit-learn)
JSON-based logging

Security
Role-based access control
Restricted analytics endpoints (admins only)
Token-based authentication (JWT)

Scalability Vision
This system is designed to scale to national-level deployment:
Modular architecture
API-based data access
Potential for:
Microservices
Load balancing
Centralized analytics dashboards
Each university can operate independently while contributing to a centralized data system.

Project Goal
This project aims to demonstrate:
A real-world solution to communication inefficiencies in universities
A scalable system design
Integration of data engineering and analytics
A foundation for data-driven education systems

Future Improvements
Real-time chat (WebSockets)
Advanced ticket prioritization & SLA
Full analytics dashboards
AI-based recommendations
Mobile application
