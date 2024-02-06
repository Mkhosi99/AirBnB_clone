#!/usr/bin/python3
"""Defining the BaseModel class that will serve as the parent module
   for the other subclasses
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Defines all common attributes/methods for the subclasses"""

    def __init__(self, *args, **kwargs):
        """The method is designed to initialize the instance of the class.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of the attributes.
        """
        timeform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(val, timeform)
                else:
                    self.__dict__[key] = val
        else:
            models.storage.new(self)

    def save(self):
        """Function updates updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns the dictionary of BaseModel instance.
        Also includes the key/value pair __class__ representing
        the class name of the object.
        """
        newDict = self.__dict__.copy()
        newDict["created_at"] = self.created_at.isoformat()
        newDict["updated_at"] = self.updated_at.isoformat()
        newDict["__class__"] = self.__class__.__name__
        return newDict

    def __str__(self):
        """Returns the string representation of BaseModel instance."""
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)
