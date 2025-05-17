"""
dependencies.py

This module defines reusable FastAPI dependency functions for injecting
shared resources like the database connection into route handlers.

Functions:
    get_db(): Returns a reference to the application's MongoDB client
              instance from the app's central database module.

Usage:
    Used as a dependency in FastAPI endpoints to access the database.
"""

from app.database import db

def get_db():
    """
    Dependency function to provide access to the shared database instance.

    Returns:
        The application's MongoDB database client instance.
    """
    return db
