 <img src="https://github.com/user-attachments/assets/5f8d33ce-fed8-438a-935c-a9916afef26e" width="150">
 
 <dive></dive>
 
 ## HBnB Evolution - Part 1: Technical Documentation
Welcome to Part 1 of the HBnB Evolution project — a simplified AirBnB-like application designed to teach and demonstrate architectural design, software modeling, and documentation principles.

This part of the project is focused entirely on technical documentation, which will serve as the blueprint for implementation in later phases.
This is a group project and it's part of the holbertonschool x Tuwaiq SWE Bootcamp 

### Overview
The HBnB Evolution application is structured around a layered architecture and includes functionality for user management, property (place) listings, reviews, and amenity tracking. This documentation effort includes:

UML diagrams (Package, Class, and Sequence)

Architectural and interaction descriptions

Design rationale for all components

### Directory Structure
```
 holbertonschool-hbnb/
└── part1/
    ├── diagrams/
    │   ├── 0_High_Level_Package_Diagram.md
    │   ├── 1_Diagram_for_Business_Logic_Layer.md
    │   └── 2_Diagrams_for_API_Calls.md
    │ 
    └── documentation/
        └── HBnB_Technical_Documentation.pdf
```
## ✅ Tasks Breakdown

<details>
<summary><strong>0. High-Level Package Diagram</strong></summary>

**📌 Objective:**  
Illustrate the three-layer architecture of the HBnB system using the **Facade Pattern** for inter-layer communication.

**🧱 Layers:**
- **Presentation Layer**: API & Services
- **Business Logic Layer**: Core Models (User, Place, Review, Amenity)
- **Persistence Layer**: Data storage/retrieval logic (e.g., repositories/DAOs)

**📎 Deliverables:**
- UML Package Diagram (Mermaid.js or draw.io)
- Explanatory notes on architecture and design patterns

</details>

---

<details>
<summary><strong>1. Detailed Class Diagram for Business Logic Layer</strong></summary>

**📌 Objective:**  
Design and document all entities in the business logic layer, showing attributes, methods, and relationships.

**📦 Entities Modeled:**
- `User`
- `Place`
- `Review`
- `Amenity`

**📎 Requirements:**
- Use UUIDs for unique identification
- Include `created_at` and `updated_at` timestamps
- Show associations (e.g., Place ↔ Amenities)

**📎 Deliverables:**
- UML Class Diagram
- Description of each class, relationships, and logic

</details>

---

<details>
<summary><strong>2. Sequence Diagrams for API Calls</strong></summary>

**📌 Objective:**  
Demonstrate the flow of data and logic for major API operations.

**📎 API Calls Modeled:**
1. User Registration  
2. Place Creation  
3. Review Submission  
4. Fetch List of Places

**📎 Deliverables:**
- 4 UML Sequence Diagrams
- Step-by-step explanation of each interaction

**🎯 Focus Areas:**
- Request flow from Presentation → Business Logic → Persistence
- Use of method calls, validations, and DB access

</details>

---

<details>
<summary><strong>3. Documentation Compilation</strong></summary>

**📌 Objective:**  
Assemble all diagrams and notes into a **comprehensive technical document** that defines the system architecture.

**📎 Includes:**
- Introduction and project overview
- High-Level Architecture section
- Detailed Class Design section
- API Interaction Flow section

**📝 Format:**  
`HBnB_Technical_Documentation.pdf`  
Stored in `/documentation/`

</details>


### Format:
HBnB_Technical_Documentation.pdf
Stored in /documentation/

###  Resources Used
UML Class Diagram Tutorial

Mermaid.js Documentation

UML Sequence Diagram Guide

Facade Pattern Reference

 ### Notes
All diagrams are written in UML using standardized notation.

Focus has been placed on clarity, modularity, and documentation quality.

This documentation will directly influence the implementation phase in Part 2 and 3.

### Repository Info
Repository: holbertonschool-hbnb

Directory for this part: /part1

Status: ✅ 100% Documentation Complete


##  <img src="https://img.icons8.com/ios/452/github.png" width="30"/> Authors: 
We Worked together to implement, test, and document each daigram together. Each member did contribute to it.

- Khulood AlOtaibi
- Maram Alsofyani
- Hessah Alotaysh
  
<br>

[![GitHub](https://img.shields.io/badge/GitHub-Khulood_AlOtaibi-lightpink)](https://github.com/KhuloodGhazi)
[![GitHub](https://img.shields.io/badge/GitHub-Maram_Alsofyani-lightpink)](https://github.com/maram-ra)
[![GitHub](https://img.shields.io/badge/GitHub-Hessah_Alotaysh-lightpink)](https://github.com/hessafa)


