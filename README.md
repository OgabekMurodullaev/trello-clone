# Trello Clone Backend

A backend implementation of a Trello-like project management tool built with Django Rest Framework. This project replicates core functionalities of Trello, such as creating boards, lists, and tasks, with support for real-time updates and task scheduling.

## Features
- Create, update, and delete boards, lists, and tasks.
- User authentication and authorization (JWT-based).
- Real-time notifications using Django signals.
- Asynchronous task processing with Celery and Redis.
- RESTful API endpoints for seamless frontend integration.
- Role-based access control for board members (e.g., admin, member).

## Tech Stack
- **Framework**: Django, Django Rest Framework
- **Database**: PostgreSQL (or SQLite for development)
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Authentication**: JWT (django-rest-framework-simplejwt)
- **Others**: Django Signals for event-driven actions

## Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- Redis
- Virtualenv (recommended)

## Installation

1. **Clone the repository**:
   ```bash
   https://github.com/OgabekMurodullaev/trello-clone.git
   cd trello-clone-backend
   ```
2. **Set up a virtual environment**
    ```
   python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
    ```pip install -r requirements.txt```

4. **Configure environment variables: Create a .env file in the project root and add the following**
    ```
   SECRET_KEY=your_secret_key
   DEBUG=debug

   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=example@gmail.com
   EMAIL_HOST_PASSWORD=password
   ```
5. **Run database migrations**
    ```python manage.py migrate```
6. **Start the Redis server**
    ```redis-server```
7. **Start the Celery worker**
    ```celery -A trello_clone worker --loglevel=info```
8. **Run the project**
    ```python manage.py runserver```