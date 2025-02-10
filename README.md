# 3Restaurant Django Application


Prerequisites

Before running this project, ensure you have the following installed:

For running locally:

Python 3.9 or above

PostgreSQL

pipenv or pip

For running with Docker:

Docker

Docker Compose

Environment Variables:

consider that .env file should not be on the git repository. However, I have prepared it for you on git to run the project simply.



Running the Project

1. Run Locally

If you want to run the project locally (without Docker):


Clone the repository

cd restaurant

Create and activate a virtual environment:

pip install -r requirements.txt

Set DEBUG=True in your .env file.

python manage.py makemigrations

python manage.py migrate

Run the development server

python manage.py runserver



2. Run with Docker

If you want to run the project using Docker:



Clone the repository

git clone 

cd restaurant

Ensure Docker is installed and running on your system.

Set DEBUG=False in your .env file.

Build and run the containers

sudo docker-compose up --build


Running Tests

To run the tests for the project:


Activate your virtual environment (if running locally) or open a shell in the app container (if using Docker):

python manage.py test


URLs

Admin Panel: http://localhost:8000/admin

User Sign-Up Page [POST]: http://localhost:8000/users/sign-up/

User Login Page [POST]: http://localhost:8000/users/login/verify-password/

Create Table [POST]: http://localhost:8000/tables

List of Tables [GET]: http://localhost:8000/tables

Book an Order [POST]: http://localhost:8000/tables/book/

Cancel an Order [POST]: http://localhost:8000/tables/cancel/
