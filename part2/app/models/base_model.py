import uuid
from datetime import datetime

class BaseModel:
    """Base model class to use for stamps and id."""

    def __init__(self):
        self.id = uuid.uuid4().hex
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
