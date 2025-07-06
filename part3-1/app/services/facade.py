import re
from datetime import datetime
import uuid
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository


class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def get_by_attribute(self, attr, value):
        for obj in self.storage.values():
            if getattr(obj, attr, None) == value:
                return obj
        return None

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.updated_at = datetime.now()
        return obj

    def delete(self, obj_id):
        return self.storage.pop(obj_id, None)

    def get_all(self):
        return list(self.storage.values())

    def all(self):
        return self.get_all()


def serialize(obj):
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    return obj


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ----- USERS -----
    def create_user(self, data):
        if not data.get("first_name") or not data.get("last_name"):
            raise ValueError("First name and last name are required")

        email = data.get("email")
        password = data.get("password")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        if not password:
            raise ValueError("Password is required")

        existing_user = self.user_repo.get_by_attribute('email', email)
        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=email
        )
        user.hash_password(password)
        self.user_repo.add(user)
        return serialize(user)

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        return serialize(user) if user else None

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        allowed_fields = {"first_name", "last_name"}
        for key in data:
            if key not in allowed_fields:
                raise ValueError(f"Cannot update field: {key}")

        for key, value in data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now()
        self.user_repo.add(user)
        return serialize(user)

    def get_all_users(self):
        return [serialize(user) for user in self.user_repo.get_all()]

    # ----- AMENITIES -----
    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            raise ValueError("Amenity name is required")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return serialize(amenity)

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return serialize(amenity) if amenity else None

    def get_all_amenities(self):
        return [serialize(a) for a in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.update(amenity_id, amenity_data)
        return serialize(amenity) if amenity else None

    # ----- PLACES -----
    def create_place(self, place_data):
        required = ["title", "price", "latitude", "longitude", "owner_id"]
        for key in required:
            if key not in place_data:
                raise ValueError(f"{key} is required")

        if place_data["price"] <= 0:
            raise ValueError("Price must be greater than 0")

        lat = place_data["latitude"]
        lon = place_data["longitude"]
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError("Latitude must be between -90 and 90 and longitude between -180 and 180")

        place = Place(**place_data)
        place.amenity_ids = place_data.get("amenities", [])
        self.place_repo.add(place)
        return serialize(place)

    def get_place_by_id(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.owner_id)
        amenities = [self.amenity_repo.get(aid) for aid in getattr(place, 'amenity_ids', [])]

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "owner": serialize(owner) if owner else None,
            "amenities": [serialize(a) for a in amenities if a],
            "reviews": [serialize(r) for r in self.review_repo.get_all() if r.place_id == place.id]
        }

    def get_all_places(self):
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude
            }
            for p in self.place_repo.get_all()
        ]

    def update_place(self, place_id, place_data):
        place = self.place_repo.update(place_id, place_data)
        return serialize(place) if place else None

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ----- REVIEWS -----
    def create_review(self, review_data):
        for field in ("user_id", "place_id", "rating", "text"):
            if not review_data.get(field):
                raise ValueError(f"{field} is required")

        user = self.user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("user_id not found")

        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("place_id not found")

        rating = review_data["rating"]
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        review = Review(
            id=str(uuid.uuid4()),
            user_id=review_data["user_id"],
            place_id=review_data["place_id"],
            rating=rating,
            text=review_data["text"]
        )
        self.review_repo.add(review)
        return serialize(review)

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return serialize(review) if review else None

    def get_all_reviews(self):
        return [serialize(r) for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [serialize(r) for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("rating must be between 1 and 5")
            review.rating = rating

        review.updated_at = datetime.now()
        self.review_repo.add(review)
        return serialize(review)

    def get_user_review_for_place(self, user_id, place_id):
        for review in self.review_repo.get_all():
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True


# Create one facade instance to use across your app
facade = HBnBFacade()
