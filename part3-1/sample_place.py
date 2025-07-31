# part3-1/seed_sample_place.py

from app.persistence.repository import db
from app.models.place import Place
from app.models.amenity import Amenity
from app import create_app

# Initialize app and context
app = create_app()
app.app_context().push()

# بيانات المالك والمزايا
owner_id = "77efcada-476b-4312-8af4-dcde4ec96fed"
wifi_id = "2150a8e8-9747-4150-a7f5-faf4274b8bd1"
parking_id = "8df9fc75-1fb4-4bb3-a705-5d2f59b29a76"

# جلب المزايا
wifi = Amenity.query.get(wifi_id)
parking = Amenity.query.get(parking_id)

# إنشاء المكان
place = Place(
    
    title="Beach House",
    description="Relaxing view by the sea",
    price=275,
    latitude=21.5,
    longitude=39.2,
    owner_id=owner_id
)

# ربط المزايا
place.amenities = [wifi, parking]

# إضافة للمخزن
db.session.add(place)
db.session.commit()

print("✅ Beach House added with amenities: wifi, parking")
