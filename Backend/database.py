from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("CLOUD_DATABASE_URL")


engine = create_engine(db_url)

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

