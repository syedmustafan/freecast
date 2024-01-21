# Freecast Project

This is a Django project for a movie and TV show website with Docker integration.

## Prerequisites

Make sure you have the following tools installed on your machine:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to run the project locally using Docker:

### 1. Clone the Repository

```bash
git clone https://github.com/syedmustafan/freecast.git
cd freecast
```

### 2. Build and Run Docker Containers

```
docker-compose up --build
```

### 3. Apply Database Migrations
```
docker-compose exec django python manage.py migrate
```

### 4. Create a Superuser 
```
docker-compose exec django python manage.py createsuperuser

```
### 5. Access the Application
```
The Django application will be accessible at http://localhost:8000/. 
The admin panel is available at http://localhost:8000/admin/ if you created a superuser.

```

### 6. Stop and Remove Containers
```
docker-compose down

```

## Running Background Tasks

### Importing Shows and Movies:

```
docker-compose exec django python manage.py import_shows
docker-compose exec django python manage.py import_movies

```
### Testing Sources:

```
docker-compose exec django python manage.py test_sources

```

## Additional Information

##### The backgournd tasks will also run when the containers will be up. It will run according to the settings 
mentioned in the settings file. 
