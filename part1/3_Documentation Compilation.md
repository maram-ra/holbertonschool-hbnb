# HBnB Project - Technical Documentation

## 📌 Introduction

### 🎯 Purpose and Scope
This document aims to provide a a detailed technical guide for the **HBnB** project for the development team. It covers the overall system architecture, design, object modeling, and the flow of operations through the system layers using UML diagrams to ensuring a consistent and efficient development process.


### ⭐️ Project Overview
**HB** nB is a full-stack web application that replicates the core functionalities of a property rental platform similar to Airbnb. It allows users to create, view, and manage property listings, as well as interact with places, amenities, cities, and users.

The project is developed using a modular architecture with a strong focus on backend design, object-relational mapping, and RESTful API support. It is built as part of the Holberton School curriculum to demonstrate mastery in Python, web development, and system design.

### 📖 Document Structure
This document is structured as follows:

- **💠 High-Level Architecture**: Overview and package diagram.
- **💠 Business Logic Layer**: Class diagram and entity relationships.
- **💠 API Interaction Flow**: Sequence diagrams and data flow explanations.
- **💠 Explanatory Notes**: Design decisions and rationale.

---

## High-Level Architecture

### 🌟 Overview
HBnB follows a **layered architecture** to ensure **separation of concerns, maintainability, and scalability**. The system is divided into the following key layers:

- **✅ Presentation Layer**: Handles user interactions via a web interface. This includes all HTTP services and API endpoints.
- **✅ Business Logic Layer**: Contains core logic and models (e.g., User, Place, Review, Amenity). This layer processes requests, applies business rules, and coordinates data flow between the frontend and storage.
- **✅ Persistence Layer**: Manages data storage and retrieval.

### 📐 High-Level Package Diagram

![Blank diagram](https://github.com/user-attachments/assets/6f14c1cf-f23e-47d2-a0f7-4d36ec2bc681)


### 💁🏻‍♀️ Explanation

- **Presentation Layer**: Exposes a RESTful API and web interface. It handles incoming HTTP requests, routes them to the appropriate logic, and returns responses.
- **Business Logic Layer**: Contains the core classes and logic (e.g., User, Place, Review, Amenity) that enforce business rules, validate data, and orchestrate interactions between layers.
- **Data Access Layer**: Abstracts how data is stored and retrieved.



---


## Business Logic Layer

### 📐 Class Diagram

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
    +register
    +update_profile
    +delete_account
}

class Place {
    +UUID id
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +UUID owner_id
    +Datetime created_at
    +Datetime updated_at
    +create
    +update
    +delete
    +list_amenities
}

class Review {
    +UUID id
    +UUID user_id
    +UUID place_id
    +Int rating
    +String comment
    +Datetime created_at
    +Datetime updated_at
    +submit
    +update
    +delete
}

class Amenity {
    +UUID id
    +String name
    +String description
    +Datetime created_at
    +Datetime updated_at
    +create
    +update
    +delete
}

User --> "1..*" Place : owns
User --> "1..*" Review : writes
Place --> "1..*" Review : has
Place --> "*" Amenity : includes
```

### 🔑 Key Entities and Their Relationships
- **User**: Represents a person using the platform. Can be a regular user or an admin. Users can own places and leave reviews.
- **Place**: Represents a property listed by a user. Contains attributes like title, description, price, and location.
- **Review**: Stores feedback and ratings left by users on places. Each review is linked to a user and a place.
- **Amenity**: Represents features (e.g., store, pool) that can be associated with places.

### 📌 Design Considerations
- **Use of inheritance** Common attributes such as id, created_at, and updated_at are abstracted in a BaseModel.
- **Encapsulation** Data is accessed and modified through methods to maintain integrity and control.
- **Associations** **One-to-many between User and Place **One-to-many between Place and Review **Many-to-many between Place and Amenity

---

## API Calls

### 📝 Sequence Diagrams

#### 1️⃣ User Registration API

```mermaid
sequenceDiagram
  participant User as User
  participant API as API
  participant BusinessModel as Business Model
  participant UserModel as Database
  User ->> API: Register
  BusinessModel ->> UserModel: store Data
  API ->> BusinessModel: RegisterUser
  UserModel -->> BusinessModel: Confirm
  BusinessModel -->> API: Return sucess Green - Fail Red
  API -->> User: Welcome aboard / Error
```

#### 2️⃣ Place Creation API

```mermaid
sequenceDiagram
title Place Creation API
participant User
participant API
participant Business Model
participant Database

User->>API: POST /places
API->>Business Model: CreatePlace(data)
Business Model->>Database: Insert place
Database-->>Business Model: OK
Business Model-->>API: Return place info
API-->>User: Place created
```

#### 3️⃣ Review Submission API

```mermaid
sequenceDiagram
title Review Submission API
participant User
participant API
participant Business Model
participant Database

User->>API: POST /reviews
API->>Business Model: Validate review
Business Model->>Database: Insert review
Database-->>Business Model: OK
Business Model-->>API: Return review info
API-->>User: Review submitted
```

#### 4️⃣ Fetching List of Places

```mermaid
sequenceDiagram
title Fetching List of Places API
participant User
participant API
participant Business Model
participant Database

User->>API: GET /places?filter=city
API->>Business Model: get_places(criteria)
Business Model->>Database: SELECT * WHERE city = ?
Database-->>Business Model: List of places
Business Model-->>API: Return data
API-->>User: Show list of places
```

### 🔑 Key Design Decisions
- **Layered Architecture**: Promotes separation of concerns—presentation, logic, and data are isolated for better maintainability and testing..
- **Object-Oriented Design**: Core entities (User, Place, Review, Amenity) use inheritance and encapsulation via a shared BaseModel.
- **RESTful API**: Standardized endpoints for CRUD operations enable easy frontend-backend integration.
- **Storage Abstraction**: Dual persistence support (FileStorage and DBStorage) allows flexibility in storage backends.
- **Auditability**: Each model tracks created_at and updated_at to support history tracking and debugging.

### 📌 How Components Fit Together
- **Presentation Layer** Handles HTTP requests through Flask routes. It sends JSON payloads and receives responses rendered as HTML or JSON.
- **Business Logic Layer** Processes incoming data, validates it, and manages relationships between entities. Core models live here.
- **Persistence Layer** Abstracts the storage logic. Uses either a file-based or SQL-based backend to persist data transparently.


