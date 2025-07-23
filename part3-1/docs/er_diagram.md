```mermaid
erDiagram
    USER {
        string id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
        string created_at
        string updated_at
    }

    PLACE {
        string id
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id
        string created_at
        string updated_at
    }

    REVIEW {
        string id
        string text
        int rating
        string place_id
        string user_id
        string created_at
        string updated_at
    }

    AMENITY {
        string id
        string name
        string created_at
        string updated_at
    }

    PLACE_AMENITY {
        string place_id
        string amenity_id
    }

    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : has
    PLACE ||--o{ PLACE_AMENITY : includes
    AMENITY ||--o{ PLACE_AMENITY : available_in
```
