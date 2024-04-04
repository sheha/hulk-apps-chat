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
      poetry run flask db init  
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


### Frontend Setup

1. **Installing Dependencies**:
   - Navigate to the frontend directory and install npm packages:
     ```bash
     npm install
     ```

2. **Running the Development Server**:
   - Serve the application with hot reload at `localhost:8080`:
     ```bash
     npm run serve
     ```

3. **Building for Production**:
   - Compile and minify for production:
     ```bash
     npm run build
     ```
## Deployment

This project is ready for deployment to Heroku with PostgreSQL and Redis add-ons. Set up your Heroku app and configure `DATABASE_URI` and `REDIS_URL` to match Heroku's add-on credentials.

## Features

- Real-time chat with multiple rooms.
- User authentication and profile management.
- Message status indicators (sent, delivered, read).
- Online/offline user status.
- Scalable architecture suitable for deploying on platforms like Heroku.

## File Structure

- `backend/`: Contains all backend code including Flask application, SocketIO setup, models, migrations, and utilities.
- `frontend/`: Houses the Vue.js application with components, assets, and service configurations.
- `docker-compose.yml`: Docker configuration for local development services.
- `Procfile`: Contains commands for Heroku deployment.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

