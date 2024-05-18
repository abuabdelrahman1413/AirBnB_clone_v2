#!/usr/bin/python3
"""This module defines a class to Database storage operations for
the HBnB clone project.
"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
from models.base_model import Base
from hashlib import md5
import os


class DBStorage:
    """This class manages DB storage for the HBnB clone project.
    """
    __engine = None
    __session = None

    def __init__(self):
        """This method initializes an instance of the
        DBStorage class.
        """
        sqluser = os.getenv('HBNB_MYSQL_USER')
        sqlpass = os.getenv('HBNB_MYSQL_PWD')
        sqlhost = os.getenv('HBNB_MYSQL_HOST')
        sqldbname = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(sqluser, sqlpass,
                                             sqlhost, sqldbname),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """This method returns a dictionary of all instances
        of the class `cls` given as argument and returns
        all instances of all classes in db if given None.
        Args:
            cls(Class Obj): Class that the returned dictionary
                will contain instances of.
        """
        if cls is None:
            myObjects = []
            for mClass in [User, State, City, Amenity, Place, Review]:
                myObjects.extend(self.__session.query(mClass).all())
        else:
            myObjects = self.__session.query(cls).all()

        rDict = {"{}.{}".format(type(obj).__name__, obj.id):
                 obj for obj in myObjects}
        return rDict

    def new(self, obj):
        """Adds the object in the `obj` variable to the current
        database session.
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database & creates the current
        database session
        """
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current Session of SQLAlchemy
        """
        self.__session.close()
