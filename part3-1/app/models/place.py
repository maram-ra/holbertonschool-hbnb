from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Title is required and must be ≤ 100 characters.")
        if price < 0:
            raise ValueError("Price must be positive.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance.")
        self.owner_id = owner.id

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.reviews = []
        self.amenity_ids = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity_id):
        self.amenity_ids.append(amenity_id)
