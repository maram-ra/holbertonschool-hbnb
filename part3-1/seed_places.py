from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Place(Base):
    __tablename__ = 'places'
    id = Column(String(36), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///instance/hbnb.db')
Session = sessionmaker(bind=engine)
session = Session()

places = [
    Place(id="1", title="Beach House", description="Relaxing view by the sea", price=275.0, latitude=21.5, longitude=39.2, owner_id="user1"),
    Place(id="2", title="Cabin in Woods", description="Peaceful cabin in the forest", price=120.0, latitude=20.1, longitude=40.0, owner_id="user2"),
    Place(id="3", title="Modern Apartment", description="Comfortable apartment in city center", price=180.0, latitude=24.7, longitude=46.7, owner_id="user3"),
]

session.bulk_save_objects(places)
session.commit()

print(" Places added.")
