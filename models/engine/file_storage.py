#!/usr/bin/python3
""" This module defines Class FileStorage which handles storage, serialization\
        and deserialization of instances to JSON file and vise versa """

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os.path
import json


class FileStorage:
    """Class FileStorage for serialization and deserialization if JSON file
        Attr:
            __file_path: string - path to the JSON file
            __objects: dictionary - empty but will store all\
                    objects by <class name>.id
        methods:
            all(self): returns the dictionary __objects
            new(self, obj): sets in __objects the obj with\
                    key <obj class name>.id
            save(self): serializes __objects to the JSON file (__file_path)
            reload(self): deserializes the JSON file to __objects\
                    (only if the JSON file exists), otherwise does nothing
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id
        Args:
            obj:object to set into __object
        """

        if obj:
            key = type(obj).__name__ + '.' + obj.id
            FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """

        dic = {}
        for key, obj in FileStorage.__objects.items():
            dic[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as json_file:
            json.dump(dic, json_file)

    def reload(self):
        """ deserializes the JSON file to __objects if it exists"""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as js_f:
                for key, dic in json.loads(js_f.read()).items():
                    dic = eval(dic['__class__'])(**dic)
                    FileStorage.__objects[key] = dic
