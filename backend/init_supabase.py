"""
Initialize Supabase database with tables
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_tables, init_database
from loguru import logger


def main():
    """Initialize Supabase database"""
    try:
        logger.info("Initializing Supabase database...")

        # Create tables
        create_tables()
        logger.info("Database tables created successfully!")

        # Initialize with sample data
        init_database()
        logger.info("Database initialized with sample data!")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    main()
