from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("CLOUD_DATABASE_URL")


from sqlalchemy import create_engine
from urllib.parse import quote_plus

engine = create_engine(
    db_url,
    fast_executemany=True,           
    echo=False,                      
    pool_pre_ping=True,              
    pool_recycle=1800,               
    pool_size=15,                    
    max_overflow=25,
    pool_timeout=60,                 
    connect_args={
        "timeout": 60,                    
        "connect_timeout": 60,
        "driver": "ODBC Driver 18 for SQL Server",
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Connected to Azure SQL")
except Exception as e:
    print(f"Connection failed: {e}")


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

