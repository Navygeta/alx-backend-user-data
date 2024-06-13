#!/usr/bin/env python3
"""
This module defines the `User` model for interacting with the `users` table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    Represents a record in the `users` table.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The user's email address.
        hashed_password (str): The user's hashed password.
        session_id (str): The session identifier for the user (optional).
        reset_token (str): The token used for resetting the password (optional)
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
