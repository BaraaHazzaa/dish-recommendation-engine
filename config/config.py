# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    """Base configuration."""
    # Database URI for SQLite
    DATABASE_URI = os.getenv(
        'DATABASE_URI',
        #ENTER YOUR DATA BASE URL HERE
        r'THIS IS YOUR DATA BASE CONNECTION'
    )
    
    # Recommendation Weights
    ALPHA = float(os.getenv('ALPHA', 0.4))  # Weight for Collaborative Filtering
    BETA = float(os.getenv('BETA', 0.6))    # Weight for Content-Based Filtering
    
    # Number of Recommendations
    TOP_N = int(os.getenv('TOP_N', 10))
    
    # Other configurations can be added here
