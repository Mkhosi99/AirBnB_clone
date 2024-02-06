#!/usr/bin/python3
"""Module creates a class called Amenity"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """This class manages amenity objects
    Represents an amenity.
    Attributes:
        name (str): Indicates the name of the amenity.
    """
    name = ""
