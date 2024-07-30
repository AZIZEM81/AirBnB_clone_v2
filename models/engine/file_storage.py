#!/usr/bin/python3
"""This module defines a class for managing file storage in a JSON format
for AirBnB clone project"""
import json


class FileStorage:
    """Class to handle the storage of models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all models in storage, filtered by class
        if provided"""
        if cls is None:
            return self.__objects
        filtered_objects = {}
        cls_name = cls.__name__
        for key, value in self.__objects.items():
            if key.split('.')[0] == cls_name:
                filtered_objects[key] = value
        return filtered_objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = obj.to_dict()['__class__'] + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """Serializes the storage dictionary to a JSON file"""
        with open(self.__file_path, 'w') as file:
            temp_storage = {
                key: value.to_dict() for key, value in self.__objects.items()
            }
            json.dump(temp_storage, file)

    def reload(self):
        """Deserializes the JSON file to the storage dictionary"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        class_map = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as file:
                loaded_data = json.load(file)
                for key, value in loaded_data.items():
                    class_name = value['__class__']
                    self.__objects[key] = class_map[class_name](**value)
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        """Deletes an object from the storage dictionary"""
        if obj is not None:
            key = obj.to_dict()['__class__'] + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Calls the reload method"""
        self.reload()
