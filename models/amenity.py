#!/usr/bin/python3
""" Module to create  Amenity class"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    name = ""

    def __init__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)
