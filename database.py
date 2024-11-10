from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os

# Database setup with SQLAlchemy
DATABASE_URL = "sqlite:///offers.db"  # Change this to your database URL

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)