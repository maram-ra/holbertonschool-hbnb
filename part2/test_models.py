from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user():
    user = User(first_name="Sara", last_name="Ali", email="sara@example.com")
    assert user.first_name == "Sara"
    assert user.is_admin == False
    print("✅ User test passed")

def test_place():
    user = User(first_name="Omar", last_name="Saleh", email="omar@example.com")
    place = Place(title="Sea View", price=200, latitude=24.7, longitude=46.6, owner=user)
    assert place.owner.email == "omar@example.com"
    print("✅ Place test passed")

def test_review():
    user = User(first_name="Layla", last_name="Nasser", email="layla@example.com")
    place = Place(title="Cabin", price=150, latitude=30, longitude=30, owner=user)
    review = Review(text="Perfect stay", rating=5, place=place, user=user)
    assert review.place.title == "Cabin"
    print("✅ Review test passed")

def test_amenity():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("✅ Amenity test passed")

if __name__ == "__main__":
    test_user()
    test_place()
    test_review()
    test_amenity()
