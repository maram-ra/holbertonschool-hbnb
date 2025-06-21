from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

# In-memory repository to simulate data persistence
class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    # Add an object to the in-memory store
    def add(self, obj):
        self.storage[obj.id] = obj

    # Retrieve an object by its ID
    def get(self, obj_id):
        return self.storage.get(obj_id)

    # Retrieve an object by any attribute (e.g., email)
    def get_by_attribute(self, attr, value):
        for obj in self.storage.values():
            if getattr(obj, attr, None) == value:
                return obj
        return None

    # Update an object's attributes
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    # Return all stored objects
    def all(self):
        return list(self.storage.values())

# Helper function to serialize objects with datetime fields
def serialize(obj):
    data = obj.__dict__.copy()
    if 'created_at' in data:
        data['created_at'] = data['created_at'].isoformat()
    if 'updated_at' in data:
        data['updated_at'] = data['updated_at'].isoformat()
    return data

# Facade to simplify interaction between API and business logic
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    # Create a new user and return serialized data
    def create_user(self, data):
        user = User(**data)
        self.user_repo.add(user)
        return serialize(user)

    # Get a user by ID
    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        return serialize(user) if user else None

    # Get a user by email
    def get_user_by_email(self, email):
        user = self.user_repo.get_by_attribute('email', email)
        return serialize(user) if user else None

    # Update a user's data
    def update_user(self, user_id, data):
        user = self.user_repo.update(user_id, data)
        return serialize(user) if user else None

    # Get all users
    def get_all_users(self):
        return [serialize(user) for user in self.user_repo.all()]
        
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return serialize(amenity)

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return serialize(amenity) if amenity else None
    
    def get_all_amenities(self):
        return [serialize(a) for a in self.amenity_repo.all()]
    
    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.update(amenity_id, data)
        return serialize(amenity) if amenity else None

    def create_place(self, place_data):
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        if not all(k in place_data for k in required_fields):
            raise ValueError("Missing required place fields")
            
        place = Place(**place_data)
        self.place_repo.add(place)
        return serialize(place)
        
    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
            
        owner = self.user_repo.get(place.owner_id)
        amenities = [self.amenity_repo.get(aid) for aid in getattr(place, 'amenity_ids', [])]
        
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": serialize(owner) if owner else None,
            "amenities": [serialize(a) for a in amenities if a]
        }

def get_all_places(self):
    return [
        {
            "id": p.id,
            "title": p.title,
            "latitude": p.latitude,
            "longitude": p.longitude
        }
        for p in self.place_repo.all()
    ]

def update_place(self, place_id, place_data):
    place = self.place_repo.update(place_id, place_data)
    return serialize(place) if place else None

# Instantiate the facade
facade = HBnBFacade()



from app.models.review import Review
from app.services.repositories import user_repo, place_repo, review_repo

class HBnBFacade:

    def create_review(self, review_data):
        # Validate required fields
        for f in ("user_id", "place_id", "rating", "text"):
            if not review_data.get(f):
                raise ValueError(f"{f} is required")

        # Check if user exists
        user = user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("user_id not found")

        # Check if place exists
        place = place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("place_id not found")

        # Validate rating range
        r = review_data["rating"]
        if not isinstance(r, int) or r < 1 or r > 5:
            raise ValueError("rating must be 1–5")

        # Create and save review
        new = Review(
            id=generate_uuid(),
            user_id=review_data["user_id"],
            place_id=review_data["place_id"],
            rating=r,
            text=review_data["text"]
        )
        review_repo.save(new)
        return new

    def get_review(self, review_id):
        review = review_repo.get(review_id)
        if not review:
            return None
        return review

    def get_all_reviews(self):
        return review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = place_repo.get(place_id)
        if not place:
            return None
        return [r for r in review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = review_repo.get(review_id)
        if not review:
            return None
        # Allow changing text and rating only
        if "text" in review_data:
            review.text = review_data["text"]
        if "rating" in review_data:
            r = review_data["rating"]
            if not isinstance(r, int) or r < 1 or r > 5:
                raise ValueError("rating must be 1–5")
            review.rating = r
        review.updated_at = datetime.now()
        review_repo.save(review)
        return review

    def delete_review(self, review_id):
        review = review_repo.get(review_id)
        if not review:
            return False
        review_repo.delete(review_id)
        return True
