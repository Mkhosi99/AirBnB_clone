#!/usr/bin/python3
"""Module creates a class called City"""
from models.base_model import BaseModel


class City(BaseModel):
    """This class manages city objects and
    Represents a city.
    Attributes:
        state_id (str): Indicates the state id.
        name (str): Indicates the name of the city.
    """
    state_id = ""
    name = ""
