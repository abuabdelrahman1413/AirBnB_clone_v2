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
from sqlalchemy.orm import sessionmaker, scoped_session
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
        classes = ['State', 'City', 'User', 'Place', 'Review', 'Amenity']
        session = self.__session
        if cls is not None:
            query = session.query(cls)
            for obj in query:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        else:
            for cls_name in classes:
                query = session.query(eval(cls_name))
                for obj in query:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Adds an object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """
        Call remove() method on the private session attribute
        """
        self.__session.close()
