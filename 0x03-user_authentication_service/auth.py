#!/usr/bin/env python3
"""
defines a _hash_password that takes in a password string
argument and returns bytes
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    returns a hashed password
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """
    returns a string representation of a new uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        """init method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a user
        Returns:
            User: the created user object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(user.email))
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        locates a user by email, and validate it
        if it exists, check the password with bcrypt.checkpw
        if it matches return True else return False
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            password_bytes = password.encode("utf-8")
            result = bcrypt.checkpw(password_bytes, hashed_password)
            return result
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        finds the user corresponding to the email and generate a new
        UUID and store it in the database as the user's session id
        Returns:
            str: the session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """gets the user from the session id"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """finds the user corresponding to the email
        if the user doesn't exist, raises ValueError
        if user exists, generate a UUID and update the user's reset_token
        database field.
        returns the token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """reset the password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
