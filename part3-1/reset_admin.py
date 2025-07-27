from app import create_app
from app.persistence.repository import db
from app.models.user import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    
    existing = User.query.filter_by(email="admin@hbnb.io").first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print(" Deleted existing admin user.")

    hashed_pw = bcrypt.generate_password_hash("admin1234").decode('utf-8')
    admin = User(
        first_name="Admin",
        last_name="User",
        email="admin@hbnb.io",
        password=hashed_pw,
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print(" Admin user created with password: admin1234")
