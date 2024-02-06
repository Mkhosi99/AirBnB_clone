#!/usr/bin/python3
"""Module creates a class called Place and is defined"""
from models.base_model import BaseModel
class Place(BaseModel):
 """Class manages place objects
 Represents a place.
 Attributes:
 city_id (str): Indicates the City id.
 user_id (str): Indicates the User id.
 name (str): Indicates the name of the place.
 description (str): Indicates the description of the place.
 number_rooms (int): Indicates the number of rooms of the place.
 number_bathrooms (int): Indicates he number of bathrooms of the place.
 max_guest (int): Indicates the maximum number of guests of the place.
 price_by_night (int): Indicates the price by night of the place.
 latitude (float): Indicates the latitude of the place.
 longitude (float): Indicates the longitude of the place.
 amenity_ids (list): Indicates a list of Amenity ids.
 """
 city_id = ""
 user_id = ""
 name = ""
 description = ""
 number_rooms = 0
 number_bathrooms = 0
 max_guest = 0
 price_by_night = 0
 latitude = 0.0
 longitude = 0.0
 amenity_ids = []
