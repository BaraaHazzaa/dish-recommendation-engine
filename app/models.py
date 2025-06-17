# app/models.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging

logger = logging.getLogger(__name__)

# Define the absolute path to the SQLite database
DATABASE_PATH = r"C:\Users\user\Desktop\30-9\project-root 9-9 3\config\NEWDB.db"

# Verify if the database file exists
if not os.path.exists(DATABASE_PATH):
    logger.error(f"SQLite database file not found at path: {DATABASE_PATH}")
    raise FileNotFoundError(f"SQLite database file not found at path: {DATABASE_PATH}")

# SQLite connection string
DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

# Initialize the  engine
try:
    engine = create_engine(
        DATABASE_URI,
        connect_args={"check_same_thread": False},  # Necessary for SQLite in multi-threaded apps
        echo=False  # Set to True for verbose SQL output (useful for debugging)
    )
    logger.info("SQLite database engine initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing SQLite engine: {e}")
    raise e

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Other configurations
TOP_N = 10  # Number of top recommendations to fetch
