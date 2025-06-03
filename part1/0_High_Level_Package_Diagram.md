```mermaid
classDiagram
    class PresentationLayer {
        <<Package>>
        +UserController
        +PlaceController
        +AmenityController
        +ReviewController
    }

    class BusinessLogicLayer {
        <<Package>>
        +UserModel
        +PlaceModel
        +AmenityModel
        +ReviewModel
    }

    class PersistenceLayer {
        <<Package>>
        +DatabaseAccess
        +Database
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
