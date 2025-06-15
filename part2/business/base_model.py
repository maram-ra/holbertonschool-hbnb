#!/usr/bin/python3
"""Base model for all other models"""
import uuid
from datetime import datetime


class BaseModel:
    """Defines common attributes for all models"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_timestamp(self):
        """Update the updated_at attribute"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return dictionary representation of the object"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
