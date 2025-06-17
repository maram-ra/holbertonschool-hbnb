from app.models.user import User

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

# Instantiate the facade
facade = HBnBFacade()
