#!/usr/bin/env python3
"""Module with a python script"""
from typing import List, TypeVar
from flask import request
import os


class Auth():
    """Class with authentication methods"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that returns false"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        if path[-1] != '/':
            path += '/'

        astericks = [stars[:-1]
                     for stars in excluded_paths if stars[-1] == '*']

        for stars in astericks:
            if path.startswith(stars):
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method that returns None"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that returns None"""
        return None

    def session_cookie(self, request=None):
        """Method that returns the cookie value"""
        if request is None:
            return None

        value = request.cookies.get(os.getenv("SESSION_NAME"))

        return value
