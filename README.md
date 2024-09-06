# Trivia App

This project if forked from Udacity's Full Stack Developer Nanodegree project at [Udacity](https://github.com/udacity/cd0037-API-Development-and-Documentation-project).

The goal of this project is to create a basic CRUD application for a simple trivia game. The rubric for this project says that the app should:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

The original repo comes with starter code for the backend Flask-based API written in Python, with a test database written in PostgreSQL, as well as a React frontend.

## Improvements

I have made several improvements to the structure of the application, to use the latest versions of all tech across the stack and to containerize the entire application using Docker and Docker Compose.

### Backend

The initial [backend](./backend/README.md) directory contained a partially completed Flask and SQLAlchemy server. The idea was to work primarily in `backend/flaskr/__init__.py` to define endpoints, and to reference `models.py` for DB and SQLAlchemy setup.

For more complex applications, I might add some more project structure, breaking out API components into separate directories, and integrating them into the application using blueprints.  However, I chose to keep the simple project structure with all the API definitions in a single file.

The main improvement to the backend is to implement Poetry for dependency management and virtualization.  Instead of a static `requirements.txt` file, and installing dependencies with `pip install`, the application uses Poetry to handle those libraries.  I've also used minimum version requirements so that the latest versions of all libraries are used.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contained a complete React frontend to consume the data from the Flask server. This frontend made use of React v16, and some older JS / jQuery patterns for querying API endpoints. The styling for React components was also quite minimal.

My improvements to the frontend include upgrading the `package.json` with the latest versions of React and its supporting packages, removing the jQuery dependency in favor of modern JS `fetch()` methods, using React Hooks to handle state and dynamically update the view, and improving the look and feel of the user interface via CSS.

> View the [Frontend README](./frontend/README.md) for more details.

### Deployment

Deploying the application is simplified through the use of Docker containers, and Docker Compose. The backend features three services:

- `db`: a Postgres image to store the supplied `trivia.psql` database, available on port `5432`
- `app`: a Python image to run the Flask app API endpoints on port `5000`
- `admin`: an Adminer image for db access (using the postgres credentials defined for the `db` service) on port `8080`

and the frontend has a single service:

- `frontend`: a NodeJS image to run the React app at `localhost:3000`

Starting the entire application is simplified with docker-compose commands. (If you don't have Docker and/or Docker Compose installed, see the [docs](https://docs.docker.com/engine/install/).)  From the project directory run:

```
docker-compose up -d --build
```

This will build and deploy all the services needed to run the application. Once the React frontend has compiled (you can check the status by running `docker logs -f`), the app can be accessed at [http://localhost:3000](http://localhost:3000).

Please note the use of `http` and NOT `https`.  CORS is not set up to handle requests across security protocols.

To verify that the database has populated as expected, log in to the Adminer service at [http://localhost:8080](http://localhost:8080) with the follwing credentials:

```
System: PostgreSQL
Server: db
Username: postgres
Password: postgres
Database: db
```

To stop the project and remove the container, run:

```
docker-compose down
```

or, to also remove peristent data:

```
docker-compose down -v
```

## Testing

A suite of unit tests is defined at `backend/test_flasker.py`.  These will test the validity of all available endpoints defined in the `flaskr` app, as well as the various error handlers associated with those endpoints.  See the [Backend README](./backend/README.md) for a detailed explanation of each endpoint.

To run the tests, you'll need to access the Docker container running the `app` service.  There are many ways to accomplish this, but I will outline the simplest: running the Docker container shell in the terminal, one with VSCode Dev Containers.

To access the bash shell command line for the `app` service, while the Docker container is running, run:

```
docker exec -it trivia-app sh
```

Then, to launch the test suite, run:

```
python test_flaskr.py
```

The tests will initialize, populate the test database, then give a status of `OK` if successful.

To exit the container shell, run:

```
exit
```
