"""
Shared dependencies for FastAPI dependency injection.
This module centralizes common dependencies used across routes.
"""

from fastapi import Depends, HTTPException, status
from typing import Optional
from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory


def get_db():
    """
    Dependency that provides a database session.
    Yields a SQLAlchemy session that is automatically closed after use.
    
    Usage:
        async def my_route(session=Depends(get_db)):
            # session is available here
            pass
    """
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_repository(session=Depends(get_db)):
    """
    Dependency that provides a database repository.
    
    Usage:
        async def my_route(repo=Depends(get_repository)):
            # repo is available here
            pass
    """
    return PostgreSQLFactory.create_db_repository()


# Example: Common error handling
class APIException(HTTPException):
    """Base API exception class"""
    pass


def validate_positive_int(value: int) -> int:
    """Validate that an integer is positive"""
    if value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value must be positive"
        )
    return value


# Add more shared dependencies here as needed
# Examples:
# - get_current_user: Verify JWT token and return current user
# - get_service: Provide service instance
# - pagination: Handle pagination parameters
