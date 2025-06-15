#!/usr/bin/python3
"""User model"""
from business.base_model import BaseModel


class User(BaseModel):
    """Represents a User"""

    def __init__(self, email="", password="", first_name="", last_name=""):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        """Return dictionary representation, excluding password"""
        data = super().to_dict()
        data.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        })
        return data

