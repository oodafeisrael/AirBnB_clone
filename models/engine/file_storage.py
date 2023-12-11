#!/usr/bin/python3

import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """file storage class"""
    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User,
                  "Amenity": Amenity, "place": Place,
                  "City": City, "Review": Review, "State": State}

    def all(self):
        """returns the  dictionary __objects"""

        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with
        key <obj class name>.id

        """

        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file"""

        new_dict = {}
        for key, val in FileStorage.__objects.items():
            new_dict[key] = val.to_dict().copy()
        with open(self.__file_path, mode='w', encoding="UTF-8") as my_file:
            json.dump(obj_dict.my_file)

    def reload(self):
        """deserializes the JSON file"""

        try:
            with open(self.__file_path, mode='r', encoding="UTF-8") as my_file:
                new_dict = json.load(my_file)
            for key, val in new_dict.items():
                class_name = val.get('__class__')
                obj = eval(class_name)(**val)
                FileStorage.__objects[key] = obj
            except FileNotFoundError:
                pass
