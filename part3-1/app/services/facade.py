print("📦 HBnBFacade module loaded!")
import re
from datetime import datetime
import uuid
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository
from app.persistence.repository import db



def serialize(obj):
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    return obj

class HBnBFacade:
    def __init__(self):
        from app.services.repositories.user_repository import UserRepository
        self.user_repo = UserRepository()

    def create_place(self, place_data):
        print("🚨 create_place() called")
        print("🧠 FACADE ID:", id(self))

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

        try:
            # نسخ البيانات وتحضيرها
            place_fields = place_data.copy()
            owner_id = place_fields.pop("owner_id")
            place_fields.pop("image_url", None)

            place = Place(**place_fields)
            place.owner_id = owner_id

            # معالجة قائمة الـ amenities
            raw_amenities = place_data.get("amenities", [])
            if not isinstance(raw_amenities, list):
                raw_amenities = []

            valid_amenities = []
            for aid in raw_amenities:
                amenity = Amenity.query.get(aid)
                print(f"🔍 Looking up amenity {aid} → {amenity}")
                if amenity:
                    valid_amenities.append(amenity)
                else:
                    print(f"[WARN] Amenity not found: {aid}")

            print("📦 About to assign amenities")
            print("🧪 valid_amenities:", valid_amenities)
            print("🧪 types:", [type(a) for a in valid_amenities])

            place.amenities = valid_amenities

            db.session.add(place)
            db.session.commit()

            return place.to_dict()

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create place: {str(e)}")
    def get_all_places(self):
        return [serialize(p) for p in Place.query.all()]
    

    def get_place_by_id(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            return None
        place_dict = place.to_dict()
        place_dict["reviews"] = [r.to_dict() for r in place.reviews]
        place_dict["amenities"] = [a.name for a in place.amenities]
        owner = User.query.get(place.owner_id)
        if owner:
            place_dict["host"] = f"{owner.first_name} {owner.last_name}"
        else:
            place_dict["host"] = "Unknown"
        return place_dict




    # ----- USERS -----
    def create_user(self, data):
        if not data.get("first_name") or not data.get("last_name"):
            raise ValueError("First name and last name are required")

        email = data.get("email")
        password = data.get("password")
        if not email or not re.match(r"[^@]+@[^@]+\\.[^@]+", email):
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

    # ----- AMENITIES (Using SQLAlchemy) -----
    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            raise ValueError("Amenity name is required")
        amenity = Amenity(**amenity_data)
        db.session.add(amenity)
        db.session.commit()
        return serialize(amenity)

    def get_amenity(self, amenity_id):
        amenity = Amenity.query.get(amenity_id)
        return serialize(amenity) if amenity else None

    def get_all_amenities(self):
        return [serialize(a) for a in Amenity.query.all()]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            amenity.name = amenity_data["name"]
            amenity.updated_at = datetime.utcnow()
            db.session.commit()
        return serialize(amenity)


# Create one facade instance to use across your app
facade = HBnBFacade()
