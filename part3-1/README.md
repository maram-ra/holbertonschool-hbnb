# HBnB - Part 3: User Authentication & Database Integration

This phase focuses on making our app secure, reliable, and production-ready by adding user authentication, secure password handling, and connecting it to a real database.

---

## About this Project

We've been working together to build a robust backend for the HBnB app. In this part, we enhanced the backend by:

- Implementing **JWT authentication** so users can securely log in and access protected resources.
- Adding **bcrypt password hashing** to safely store user passwords.
- Switching from temporary in-memory storage to **persistent storage with SQLAlchemy**.
- Supporting different configurations for development and production environments.
- Securing API endpoints so only authenticated and authorized users can modify their own data.
- Documenting our database schema with clear diagrams using **mermaid.js**.

---

## Why This Matters

- Keeps user data safe and private.
- Ensures data persistence beyond app restarts.
- Sets the foundation for deploying a scalable, secure API.
- Encourages best practices in security and software architecture.

---

## Technologies & Concepts Used

- **Flask** – Web framework
- **Flask-Bcrypt** – Password hashing
- **Flask-JWT-Extended** – JWT token handling
- **SQLAlchemy** – Database ORM
- **SQLite** & **MySQL** – Development and production databases
- **mermaid.js** – Database schema visualization

---

## What We Built

| Step | Description | Purpose |
|---|---|---|
| 0 | Updated Flask Application Factory to accept configuration objects | Flexible environment configs |
| 1 | Enhanced User model with bcrypt password hashing | Secure password storage |
| 2 | Implemented JWT login and token management | Stateless authentication |
| 3 | Secured endpoints with JWT and ownership checks | Protect user data integrity |
| 4 | Role-based access control for admins | Manage app-wide resources |
| 5 | Replaced in-memory storage with SQLAlchemy ORM | Persistent and scalable data |
| 6 | Mapped all models and relationships to the database | Proper data structure |
| 7 | Created ER diagrams with mermaid.js | Visualized database design |

---

## Getting Started

1. Clone the repo and navigate to part3:


   ```bash
   git clone https://github.com/yourusername/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part3  ```
   
 2. Create and activate a virtual environment:


 ```bash
python3 -m venv venv
source venv/bin/activate
 ```


3. Install dependencies:

 ```bash
pip install -r requirements.txt
 ```
4. Configure environment variables or update config classes as needed.

5. Initialize the database (migrations or create tables):

 ```bash
flask db upgrade
 ```

6. Run the app:

 ```bash
flask run
 ```
 
7. Start testing user registration, login, and managing places and reviews through the API.

### Important Notes
- Passwords are hashed and never returned in API responses.

- JWT tokens must be included to access protected routes.

- Public endpoints remain accessible without authentication.

- Users can only edit or delete resources they own.

- Admins have special privileges to manage the entire app.

### Database Visualization
Check out the docs/ER_diagram.md file for our database schema rendered with mermaid.js, illustrating relationships between users, places, reviews, and amenities.

### About Us
This project was developed collaboratively by three team members, combining our skills in backend development, security, and database management to build a secure and scalable API.
