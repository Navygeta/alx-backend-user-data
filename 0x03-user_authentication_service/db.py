#!/usr/bin/env python3
"""
DB module for managing database interactions.
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    DB class for interacting with the database.

    Attributes:
        _engine (Engine): The SQLAlchemy engine.
        __session (Session): The SQLAlchemy session (memoized).
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance, setting up the database engine
        and creating all tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.

        Returns:
            Session: The SQLAlchemy session.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created user instance or None if the operation fails.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            print(f"Failed to add user: {e}")
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user based on a set of filters.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering users.

        Raises:
            InvalidRequestError: If any of the filters are invalid.
            NoResultFound: If no user matches the filters.

        Returns:
            User: The found user instance.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError(f"Invalid filter: {key}")
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound("No user found with the given filters.")
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user based on a given id.

        Args:
            user_id (int): The ID of the user to be updated.
            **kwargs: Arbitrary keyword arguments for updating user attributes.

        Raises:
            ValueError: If any of the update fields are invalid.

        Returns:
            None
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            raise NoResultFound(f"No user found with ID {user_id}.")
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[key] = value
            else:
                raise ValueError(f"Invalid update field: {key}")
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()
