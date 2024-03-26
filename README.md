# Hulk Chat App Backend

## Overview
This document provides instructions for setting up and running the backend for the Hulk Chat App, a Flask-based application utilizing WebSocket for real-time communication and PostgreSQL for data persistence.

## Prerequisites
- Docker and Docker Compose (for local development)
- Python 3.8+
- Poetry for Python dependency management

## Local Development Setup

1. **Environment Variables**: Copy the `.env.example` to `.env` and adjust the variables to match your local setup, particularly for `DATABASE_URI` and `REDIS_URL`.

   2. **Starting PostgreSQL and Redis**:
       - Ensure Docker is running.
       - From the project root, start the services with Docker Compose:
         ```bash
         docker-compose up -d
         ```
         This command starts PostgreSQL and Redis services in detached mode.

      pgAdmin Setup: To manage your PostgreSQL database via a web interface, pgAdmin is included as part of the Docker setup.
   
      Access pgAdmin at http://localhost:5050.
      Log in using the default email and password specified in the docker-compose.yml (e.g., admin@admin.com and admin).
      To connect pgAdmin to your PostgreSQL database:
      Right-click on "Servers" > "Create" > "Server".
      Name your server (e.g., "Hulk Chat DB").
      Under the "Connection" tab, set "Hostname/Address" to postgres, "Username" to your POSTGRES_USER, and "Password" to your POSTGRES_PASSWORD. The database name is your POSTGRES_DB.


3. **Installing Dependencies**:
    - Install project dependencies with Poetry:
      ```bash
      poetry install
      ```

4. **Database Migrations**:
    - Initialize the database and run migrations:
      ```bash
      poetry run flask db init  # Only needed if you haven't run it before
      poetry run flask db migrate -m "Initial migration."
      poetry run flask db upgrade
      ```

5. **Running the Application**:
    - Start the Flask application with:
      ```bash
      poetry run flask run
      ```
    - Or, to use the Flask-SocketIO server:
      ```bash
      poetry run python app.py
      ```

## Deployment

This project is configured for deployment to Heroku with PostgreSQL and Redis add-ons. Follow the standard Heroku deployment process, ensuring that `DATABASE_URI` and `REDIS_URL` environment variables are set in your Heroku app settings to match the credentials provided by Heroku.

## Features

- Real-time chat functionality using Flask-SocketIO.
- User authentication and registration.
- Message persistence with PostgreSQL.
- Environment isolation with Docker for local development.
- Easy deployment setup for Heroku.

For detailed information on project setup, features, and more, refer to the specific sections of this README.

