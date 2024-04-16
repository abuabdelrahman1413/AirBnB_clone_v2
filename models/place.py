#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
import models
import os


place_amenity = Table('place_amenity',
                      Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", cascade='all, delete',
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
    else:
        @property
        def reviews(self):
            """The reviews property."""
            from models import storage
            reviewsList = []
            for key, value in storage.all().items():
                if (type(value).__name__ == 'Review'):
                    if ('place_id' in value.__dict__ and
                            str(value.__dict__['place_id']) == self.id):
                        reviewsList.append(value)
            return reviewsList

        @property
        def amenities(self):
            from models import storage
            amenitiesList = []
            for key, value in storage.all().items():
                if (type(value).__name__ == 'Amenity'):
                    if (value.__dict__['id'] in self.amenity_ids):
                        amenitiesList.append(value)
            return amenitiesList

        @amenities.setter
        def amenities(self, obj=None):
            if obj is not None:
                if type(obj) is Amenity and obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
