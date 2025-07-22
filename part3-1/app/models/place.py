from app.persistence.repository import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity

# Association table for many-to-many relationship with amenities
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    #Foreign key to User
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    # One-to-Many: Place → Reviews
    reviews = db.relationship('Review', backref='place', lazy=True)

    #Many-to-Many: Place ↔ Amenity
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', lazy='subquery')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
