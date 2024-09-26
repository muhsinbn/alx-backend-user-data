#!/usr/bin/env python3
""" Module that query the web server for the corresponding endpoint
"""
import requests


BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a new user with the given email and password.

    Args:
        email (str): The email of the user to register.
        password (str): The password of the user to register.

    Raises:
        AssertionError: If the response status code is not 200 or the
        response JSON is not as expected.
    """
    response = requests.post(
            f"{BASE_URL}/register", data={"email": email, "password": password}
            )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with the given email and an incorrect password.

    Args:
        email (str): The email of the user to log in.
        password (str): An incorrect password for the user.

    Raises:
        AssertionError: If the response status code is not 401.
    """
    response = requests.post(
            f"{BASE_URL}/sessions", data={"email": email, "password": password}
            )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in with the given email and password.

    Args:
        email (str): The email of the user to log in.
        password (str): The password of the user to log in.

    Returns:
        str: The session ID.

    Raises:
        AssertionError: If the response status code is not 200 or the
        session_id is not in the cookies.
    """
    response = requests.post(
            f"{BASE_URL}/sessions", data={"email": email, "password": password}
            )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in response.cookies
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """
    Attempts to access the profile without being logged in.

    Raises:
        AssertionError: If the response status code is not 403.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Accesses the profile while being logged in with a valid session ID.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the response status code is not 200 or the
        email is not in the response JSON.
    """
    response = requests.get(
            f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Logs out by destroying the session.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the response status code is not 200.
    """
    response = requests.delete(
            f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Requests a password reset token for the given email.

    Args:
        email (str): The email of the user requesting the password reset token.

    Returns:
        str: The reset token.

    Raises:
        AssertionError: If the response status code is not 200 or the
        reset_token is not in the response JSON.
    """
    response = requests.post(
            f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert "reset_token" in data
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the password for the user with the given email and reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token for the user.
        new_password (str): The new password for the user.

    Raises:
        AssertionError: If the response status code is not 200 or
        the response JSON is not as expected.
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    """
    Main script to run the test cases in sequence.
    """
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
