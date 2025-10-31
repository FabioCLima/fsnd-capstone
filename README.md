# Casting Agency API - Full Stack Nanodegree Capstone Project

A RESTful API for managing actors and movies for a casting agency, built as the final project for Udacity's Full Stack Nanodegree program.

## Live Demo

**Application URL:** https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/

## Project Overview

The Casting Agency API is a backend application that enables users to:
- Create, read, update, and delete actors
- Create, read, update, and delete movies
- Manage the relationship between actors and movies
- Validate all input data using Pydantic schemas

This project demonstrates:
- RESTful API design principles
- Modern Python development with type hints
- Database modeling with SQLAlchemy 2.0
- Data validation with Pydantic 2.x
- Deployment to Heroku with PostgreSQL
- Professional code organization and documentation

## Technology Stack

- **Python 3.10** - Programming language
- **Flask 3.0** - Web framework
- **SQLAlchemy 2.0** - ORM with modern typed mappings
- **Pydantic 2.9** - Data validation and serialization
- **PostgreSQL** - Production database
- **Gunicorn** - WSGI HTTP Server
- **Heroku** - Cloud platform deployment
- **UV** - Modern Python package manager

## Project Structure

```
starter/
├── app.py              # Flask application and API endpoints
├── models.py           # SQLAlchemy models and Pydantic schemas
├── auth.py             # Auth0 integration and @requires_auth decorator
├── test_app.py         # Unit tests
├── pyproject.toml      # UV package configuration
├── requirements.txt    # Python dependencies
├── Procfile            # Heroku deployment configuration
├── runtime.txt         # Python version for Heroku
├── setup.sh           # Environment variables script
├── manage.py (optional) # DB management helpers (create/drop/seed)
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Data Models

### Actor
- `id` (Integer, Primary Key)
- `name` (String, required) - Actor's full name
- `age` (Integer, required) - Actor's age (1-150)
- `gender` (String, required) - Actor's gender
- `created_at` (DateTime) - Record creation timestamp

### Movie
- `id` (Integer, Primary Key)
- `title` (String, required) - Movie title
- `release_date` (DateTime, required) - Movie release date
- `created_at` (DateTime) - Record creation timestamp

### MovieActor (Association Table)
- Many-to-many relationship between Movies and Actors
- `id` (Integer, Primary Key)
- `movie_id` (Foreign Key to movies)
- `actor_id` (Foreign Key to actors)

## API Endpoints

### Health Check
```http
GET /
```
Returns API status and available endpoints.

**Response:**
```json
{
  "success": true,
  "message": "Casting Agency API is running!",
  "endpoints": {
    "movies": "/api/movies",
    "actors": "/api/actors"
  }
}
```

### Actors

#### Get All Actors
```http
GET /api/actors
```

**Success Response (200):**
```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Tom Hanks",
      "age": 67,
      "gender": "Male",
      "created_at": "2025-10-31T01:59:14.890404"
    }
  ],
  "total_actors": 1
}
```

#### Get Actor by ID
```http
GET /api/actors/<actor_id>
```

**Success Response (200):**
```json
{
  "success": true,
  "actor": {
    "id": 1,
    "name": "Tom Hanks",
    "age": 67,
    "gender": "Male",
    "created_at": "2025-10-31T01:59:14.890404"
  }
}
```

#### Create Actor
```http
POST /api/actors
Content-Type: application/json

{
  "name": "Tom Hanks",
  "age": 67,
  "gender": "Male"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "actor": {
    "id": 1,
    "name": "Tom Hanks",
    "age": 67,
    "gender": "Male",
    "created_at": "2025-10-31T01:59:14.890404"
  }
}
```

**Validation Error Response (422):**
```json
{
  "success": false,
  "error": "Validation error",
  "details": [
    {
      "type": "int_parsing",
      "loc": ["age"],
      "msg": "Input should be a valid integer"
    }
  ]
}
```

#### Update Actor
```http
PATCH /api/actors/<actor_id>
Content-Type: application/json

{
  "age": 68
}
```

**Success Response (200):**
```json
{
  "success": true,
  "actor": {
    "id": 1,
    "name": "Tom Hanks",
    "age": 68,
    "gender": "Male",
    "created_at": "2025-10-31T01:59:14.890404"
  }
}
```

#### Delete Actor
```http
DELETE /api/actors/<actor_id>
```

**Success Response (200):**
```json
{
  "success": true,
  "deleted": 1
}
```

### Movies

#### Get All Movies
```http
GET /api/movies
```

**Success Response (200):**
```json
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Forrest Gump",
      "release_date": "1994-07-06T00:00:00",
      "created_at": "2025-10-31T02:00:00.000000"
    }
  ],
  "total_movies": 1
}
```

#### Get Movie by ID
```http
GET /api/movies/<movie_id>
```

**Success Response (200):**
```json
{
  "success": true,
  "movie": {
    "id": 1,
    "title": "Forrest Gump",
    "release_date": "1994-07-06T00:00:00",
    "created_at": "2025-10-31T02:00:00.000000"
  }
}
```

#### Create Movie
```http
POST /api/movies
Content-Type: application/json

{
  "title": "Forrest Gump",
  "release_date": "1994-07-06T00:00:00"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "movie": {
    "id": 1,
    "title": "Forrest Gump",
    "release_date": "1994-07-06T00:00:00",
    "created_at": "2025-10-31T02:00:00.000000"
  }
}
```

#### Update Movie
```http
PATCH /api/movies/<movie_id>
Content-Type: application/json

{
  "title": "Forrest Gump (Special Edition)"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "movie": {
    "id": 1,
    "title": "Forrest Gump (Special Edition)",
    "release_date": "1994-07-06T00:00:00",
    "created_at": "2025-10-31T02:00:00.000000"
  }
}
```

#### Delete Movie
```http
DELETE /api/movies/<movie_id>
```

**Success Response (200):**
```json
{
  "success": true,
  "deleted": 1
}
```

## Error Handling

The API returns standardized error responses:

### 400 Bad Request
```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

### 405 Method Not Allowed
```json
{
  "success": false,
  "error": 405,
  "message": "Method not allowed"
}
```

### 422 Unprocessable Entity
```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable entity"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```

## Local Development Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- UV package manager (recommended) or pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/FabioCLima/fsnd-capstone.git
cd fsnd-capstone
```

2. **Install UV (if not already installed)**
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

3. **Create PostgreSQL database**
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE capstone;

# Exit psql
\q
```

4. **Configure environment variables**
```bash
# Copy example file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Example `.env` file:
```env
DATABASE_URL=postgresql://localhost:5432/capstone
FLASK_APP=app.py
FLASK_ENV=development
PORT=8080
# Auth0 config
# Prefer API_AUDIENCE; AUTH0_AUDIENCE kept for compatibility
AUTH0_DOMAIN=your-domain.auth0.com
API_AUDIENCE=casting-agency
ALGORITHMS=RS256
```

5. **Install dependencies**
```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

6. **Initialize database**
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Create tables
python -c "from app import APP; from models import db; APP.app_context().push(); db.create_all()"
```

7. **Run the application**
```bash
# Using UV
uv run python app.py

# Or if environment is activated
python app.py
```

The API will be available at: `http://localhost:8080`

## Authentication and Authorization

This project includes `auth.py` with helpers for Auth0 JWT validation and a `@requires_auth` decorator you can apply to endpoints. Configure the following environment variables (via `.env` or `setup.sh`):

- `AUTH0_DOMAIN` (e.g., `your-tenant.auth0.com`)
- `API_AUDIENCE` (your API identifier, e.g., `casting-agency`)
- `ALGORITHMS` (comma-separated list, default `RS256`)

Example usage in `app.py` (not enforced by default):
```python
from auth import requires_auth

@app.route('/api/movies-secure')
@requires_auth('read:movies')
def get_movies_secure():
    ...
```

## Testing

Run the test suite:

```bash
# Using UV
uv run pytest

# Or with coverage
uv run pytest --cov=. --cov-report=html
```

## Deployment to Heroku

### Prerequisites

- Heroku account (verified with payment method)
- Heroku CLI installed

### Deployment Steps

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**
```bash
heroku login -i
```

3. **Create Heroku app**
```bash
heroku create your-app-name
```

4. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:essential-0
```

5. **Set environment variables**
```bash
heroku config:set FLASK_APP=app.py
heroku config:set FLASK_ENV=production
```

6. **Deploy application**
```bash
git push heroku main
```

7. **Initialize database**
```bash
heroku run "python -c 'from app import APP; from models import db; APP.app_context().push(); db.create_all()'"
```

8. **Open application**
```bash
heroku open
```

### Useful Heroku Commands

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Run commands
heroku run python

# View configuration
heroku config

# Reset database
heroku pg:reset DATABASE_URL
heroku run "python -c 'from app import APP; from models import db; APP.app_context().push(); db.create_all()'"
```

## Testing the Live API

### Using curl

**Get all actors:**
```bash
curl https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors
```

**Create an actor:**
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors \
  -H "Content-Type: application/json" \
  -d '{"name": "Meryl Streep", "age": 74, "gender": "Female"}'
```

**Create a movie:**
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/movies \
  -H "Content-Type: application/json" \
  -d '{"title": "The Devil Wears Prada", "release_date": "2006-06-30T00:00:00"}'
```

**Update an actor:**
```bash
curl -X PATCH https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors/1 \
  -H "Content-Type: application/json" \
  -d '{"age": 75}'
```

**Delete a movie:**
```bash
curl -X DELETE https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/movies/1
```

## Features

### Data Validation with Pydantic

All input data is validated using Pydantic schemas:

- **Type checking** - Ensures correct data types (int, str, datetime)
- **Field validation** - Validates constraints (age 1-150, non-empty strings)
- **Automatic serialization** - Converts SQLAlchemy models to JSON
- **Detailed error messages** - Returns specific validation errors

Example validation error:
```json
{
  "success": false,
  "error": "Validation error",
  "details": [
    {
      "type": "int_parsing",
      "loc": ["age"],
      "msg": "Input should be a valid integer",
      "input": "not a number"
    }
  ]
}
```

### Modern SQLAlchemy 2.0

- **Typed mappings** - Using `Mapped` and `mapped_column`
- **Declarative models** - Clean and readable model definitions
- **Relationships** - Proper many-to-many with association table
- **Automatic timestamps** - Created_at fields with defaults

### Production Ready

- **CORS enabled** - Ready for frontend integration
- **Error handling** - Comprehensive error responses
- **Database migrations** - Support for Flask-Migrate
- **Environment configuration** - Using python-dotenv
- **Production WSGI server** - Gunicorn for deployment

## Future Enhancements

- [ ] Auth0 authentication and authorization
- [ ] Role-Based Access Control (RBAC)
  - Casting Assistant: View actors and movies
  - Casting Director: Add/delete actors, modify movies
  - Executive Producer: Full access
- [ ] Pagination for large datasets
- [ ] Search and filtering capabilities
- [ ] Actor-Movie relationship endpoints
- [ ] Integration tests
- [ ] CI/CD pipeline
- [ ] API documentation with Swagger/OpenAPI

## Author

**Fabio Lima**
- Email: lima.fisico@gmail.com
- GitHub: https://github.com/FabioCLima/fsnd-capstone
- Heroku App: https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/

## License

This project is part of the Udacity Full Stack Nanodegree program.

## Acknowledgments

- Udacity Full Stack Nanodegree Program
- Flask and SQLAlchemy communities
- Pydantic for excellent data validation
