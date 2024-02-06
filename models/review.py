#!/usr/bin/python3
"""Module creates a class called Review and Defines it"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class manages review objects
    Represents a review.
    Attributes:
        place_id (str): Indicates the Place id.
        user_id (str): Indicates the User id.
        text (str): Indicates the review in text.
    """
    place_id = ""
    user_id = ""
    text = ""
