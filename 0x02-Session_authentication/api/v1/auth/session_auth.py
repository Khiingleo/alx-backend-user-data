#!/usr/bin/env python3
"""
defines a class SessionAuth
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ session authentication class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id """
        if user_id is None or type(user_id) is not str:
            return None

        id = str(uuid4())
        self.user_id_by_session_id[id] = user_id

        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User id based on a session ID """
        if session_id is None or type(session_id) is not str:
            return None
        value = self.user_id_by_session_id.get(session_id)
        return value

    def current_user(self, request=None):
        """
        (overload) that returns a User instance based on a cookie value
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        deletes the user session/logout
        """
        if request is None:
            return False

        cookie = self.session_cookie(request)

        if cookie is None:
            return False

        if self.user_id_for_session_id(cookie) is None:
            return False

        del self.user_id_by_session_id[cookie]

        return True
