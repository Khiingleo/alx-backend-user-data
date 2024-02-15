#!/usr/bin/env python3
"""
defines a class SessionAuth
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
