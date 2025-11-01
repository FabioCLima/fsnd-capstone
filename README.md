# Casting Agency API - Full Stack Nanodegree Capstone Project

A RESTful API for managing actors and movies for a casting agency, built as the final project for Udacity's Full Stack Nanodegree program.

## Live Demo

**Application URL:** https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/

## 📚 Documentation

This project includes comprehensive documentation:

- **[README.md](./README.md)** (this file) - Complete project documentation
- **[QUICK_START.md](./QUICK_START.md)** - Quick reference guide to get started
- **[AUTH0_SETUP.md](./AUTH0_SETUP.md)** - Step-by-step Auth0 configuration
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Detailed implementation changes
- **[COMPLETION_CHECKLIST.md](./COMPLETION_CHECKLIST.md)** - Project verification checklist
- **[SUBMISSION.md](./SUBMISSION.md)** - Project submission documentation

**🚀 New to this project? Start with [QUICK_START.md](./QUICK_START.md)**

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [Error Handling](#error-handling)
- [Local Development Setup](#local-development-setup)
- [Testing](#testing)
- [Deployment to Heroku](#deployment-to-heroku)
- [Testing the Live API](#testing-the-live-api)
- [Features](#features)
- [Implemented Features](#implemented-features)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

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
- **Auth0 JWT authentication and authorization**
- **Role-Based Access Control (RBAC)**
- **Comprehensive test suite (35+ tests)**
- Deployment to Heroku with PostgreSQL
- Professional code organization and documentation

## Technology Stack

### Backend & Framework
- **Python 3.10** - Programming language
- **Flask 3.0** - Web framework
- **SQLAlchemy 2.0** - ORM with modern typed mappings
- **Pydantic 2.9** - Data validation and serialization

### Authentication & Security
- **Auth0** - Authentication and authorization platform
- **python-jose** - JWT token validation
- **RBAC** - Role-Based Access Control implementation

### Database
- **PostgreSQL** - Production database
- **Flask-Migrate** - Database migration management

### Testing
- **unittest** - Python testing framework
- **35+ comprehensive tests** - Authentication, authorization, CRUD operations

### Deployment
- **Gunicorn** - WSGI HTTP Server
- **Heroku** - Cloud platform deployment
- **UV** - Modern Python package manager

## Project Structure

```
fsnd-capstone/
├── app.py                      # Flask application and API endpoints with auth
├── models.py                   # SQLAlchemy models and Pydantic schemas
├── auth.py                     # Auth0 integration and @requires_auth decorator
├── test_app.py                 # Comprehensive test suite (35+ tests)
│
├── README.md                   # Complete project documentation
├── AUTH0_SETUP.md             # Detailed Auth0 configuration guide
├── QUICK_START.md             # Quick reference guide
├── IMPLEMENTATION_SUMMARY.md  # Summary of all implementation changes
├── COMPLETION_CHECKLIST.md    # Project completion verification checklist
├── SUBMISSION.md              # Project submission documentation
│
├── pyproject.toml             # UV package configuration
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku deployment configuration
├── runtime.txt                # Python version for Heroku
├── .env.example              # Environment variables template
│
├── manage.py                  # Optional DB management helpers
└── migrations/                # Database migration files (if using Flask-Migrate)
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

**Note:** All endpoints except the health check require authentication. Include JWT token in Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

### Health Check
```http
GET /
```
Returns API status and available endpoints. **No authentication required.**

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
Authorization: Bearer YOUR_JWT_TOKEN
```
**Permission Required:** `get:actors`
**Roles:** Casting Assistant, Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
```
**Permission Required:** `get:actors`
**Roles:** Casting Assistant, Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "name": "Tom Hanks",
  "age": 67,
  "gender": "Male"
}
```
**Permission Required:** `post:actors`
**Roles:** Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "age": 68
}
```
**Permission Required:** `patch:actors`
**Roles:** Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
```
**Permission Required:** `delete:actors`
**Roles:** Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
```
**Permission Required:** `get:movies`
**Roles:** Casting Assistant, Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
```
**Permission Required:** `get:movies`
**Roles:** Casting Assistant, Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "title": "Forrest Gump",
  "release_date": "1994-07-06T00:00:00"
}
```
**Permission Required:** `post:movies`
**Roles:** Executive Producer only

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
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "title": "Forrest Gump (Special Edition)"
}
```
**Permission Required:** `patch:movies`
**Roles:** Casting Director, Executive Producer

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
Authorization: Bearer YOUR_JWT_TOKEN
```
**Permission Required:** `delete:movies`
**Roles:** Executive Producer only

**Success Response (200):**
```json
{
  "success": true,
  "deleted": 1
}
```

### API Endpoints Summary

Complete list of all endpoints with authentication requirements:

| Endpoint | Method | Permission | Assistant | Director | Producer | Description |
|----------|--------|------------|-----------|----------|----------|-------------|
| `/` | GET | None | ✅ | ✅ | ✅ | Health check (public) |
| `/api/actors` | GET | `get:actors` | ✅ | ✅ | ✅ | Get all actors |
| `/api/actors/<id>` | GET | `get:actors` | ✅ | ✅ | ✅ | Get specific actor |
| `/api/actors` | POST | `post:actors` | ❌ | ✅ | ✅ | Create new actor |
| `/api/actors/<id>` | PATCH | `patch:actors` | ❌ | ✅ | ✅ | Update actor |
| `/api/actors/<id>` | DELETE | `delete:actors` | ❌ | ✅ | ✅ | Delete actor |
| `/api/movies` | GET | `get:movies` | ✅ | ✅ | ✅ | Get all movies |
| `/api/movies/<id>` | GET | `get:movies` | ✅ | ✅ | ✅ | Get specific movie |
| `/api/movies` | POST | `post:movies` | ❌ | ❌ | ✅ | Create new movie |
| `/api/movies/<id>` | PATCH | `patch:movies` | ❌ | ✅ | ✅ | Update movie |
| `/api/movies/<id>` | DELETE | `delete:movies` | ❌ | ❌ | ✅ | Delete movie |

**Legend:**
- ✅ = Role has access
- ❌ = Role does not have access (will receive 403 Forbidden)

## Error Handling

The API returns standardized error responses in JSON format.

### Authentication Errors

#### 401 Unauthorized - Missing Token
```json
{
  "code": "authorization_header_missing",
  "description": "Authorization header is expected."
}
```

#### 401 Unauthorized - Invalid Token
```json
{
  "code": "token_expired",
  "description": "Token expired."
}
```

#### 401 Unauthorized - Malformed Header
```json
{
  "code": "invalid_header",
  "description": "Authorization header must start with Bearer."
}
```

#### 403 Forbidden - Insufficient Permissions
```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

### Standard HTTP Errors

#### 400 Bad Request
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

This API implements Auth0-based authentication with Role-Based Access Control (RBAC). All endpoints (except the health check endpoint `/`) require a valid JWT token with appropriate permissions.

### Roles and Permissions

The API defines three roles with different access levels:

#### 1. Casting Assistant
**Permissions:**
- `get:actors` - View actors
- `get:movies` - View movies

**Access:**
- ✅ GET `/api/actors`
- ✅ GET `/api/actors/<id>`
- ✅ GET `/api/movies`
- ✅ GET `/api/movies/<id>`

#### 2. Casting Director
**Permissions:**
- `get:actors` - View actors
- `get:movies` - View movies
- `post:actors` - Create actors
- `patch:actors` - Update actors
- `delete:actors` - Delete actors
- `patch:movies` - Update movies

**Access:**
- ✅ All Casting Assistant permissions
- ✅ POST `/api/actors`
- ✅ PATCH `/api/actors/<id>`
- ✅ DELETE `/api/actors/<id>`
- ✅ PATCH `/api/movies/<id>`

#### 3. Executive Producer
**Permissions:** All permissions
- `get:actors`, `get:movies`
- `post:actors`, `post:movies`
- `patch:actors`, `patch:movies`
- `delete:actors`, `delete:movies`

**Access:**
- ✅ All operations on all endpoints

### Auth0 Configuration

Configure the following environment variables:

```bash
AUTH0_DOMAIN=your-tenant.auth0.com
API_AUDIENCE=casting-agency
ALGORITHMS=RS256
```

For detailed Auth0 setup instructions, see [AUTH0_SETUP.md](./AUTH0_SETUP.md).

### Making Authenticated Requests

All API requests (except `/`) must include a valid JWT token in the Authorization header:

```bash
curl -X GET https://your-app.herokuapp.com/api/actors \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Authentication Error Responses

**Missing Token (401):**
```json
{
  "code": "authorization_header_missing",
  "description": "Authorization header is expected."
}
```

**Invalid Token (401):**
```json
{
  "code": "token_expired",
  "description": "Token expired."
}
```

**Insufficient Permissions (403):**
```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

## Testing & Coverage

To run the full test suite (~35 tests) and generate coverage reports:

```bash
# 1) Create/activate venv and install deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Load Auth0 env and fetch tokens (uses your M2M apps)
source ./setup.sh
fetch_assistant && fetch_director && fetch_producer

# 3) Execute tests (uses SQLite for tests)
./scripts/test.sh

# 4) Coverage (terminal + XML + HTML in ./htmlcov)
./scripts/coverage.sh
```

The test runner sets the following env vars:
- `FLASK_SKIP_APP_INIT_FOR_TESTS=1` and `FLASK_TESTING=1` to avoid initializing the default DB inside `create_app()`
- `DATABASE_URL_TEST=sqlite:////tmp/capstone_test.db` (override if needed)

## Auth0 Setup (summary)
- API (Identifier = `https://casting-agency-api`) with RBAC enabled and "Add Permissions in the Access Token" ON.
- Permissions:
  - Movies: `get:movies`, `post:movies`, `patch:movies`, `delete:movies`
  - Actors: `get:actors`, `post:actors`, `patch:actors`, `delete:actors`
- Roles:
  - Casting Assistant: `get:actors`, `get:movies`
  - Casting Director: `get:actors`, `get:movies`, `post:actors`, `patch:actors`, `delete:actors`, `patch:movies`
  - Executive Producer: all of the above plus `post:movies`, `delete:movies`
- Three Machine-to-Machine applications (one per role) authorized only with the scopes of the corresponding role. Their Client IDs/Secrets are referenced by `setup.sh`.

## Local Run (API)
```bash
source ./setup.sh
export PORT=8085 DATABASE_URL=sqlite:////tmp/capstone.db
python app.py
```

Health check:
```bash
curl -s http://localhost:$PORT/
```

Smoke examples:
```bash
# Assistant
fetch_assistant && use_assistant
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:$PORT/api/actors

# Director
fetch_director && use_director
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"Actor","age":30,"gender":"male"}' http://localhost:$PORT/api/actors

# Producer
fetch_producer && use_producer
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"Movie","release_date":"2025-01-01T00:00:00"}' http://localhost:$PORT/api/movies
```

## Security & Secrets
- Do not commit real secrets. `.gitignore` already ignores `setup.sh`.
- Tokens are fetched at runtime via Client Credentials. 

## Testing

The project includes a comprehensive test suite with 35+ tests covering:
- Public endpoints (health check)
- Authentication (missing, invalid, and valid tokens)
- Authorization (RBAC - different roles and permissions)
- CRUD operations for actors and movies
- Error handling (404, 422, 401, 403)
- Data validation

### Setup Test Database

```bash
# Create test database
createdb capstone_test

# Or using PostgreSQL
sudo -u postgres psql
CREATE DATABASE capstone_test;
\q
```

### Configure Test Environment Variables

Create a `.env.test` file or set environment variables:

```bash
DATABASE_URL_TEST=postgresql://localhost:5432/capstone_test

# JWT tokens for testing (obtain from Auth0)
ASSISTANT_TOKEN=your_assistant_jwt_token
DIRECTOR_TOKEN=your_director_jwt_token
PRODUCER_TOKEN=your_producer_jwt_token
```

### Running Tests

```bash
# Using unittest (recommended)
python test_app.py

# Run with verbose output
python test_app.py -v

# Run specific test
python test_app.py CastingAgencyTestCase.test_001_health_check

# Using pytest (if installed)
pytest test_app.py

# With coverage
pytest test_app.py --cov=. --cov-report=html
```

### Test Coverage

The test suite includes:
- **1 test** for public endpoints
- **6 tests** for GET endpoints with different auth levels
- **10 tests** for POST endpoints (create operations)
- **7 tests** for PATCH endpoints (update operations)
- **7 tests** for DELETE endpoints
- **4 tests** for error cases (404, invalid data, invalid tokens)

**Total: 35 comprehensive tests**

### Expected Test Results

When JWT tokens are not set, tests requiring authentication will be skipped. To run all tests, ensure you have valid JWT tokens in your environment variables.

```
...s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s.s
----------------------------------------------------------------------
Ran 35 tests in 0.234s

OK (skipped=34)
```

With tokens configured:
```
...................................
----------------------------------------------------------------------
Ran 35 tests in 2.156s

OK
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

# Auth0 Configuration
heroku config:set AUTH0_DOMAIN=your-tenant.auth0.com
heroku config:set API_AUDIENCE=casting-agency
heroku config:set ALGORITHMS=RS256
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

**Important:** All endpoints except the health check require authentication. You need a valid JWT token from Auth0.

### Using curl

**Health check (no auth required):**
```bash
curl https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/
```

**Get all actors (requires token):**
```bash
curl https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Create an actor (requires Director or Producer token):**
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors \
  -H "Authorization: Bearer YOUR_DIRECTOR_OR_PRODUCER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Meryl Streep", "age": 74, "gender": "Female"}'
```

**Create a movie (requires Producer token only):**
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/movies \
  -H "Authorization: Bearer YOUR_PRODUCER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "The Devil Wears Prada", "release_date": "2006-06-30T00:00:00"}'
```

**Update an actor (requires Director or Producer token):**
```bash
curl -X PATCH https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors/1 \
  -H "Authorization: Bearer YOUR_DIRECTOR_OR_PRODUCER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"age": 75}'
```

**Delete a movie (requires Producer token only):**
```bash
curl -X DELETE https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/movies/1 \
  -H "Authorization: Bearer YOUR_PRODUCER_TOKEN"
```

**Expected error without token:**
```bash
curl https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors
# Returns: {"code": "authorization_header_missing", "description": "Authorization header is expected."}
```

### Getting JWT Tokens

To obtain JWT tokens for testing, follow the instructions in [AUTH0_SETUP.md](./AUTH0_SETUP.md). You'll need to:

1. Create an Auth0 account
2. Configure your API and roles
3. Create test users
4. Generate tokens for each role

See the [Token Generation](./AUTH0_SETUP.md#obtaining-jwt-tokens-for-testing) section for detailed instructions.

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
- **Auth0 authentication** - Secure JWT-based authentication
- **RBAC implementation** - Role-Based Access Control with 3 roles
- **Comprehensive testing** - 35+ tests covering all functionality
- **Error handling** - Comprehensive error responses with proper status codes
- **Database migrations** - Support for Flask-Migrate
- **Environment configuration** - Using python-dotenv
- **Production WSGI server** - Gunicorn for deployment
- **Security best practices** - No hardcoded secrets, environment-based configuration

## Implemented Features

- ✅ Auth0 authentication and authorization
- ✅ Role-Based Access Control (RBAC)
  - Casting Assistant: View actors and movies
  - Casting Director: Add/delete actors, modify movies
  - Executive Producer: Full access
- ✅ Comprehensive test suite (35+ tests)
- ✅ JWT token validation with Auth0
- ✅ Permission-based access control
- ✅ Authentication error handling

## Future Enhancements

- [ ] Pagination for large datasets
- [ ] Search and filtering capabilities
- [ ] Actor-Movie relationship endpoints (assign actors to movies)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] API documentation with Swagger/OpenAPI
- [ ] Rate limiting for API endpoints
- [ ] Caching for frequently accessed data
- [ ] Advanced filtering and sorting options

## Author

**Fabio Lima**
- Email: lima.fisico@gmail.com
- GitHub: https://github.com/FabioCLima/fsnd-capstone
- Heroku App: https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/

## License

MIT License

Copyright (c) 2023 Fabio Lima


## Acknowledgments

- Udacity Full Stack Nanodegree Program
- Flask and SQLAlchemy communities
- Pydantic for excellent data validation
- Auth0 for authentication platform

## Getting Help

### Documentation Resources

- **Quick Start Issues**: Check [QUICK_START.md](./QUICK_START.md)
- **Auth0 Configuration**: See [AUTH0_SETUP.md](./AUTH0_SETUP.md)
- **Testing Problems**: Review the [Testing](#testing) section above
- **Deployment Issues**: Check [Deployment to Heroku](#deployment-to-heroku) section

### Common Issues

**Authentication not working?**
- Verify Auth0 is configured correctly (see AUTH0_SETUP.md)
- Check that RBAC is enabled in Auth0 API settings
- Ensure "Add Permissions in the Access Token" is enabled
- Verify environment variables are set correctly

**Tests failing?**
- Ensure JWT tokens are set as environment variables
- Verify test database exists (capstone_test)
- Check tokens haven't expired (regenerate if needed)

**Deployment issues?**
- Verify all Heroku config vars are set
- Check Heroku logs: `heroku logs --tail`
- Ensure PostgreSQL addon is attached

### Contact

For project-specific questions or issues:
- **Email**: lima.fisico@gmail.com
- **GitHub Issues**: https://github.com/FabioCLima/fsnd-capstone/issues
