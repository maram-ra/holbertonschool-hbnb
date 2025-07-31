from app.persistence.repository import db
from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class DBStorage:
    def __init__(self):
        self.__session = db.session

    def reload(self):
        # لا حاجة لـ create_engine، db.create_all() كافية
        db.create_all()

    def all(self, cls=None):
        objects = {}
        if cls:
            results = self.__session.query(cls).all()
            for obj in results:
                key = f"{cls.__name__}.{obj.id}"
                objects[key] = obj
        return objects
