from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
User=os.getenv("User")
Password=os.getenv("Password")
db =os.getenv("DB")
Host=os.getenv("Host")
Port=os.getenv("Port")

DATABASE_URL = f"mysql+pymysql://{User}:{Password}@{Host}:{Port}/{db}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

import myModels
Base.metadata.create_all(engine)