import sys
import os

# أضف جذر المشروع إلى sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from app import create_app
from app.models import storage
from app.models.amenity import Amenity

# فعّل Flask app context
app = create_app()
with app.app_context():
    storage.reload()  # ✅ استدعِ reload هنا فقط

    def print_amenities():
        amenities = storage.all(Amenity)
        print("amenities = {")
        for amenity in amenities.values():
            print(f'    "{amenity.name}": "{amenity.id}",')
        print("}")

    if __name__ == "__main__":
        print_amenities()
