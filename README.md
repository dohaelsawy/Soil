# :office: Soil Co-Working Space Management System
backend service for managing Soil Spaces, a co-working and community-focused workspace. 

## :dizzy: Features
- Browse available workspace details.
- Book workspaces with time-slot selection.
- Admin management of spaces and bookings.
- Role-based authentication.
- Input validation.
- Booking conflict prevention.
- Filter available spaces by type, capacity, or price range.
- Integrate rate-limiting to prevent abuse of public endpoints.

## :computer: Technology Stack

- Backend Framework: Django framework, Django RESTful framework
- Database: PostgreSQL
- Authentication: Role-based authentication
- Containerization: Docker

## :hammer_and_wrench: Prerequisites

- Docker
- Docker Compose
- python 

## :wrench: Installation
- clone the project using
```
git clone https://github.com/dohaelsawy/Soil.git
```
- Create .env file in the root of the project and setup the following environments variables:
```py
DB_ENGINE=django.db.backends.postgresql
DB_NAME=soil_spaces_db
DB_USER=postgres
DB_PASSWORD=DBpassword
DB_HOST=db
DB_PORT=5432
DEBUG=True
```
- Run docker:
```py
make up
```
this command will build and run docker container and establish the project
- Create a superadmin for access admin endpoints:
```py
make superuser
```
- Access swagger ui on the following url:
```
http://0.0.0.0:8000/api/docs/
```
- Run unit tests using following command:
```py
make test
```
