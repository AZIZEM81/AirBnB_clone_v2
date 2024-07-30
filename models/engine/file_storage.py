#!/usr/bin/python3
"""FileStorage module for AirBnB clone

This module contains the FileStorage class that manages the storage
and retrieval of objects in a file-based storage system.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """FileStorage class to manage file-based storage for AirBnB clone

    Attributes:
        __file_path (str): path to the JSON file where objects are stored
        __objects (dict): dictionary of objects
    """
    
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects in storage

        If cls is specified, only objects of that class are returned.
        """
        if cls is None:
            return FileStorage.__objects
        cls_name = cls.__name__
        return {k: v for k, v in FileStorage.__objects.items() if k.startswith(cls_name)}

    def new(self, obj):
        """Adds a new object to the storage dictionary

        Args:
            obj (BaseModel): the object to add
        """
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """Saves the objects to a JSON file"""
        with open(FileStorage.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in FileStorage.__objects.items()}, f)

    def reload(self):
        """Loads objects from the JSON file into storage"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objs = json.load(f)
                for k, v in objs.items():
                    cls_name = v['__class__']
                    cls = eval(cls_name)
                    FileStorage.__objects[k] = cls(**v)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage if it exists

        Args:
            obj (BaseModel): the object to delete
        """
        if obj is not None:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()

    def close(self):
        """Call the reload method to ensure objects are reloaded"""
        self.reload()
