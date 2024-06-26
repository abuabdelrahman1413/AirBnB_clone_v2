#!/usr/bin/python3
"""
This module defines a class DBStorage
"""


from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base


class DBStorage:
    """
    This class manages storage of hbnb models in a MySQL database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new DBStorage object
        """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.
            format(getenv('HBNB_MYSQL_USER'),
                   getenv('HBNB_MYSQL_PWD'),
                   getenv('HBNB_MYSQL_HOST'),
                   getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dict of objects
        """
        new_dict = {}
