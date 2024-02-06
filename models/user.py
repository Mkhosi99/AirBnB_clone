#!/usr/bin/python3
"""Module creates a class called User and defines it"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class manages user objects
    Represents a User.
    Attributes:
        email (str): Indicates the email of the user.
        password (str): Indicates the password of the user.
        first_name (str): Indicates the first name of the user.
        last_name (str): Indicates the last name of the user.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
