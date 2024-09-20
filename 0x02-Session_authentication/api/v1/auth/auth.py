#!/usr/bin/env python3
""" A Method that creates a class Auth."""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Class definition."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ method to require authentication
        Args:
            path - string
            excluded_paths: List of strings
        Returns:
            True if path requires authentication, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize path to ensure it ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check if normalized path is in excluded_paths
        for excluded_path in excluded_paths:

            # Handle wildcard '*' at the end of excluded_path
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if not excluded_path.endswith('/'):
                    excluded_path += '/'

                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to handle authorization header
        Args:
            request - None
        Return: string
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ A method that determines the current user
        Args:
            request - None
        Return: The user
        """
        return None

    def session_cookie(self, request=None):
        """ Method that returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
