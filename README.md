# University Residence Management API

This project is a Django-based API for managing university residence buildings, rooms, and residents.

## Features

- CRUD operations for buildings, rooms, and residents
- RESTful API endpoints
- Swagger documentation
- Caching
- Filtering
- Searching
- Ordering

## Technologies Used

- Django
- Django REST Framework
- drf-yasg (for Swagger documentation)
- SQLite (default database)
- pylibmc
- pymemcache
- django-filter
- rest_framework.filters

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
- `/api/token-auth/`: Obtain authentication token
- Caching: List endpoints for buildings and rooms are cached for 15 minutes
- Filtering: Endpoints support filtering by various fields (e.g., building name, room capacity, resident check-in date)
- Searching: Endpoints support searching by specific fields (e.g., room number, resident email)
- Ordering: Endpoints support ordering by specific fields (e.g., building name, room capacity)

- `/api/buildings/`: CRUD operations for buildings
- `/api/rooms/`: CRUD operations for rooms
- `/api/residents/`: CRUD operations for residents

## Documentation

API documentation is available at `/docs/` when the server is running.
