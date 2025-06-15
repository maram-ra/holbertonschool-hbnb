#!/usr/bin/python3
"""Place model"""
from business.base_model import BaseModel


class Place(BaseModel):
    """Represents a place listing in HBnB"""

    def __init__(self, name, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id  # refers to a User
        self.amenities = []  # list of amenity IDs

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': self.amenities,
        })
        return data
