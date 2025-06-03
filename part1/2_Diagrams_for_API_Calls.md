## 1. User Registration API

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
## 2. Place Creation API

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

## 3. Review Submission API

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

## 4. Fetching List of Places

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

## Place Creation 


## Review Submission

## Review Submission

## Fetching a List of Places
