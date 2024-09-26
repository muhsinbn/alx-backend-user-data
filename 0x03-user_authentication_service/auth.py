#!/usr/bin/env python3
""" Module that definesa _hash_password method
"""
import bcrypt
import secrets
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ Method to return the hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """ Method that returns a string representation of new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Method that takes in str args and return User object
        """
        try:
            # Check if User with this email already exists
            old_user = self._db.find_user_by(email=email)

            if old_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Add the new User object to database
        new_user = self._db.add_user(
                email=email, hashed_password=hashed_password.decode('utf-8'))

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Method that locates if the email is valid and decode
        Return:
            True if it matches or False
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(
                'utf-8'), user.hashed_password.encode('utf-8'))
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Method that finds user to the email, generate a new UUID and store
        it in the database as the user's session_id
        """
        try:
            new_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        # Generate a new UUID for the session ID
        session_id = _generate_uuid()

        # Update the user's session_id in the database
        self._db.update_user(new_user.id, session_id=session_id)

        # Return the session ID
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Method that returns User or None from session_id
        """
        if session_id is None:
            return None

        try:
            new_user = self._db.find_user_by(session_id=session_id)
            return new_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Method that destroys a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Method that resets the user's token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User {email} does not exist")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Method that updates the password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                    user.id, hashed_password=hashed_password.decode(
                        'utf-8'), reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
