#!/usr/bin/env python3
""" defines the class Auth """
from flask import request
from typing import List, TypeVar


class Auth:
    """ class that manages API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determines which routes require authentication
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                if excluded_path[:-1] in path:
                    return False

        if path not in excluded_paths:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """
        validate all requests to secure the API
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None (for now)
        """
        return None
