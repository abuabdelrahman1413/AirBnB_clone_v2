#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import declarative_base, relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """class Amenity"""

    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_aminities = relationship("Place", secondary=place_amenity,
                                   overlaps="amenities,place_amenities")
