#!/usr/bin/env python3
"""defines a class UserSession """
from models.base import Base


class UserSession(Base):
    """
    user session model that inherits from base
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ initialization method """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
