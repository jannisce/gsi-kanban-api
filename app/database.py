from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # Path to the SQLite database file

# Create the connection engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create the Base object to define the models
Base = declarative_base()

# Create the SessionLocal object to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
