from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be ≤ 50 characters.")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be ≤ 50 characters.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        
    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
