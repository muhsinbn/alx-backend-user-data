#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import logging

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # Set logging level to WARNING to suppress info logs
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Method that save the user to the database
        Args:
        email (str): The email of the user.
        hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find a user by arbitrary Keyword arguments
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound(f"No user found for {kwargs}")
        except InvalidRequestError:
            raise InvalidRequestError(f"Invalid query arguments: {kwargs}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Method that takes in a required user_id and arbitrary argument
        Return:
            None
        """
        user = self.find_user_by(id=user_id)
        allowed_attr = set(User.__table__.columns.keys())
        for key, value in kwargs.items():
            if key not in allowed_attr:
                raise ValueError(f"Invalid attribute '{key}' for user update")
            setattr(user, key, value)
        self._session.commit()
