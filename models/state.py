#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

# cities = relationship("City", backref="state", cascade="all, delete"):
# This sets up a one-to-many relationship between State and City.
# The cities attribute will hold all City instances that reference
# this State instance.
# backref="state": This creates a bidirectional relationship. Each City will
# have a state attribute that references its parent State.
# cascade="all, delete": This specifies that all associated City
# objects should be deleted if the parent State is deleted.

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete")
