#!/usr/bin/pyton3
""" Creates a unique insance of class FileStorage. This module\
        executes every time the model package is imported """

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
