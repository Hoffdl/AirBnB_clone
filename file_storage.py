#!/usr/bin/python3
"""
This File defines the storage system (File System)
For the project.
It uses json format to serialize or deserialize
an object"""

import json
from json.decoder import JSONDecodeError
from .errors import *
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.city import City

