#!/usr/bin/python3
""" This module defines Class FileStorage which handles storage, serialization\
        and deserialization of instances to JSON file and vise versa """

from models.engine.errors import *
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
    models = ["Amenity", "BaseModel", "User", "Place",
              "State", "City", "Review"]

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

    def find_all(self, model=""):
        """ finds and returns all instances or instances of
        a particular model
        Args:
            model (str): model in which all instances are returned.
                    if empty, returns all registered instances(all models)
        """

        if model and model not in FileStorage.models:
            raise ModuleNotFoundError(model)

        lst = []
        for key, dic in FileStorage.__objects.items():
            if key.startswith(model):
                """<string.startswith("")> always returns True"""
                lst.append(str(dic))

        return lst

    def find_by_id(self, model, obj_id):
        """ finds an element of model by id and returns it
        Args:
            model: model to search through
            obj_id: instance id to search for
        """

        if model and model not in FileStorage.models:
            raise ModuleNotFoundError(model)

        _key = model + '.' + obj_id
        if _key not in FileStorage.__objects:
            raise InstanceNotFoundError(obj_id, model)

        return FileStorage.__objects[_key]

    def delete_by_id(self, model, obj_id):
        """ finds and delete the elements of a model by id
        Args:
            model: model to search through
            obj_id: instance id to delete
        """

        F = FileStorage  # ALIAS
        if model and model not in F.models:
            raise ModuleNotFoundError(model)

        _key = model + '.' + obj_id
        if _key not in F.__objects:
            raise InstanceNotFoundError(obj_id, model)

        del F.__objects[_key]
        self.save()

    def update_one(self, model, obj_id, field, value):
        """ Finds and updates an instance field with value
        Args:
            model: model to search through
            obj_id: instance id
            field: feild to be updated
            value: value to be added/inserted into field
        """

        F = FileStorage  # ALIAS
        if model and model not in F.models:
            raise ModuleNotFoundError(model)

        _key = model + '.' + obj_id
        if _key not in F.__objects:
            raise InstanceNotFoundError(obj_id, model)
        if field in ['id', 'created_at', 'updated_at']:
            return

        inst = F.__objects[_key]
        try:
            # check if attribute exists and type
            vtype = type(inst.__dict__[field])
            inst.__dict__[field] = vtype(value)
        except KeyError:
            # if attr doesnt exist insert into inst
            inst.__dict__[field] = value
        finally:
            inst.save()
