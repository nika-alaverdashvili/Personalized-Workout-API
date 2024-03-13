# Personalized Workout API

## Introduction
The Personalized Workout API provides a platform for users to create and manage their workout plans, track fitness progress, and browse a variety of exercises tailored to their fitness goals. This RESTful API is designed to help users stay on track with their fitness routines and achieve their health objectives efficiently.

## Technology Stack
- **Python**: The main programming language.
- **Django & Django REST Framework**: Powers the web application and API.
- **PostgreSQL**: Manages all user data and workout information.
- **Docker & Docker Compose**: Simplifies deployment and service management.
- **GitHub Actions**: Automates testing, linting, and deployment processes.

## Deployment
To set up the Personalized Workout API locally, execute the following:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nika-alaverdashvili/personalized-workout-api.git
   ```
   ```bash
   cd personalized-workout-api/
   ```

2. **Build the Docker image**:
   ```sh
   docker-compose build
   ```

3. **Run the API using Docker Compose**:
   ```sh
   docker-compose up
   ```

4. **Create a superuser for accessing the admin panel**:
   ```sh
   docker-compose run --rm app sh -c "python manage.py createsuperuser"
   ```

## Development
Once the setup is complete, you can further ensure the application’s robustness:

1. **Running Unit Tests**:
   Verify all functionalities:
   ```sh
   docker-compose run --rm app sh -c "python manage.py test"
   ```

2. **Linting with Flake8**:
   Maintain code quality:
   ```sh
   docker-compose run --rm app sh -c "flake8"
   ```

3. **Database Readiness Check**:
   Confirm database availability:
   ```sh
   docker-compose run --rm app sh -c "python manage.py wait_for_db"
   ```

## Admin Panel Access
Access the administrative dashboard via:
```
http://127.0.0.1:8000/admin/
```
Log in with the superuser credentials to oversee application settings and data.

## Interactive API Documentation with Swagger
Explore the API functionalities through:
```
http://127.0.0.1:8000/api/docs/
```
This interactive documentation provides a hands-on approach to learning and testing the API’s capabilities.

## JSON Requests

### User Registration and Authentication
To register a new user and access various endpoints, submit the following JSON payload:
```json
{
  "email": "user@example.com",
  "password": "password",
  "name": "your_name"
}
```

After obtaining your token, click on the top right authorization button in the Swagger UI, which will allow you to access the user endpoint. For all subsequent operations, simply use your email and password for authorization via the same button located at the top right side. at [Swagger User Endpoint](http://127.0.0.1:8000/api/docs/#/user).

### Fitness Progress CRUD
For CRUD operations on fitness progress, authorization is required as previously mentioned. Access the detailed API documentation here: [Fitness Progress Endpoint](http://127.0.0.1:8000/api/docs/#/fitness-progress).

Example JSON request for creating or updating a fitness progress record:
```json
{
  "date": "2024-03-13",
  "weight": 100,
  "goal_weight": 90,
  "achieved_goals": "Health",
  "notes": "Sample note",
  "exercise_duration": 2,
  "calories_burned": 500,
  "mood": "excellent"
}
```

### Muscle Groups and Exercises CRUD
Initially, create a muscle group using the following JSON structure:
```json
{
  "name": "Biceps",
  "description": "Barbell curl"
}
```
For manipulation of exercises, first ensure a muscle group exists, then proceed with creating an exercise:
```json
{
  "name": "Bicep curls",
  "description": "Bicep curl exercise",
  "instructions": "Hold a dumbbell in each hand",
  "target_muscles": [11] // Ensure this is the correct ID
}
```

### Workout Plans and Exercises
Creating a new workout plan is accomplished with the following JSON structure:
```json
{
  "user": 1,  // Ensure this is the correct user ID
  "title": "Fitness Plan",
  "frequency": 5,
  "goal": "Gain weight",
  "session_duration": 55,
  "create_workout_exercises": []
}
```
After establishing a workout plan, you can create workout exercises linked to the plan with:
```json
{
  "workout_plan": 1, // Ensure this is the correct workout plan ID
  "exercise": 1, // Ensure this is the correct exercise ID
  "sets": 4,
  "repetitions": 7,
  "duration": 24
}

