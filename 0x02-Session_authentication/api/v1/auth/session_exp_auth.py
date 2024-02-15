#!/usr/bin/env python3
"""
defines a class SessionExpAuth
"""
from api.v1.auth.session_auth import SessionAuth
import os
import datetime


class SessionExpAuth(SessionAuth):
    """
    Expiration authentication system class
    """

    def __init__(self):
        """ initialization method """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create a session id and return the session id created
        """
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the user_id from session dictionary
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        if "created_at" not in session_dictionary:
            return None

        created_at = session_dictionary.get("created_at")
        session_time = datetime.timedelta(seconds=self.session_duration)

        if created_at + session_time < datetime.datetime.now():
            return None

        return session_dictionary.get("user_id")
