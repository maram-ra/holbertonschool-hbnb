# Business Logic Layer - Class Diagram

This diagram shows the structure of the core entities in the HBnB application:
- User
- Place
- Review
- Amenity

It illustrates their attributes, methods, and how they are related to each other in the business logic layer.

```mermaid
classDiagram
class User {
    +UUID id
    +String first_name
    +String last_name
    +String email
    +String password
    +Bool is_admin
    +Datetime created_at
    +Datetime updated_at
    +register()
    +update_profile()
    +delete_account()
}
...
