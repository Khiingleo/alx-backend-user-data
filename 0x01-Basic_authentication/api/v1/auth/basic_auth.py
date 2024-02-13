#!/usr/bin/env python3
"""defines a class BasicAuth"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header forr
        a basic authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] == "Basic ":
            return authorization_header[6:]

        return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            result = b64decode(base64_authorization_header)
            return result.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        returns the user email and password from the
        base64 decoded value
        """
        decode = decoded_base64_authorization_header
        if decode is None:
            return (None, None)
        if type(decode) is not str:
            return (None, None)
        if ":" not in decode:
            return (None, None)

        result = decode.split(":", 1)
        return (result[0], result[1])

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads 'Auth' and retrieves the 'User' instance
        """
        basic_auth = self.authorization_header(request)
        base64_data = self.extract_base64_authorization_header(basic_auth)
        decode = self.decode_base64_authorization_header(base64_data)
        user_cred = self.extract_user_credentials(decode)
        user = self.user_object_from_credentials(user_cred[0], user_cred[1])

        return user
