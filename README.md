# University Residence Management API

This project is a Django-based API for managing university residence buildings, rooms, and residents.

## Features

- CRUD operations for buildings, rooms, and residents
- RESTful API endpoints
- Swagger documentation

## Technologies Used

- Django
- Django REST Framework
- drf-yasg (for Swagger documentation)
- SQLite (default database)

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/uni_residence_project.git
   cd uni_residence_project
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```
   python manage.py migrate
   ```

5. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `/api/buildings/`: CRUD operations for buildings
- `/api/rooms/`: CRUD operations for rooms
- `/api/residents/`: CRUD operations for residents

## Documentation

API documentation is available at `/docs/` when the server is running.
