#!/usr/bin/python3
""" City HBNB project """
from models.base_model import BaseModel


class City(BaseModel):
    """ The city class, contains state ID and nam """
    state_id = ""
    name = ""
