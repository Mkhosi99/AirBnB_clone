#!/usr/bin/python3
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import os.path
import json


class FileStorage:
    """ Represents an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        key = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(key, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        ob_dict = FileStorage.__objects
        objDict = {obj: ob_dict[obj].to_dict() for obj in ob_dict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objDict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists"""
        try:
            with open(FileStorage.__file_path) as f:
                objDict = json.load(f)
                for ob in objDict.values():
                    className = ob["__class__"]
                    del ob["__class__"]
                    self.new(eval(className)(**ob))
        except FileNotFoundError:
            return
