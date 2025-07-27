from app.persistence.repository import db
from app.models.user import User
from app import create_app

app = create_app()

with app.app_context():
    users = User.query.all()
    if not users:
        print("🚫 No users found.")
    else:
        print("📋 Registered Users:\n")
        for u in users:
            print(f"- ID: {u.id}")
            print(f"  Name: {u.first_name} {u.last_name}")
            print(f"  Email: {u.email}")
            print(f"  Admin: {'Yes' if u.is_admin else 'No'}")
            print("-" * 30)

