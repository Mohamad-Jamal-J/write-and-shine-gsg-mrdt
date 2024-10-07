# Write & Shine (Python Django Application)

## Overview
Write & Shine is a web platform that allows users to publish and discover diverse content across various fields, including technology, science, and art. It fosters a community for professionals to share knowledge, insights, and stay updated on the latest trends.

## Table of Contents
- [Write \& Shine (Python Django Application)](#write--shine-python-django-application)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Project Focus](#project-focus)
  - [System Components](#system-components)
  - [System Architecture](#system-architecture)
  - [Developers Roles and Responsibilities](#developers-roles-and-responsibilities)
  - [UI Prototypes](#ui-prototypes)
  - [Design Patterns](#design-patterns)
    - [Factory Design Pattern (FDP)](#factory-design-pattern-fdp)
    - [Observer Design Pattern (ODP)](#observer-design-pattern-odp)
  - [Proposal Document](#proposal-document)


## Project Focus
The project aims to develop a robust and maintainable web platform, enabling users to seamlessly create, manage, and discover content. The focus is not only on providing a high-quality user experience but also on implementing best practices in software development, such as modular architecture, SOLID and DRY principles, and unit testing. These practices ensure that the platform is scalable, maintainable, and easy to extend, reflecting the core learning objectives of this training program.


## System Components

| Application            | Description                                         |
|------------------------|-----------------------------------------------------|
| **Accounts Application** | Registration and account management.                |
| **Profiles Application** | Profile management.                                 |
| **Posts Application**    | CRUD operations on posts.                           |
| **Interactions Application** | Managing likes, comments, and saving/sharing posts. |
| **Search Application**   | Searching posts and bloggers.                      |


## System Architecture
The system follows the Model Service View Template (MSVT) pattern, extending Django's MVT architecture with a Service Layer for clear separation of concerns between the Model and View.

![msvt](https://github.com/user-attachments/assets/8c5347a3-d6fe-44ba-82ee-c736deaa9e1a)
*Figure 1 - MSVT Architecture*


## Developers Roles and Responsibilities

| Role                  | Developer              | Responsibilities                        |
|-----------------------|------------------------|-----------------------------------------|
| **Team Lead - Back-End** | Mohammad Jaradat       | Overall project coordination, Back-End  |
| **Front-End Developer**  | Hala Barqawi           | Profile page, Create Posts              |
| **Front-End Developer**  | Mays Qasem             | Sign In/Up Page, Home Page              |
| **Back-End Developer**   | Sarah Abu Irmeileh     | Posts Management, Interactions Management                     |


## UI Prototypes
You can view the UI prototypes [here](https://docs.google.com/presentation/d/1ANHg3Tmhs2OJV8dCQWF-F4LsJmgqz7SHZsNBJQ0zGHM/edit?usp=sharing) or by clicking on the image below.

[![prototype_slide](https://github.com/user-attachments/assets/5f59808f-baf0-4df3-9876-69f6acde782f)](https://docs.google.com/presentation/d/1ANHg3Tmhs2OJV8dCQWF-F4LsJmgqz7SHZsNBJQ0zGHM/edit?usp=sharing)
*Figure 2 - UI Prototypes*

## Design Patterns
### Factory Design Pattern (FDP)
The FDP is used to create MessageHandler instances for different applications, managing feedback messages efficiently.
### Observer Design Pattern (ODP)
The ODP will be implemented for the following and followers feature in the next release, enabling users to receive notifications about updates from accounts they follow, boosting user engagement.

## Proposal Document
You can view the proposal document [here](https://docs.google.com/document/d/1DYpF0NFRY3Cn5sV4eGW7F81uCOLlB1t9spdQu9ub58M/edit?usp=sharing)
