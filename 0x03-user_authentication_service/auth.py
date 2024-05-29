#!/usr/bin/env python3
"""Module with a python script"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import bcrypt


def _hash_password(password: str) -> str:
    """Function that encrypts the password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a string representation of the uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Method that inits the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Regesters a new user"""
        try:
            db = self._db
            user = db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            new_user = User()
            new_user.email = email
            new_user.hashed_password = _hash_password(password)
            db.add_user(new_user.email, new_user.hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the user"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
            hashed_password = user.hashed_password
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Gets user from session id"""
        db = self._db
        try:
            if session_id is None:
                return None
            user = db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroys the session"""
        db = self._db

        try:
            user = db.find_user_by(id=user_id)
            db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Resets the password"""
        db = self._db

        try:
            user = db.find_user_by(email=email)
            reset_token = _generate_uuid()
            db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password"""
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            db.update_user(
                    user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError
