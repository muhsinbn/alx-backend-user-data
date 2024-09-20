#!/usr/bin/env python3
""" class that inherits from SessionExpAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session database class
    """

    def create_session(self, user_id=None):
        """ Create and store a new UserSession instance """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save the session to the database
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return the user ID by querying UserSession in the database """
        if session_id is None:
            return None

        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return None

            user_session = user_sessions[0]
            if self.session_duration <= 0:
                return user_session.user_id

            created_at = user_session.created_at
            if created_at is None:
                return None

            expiration_time = created_at + timedelta(
                    seconds=self.session_duration)
            if datetime.now() > expiration_time:
                return None

            return user_session.user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """ Destroy the UserSession based on the session
        ID from the request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()  # Remove the session from the database
        return True
