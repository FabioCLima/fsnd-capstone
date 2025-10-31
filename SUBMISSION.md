# Udacity Full Stack Nanodegree - Capstone Project Submission

## Project Information

**Student Name:** Fabio Lima
**Student Email:** lima.fisico@gmail.com
**Project Name:** Casting Agency API
**Submission Date:** October 30, 2025

## Live Application

**Heroku URL:** https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/

**GitHub Repository:** [Add your repository URL here]

## Project Overview

The Casting Agency API is a RESTful backend service for managing actors and movies in a casting agency. The application demonstrates:

1. **Database Modeling** - PostgreSQL with SQLAlchemy 2.0
2. **API Development** - Flask with comprehensive CRUD endpoints
3. **Data Validation** - Pydantic schemas for input validation
4. **Deployment** - Production deployment on Heroku
5. **Code Quality** - Modern Python with type hints and proper structure

## Technology Stack

- Python 3.10
- Flask 3.0
- SQLAlchemy 2.0 (with typed mappings)
- Pydantic 2.9 (data validation)
- PostgreSQL
- Heroku (deployment)
- Gunicorn (WSGI server)
- UV (package management)

## Completed Requirements

### 1. Database Setup ✅

**Models Implemented:**
- `Actor` - Stores actor information (id, name, age, gender, created_at)
- `Movie` - Stores movie information (id, title, release_date, created_at)
- `MovieActor` - Association table for many-to-many relationship

**Features:**
- Modern SQLAlchemy 2.0 syntax with `Mapped` type hints
- Proper relationships and foreign keys
- Automatic timestamp tracking
- Database URL handling for Heroku (postgres:// to postgresql://)

**Files:**
- `models.py` - Lines 13-128 (SQLAlchemy models)

### 2. API Endpoints ✅

**Implemented Endpoints:**

**Actors:**
- `GET /api/actors` - List all actors
- `GET /api/actors/<id>` - Get specific actor
- `POST /api/actors` - Create new actor
- `PATCH /api/actors/<id>` - Update actor
- `DELETE /api/actors/<id>` - Delete actor

**Movies:**
- `GET /api/movies` - List all movies
- `GET /api/movies/<id>` - Get specific movie
- `POST /api/movies` - Create new movie
- `PATCH /api/movies/<id>` - Update movie
- `DELETE /api/movies/<id>` - Delete movie

**Health Check:**
- `GET /` - API status and endpoint listing

**Files:**
- `app.py` - Lines 43-278 (API routes)

### 3. Data Validation ✅

**Pydantic Schemas Implemented:**
- `ActorCreate` - Validation for creating actors
- `ActorUpdate` - Validation for updating actors (partial)
- `ActorResponse` - Serialization for actor responses
- `MovieCreate` - Validation for creating movies
- `MovieUpdate` - Validation for updating movies (partial)
- `MovieResponse` - Serialization for movie responses

**Validation Rules:**
- Name: String, 1-120 characters, required
- Age: Integer, 1-150 range, required
- Gender: String, 1-20 characters, required
- Title: String, 1-120 characters, required
- Release Date: DateTime, required

**Files:**
- `models.py` - Lines 135-206 (Pydantic schemas)

### 4. Error Handling ✅

**HTTP Error Codes Handled:**
- 400 - Bad Request
- 404 - Not Found
- 405 - Method Not Allowed
- 422 - Unprocessable Entity (validation errors)
- 500 - Internal Server Error

**Features:**
- Consistent JSON error responses
- Detailed validation error messages from Pydantic
- Proper error status codes

**Files:**
- `app.py` - Lines 284-322 (Error handlers)

### 5. Heroku Deployment ✅

**Deployment Configuration:**
- `Procfile` - Web process with Gunicorn
- `runtime.txt` - Python version specification
- `requirements.txt` - Production dependencies
- PostgreSQL addon configured (essential-0 plan)

**Environment Variables Set:**
- `DATABASE_URL` - Auto-configured by Heroku PostgreSQL addon
- `FLASK_APP` - Set to app.py
- `FLASK_ENV` - Set to production

**Database Initialized:**
- Tables created successfully on Heroku
- Tested with sample data

**Files:**
- `Procfile`
- `runtime.txt`
- `requirements.txt`

### 6. Code Quality ✅

**Modern Python Features:**
- Type hints with `Mapped` and `mapped_column`
- Pydantic for runtime validation
- Clean separation of concerns (models, schemas, routes)
- Comprehensive docstrings
- Environment variable configuration

**Project Structure:**
- Well-organized file structure
- Clear naming conventions
- Configuration files properly organized
- Example environment file provided

## Testing the Application

### Health Check
```bash
curl https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/
```

**Expected Response:**
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

### Create Actor
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors \
  -H "Content-Type: application/json" \
  -d '{"name": "Tom Hanks", "age": 67, "gender": "Male"}'
```

**Expected Response (201):**
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

### Get All Actors
```bash
curl https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors
```

**Expected Response (200):**
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

### Create Movie
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/movies \
  -H "Content-Type: application/json" \
  -d '{"title": "Forrest Gump", "release_date": "1994-07-06T00:00:00"}'
```

### Update Actor
```bash
curl -X PATCH https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors/1 \
  -H "Content-Type: application/json" \
  -d '{"age": 68}'
```

### Delete Actor
```bash
curl -X DELETE https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors/1
```

### Test Validation Error
```bash
curl -X POST https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/api/actors \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "age": "not a number", "gender": "Male"}'
```

**Expected Response (422):**
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

## Project Files

### Core Application Files
- `app.py` - Flask application with all API endpoints (332 lines)
- `models.py` - Database models and Pydantic schemas (207 lines)
- `test_app.py` - Unit tests (placeholder for future implementation)

### Configuration Files
- `pyproject.toml` - UV package manager configuration
- `requirements.txt` - Python dependencies for Heroku
- `Procfile` - Heroku process configuration
- `runtime.txt` - Python version specification
- `.env.example` - Environment variables template
- `setup.sh` - Local environment setup script

### Documentation
- `README.md` - Comprehensive project documentation
- `SUBMISSION.md` - This submission document
- `.gitignore` - Git ignore rules

## Running Locally

### Prerequisites
- Python 3.10+
- PostgreSQL
- UV package manager (optional but recommended)

### Setup Steps

1. Clone repository
2. Install dependencies: `uv sync` or `pip install -r requirements.txt`
3. Create database: `createdb capstone`
4. Configure environment variables (copy `.env.example` to `.env`)
5. Initialize database: Run Python command to create tables
6. Run application: `python app.py`
7. Access at `http://localhost:8080`

## Additional Features Implemented

### Beyond Basic Requirements:

1. **Pydantic Integration** - Modern data validation with detailed error messages
2. **Type Safety** - Full type hints using SQLAlchemy 2.0 Mapped types
3. **UV Package Manager** - Modern Python dependency management
4. **Comprehensive Documentation** - Detailed README with examples
5. **CORS Support** - Ready for frontend integration
6. **Partial Updates** - PATCH endpoints support partial updates using Pydantic
7. **Timestamps** - Automatic created_at tracking for all records
8. **Professional Error Handling** - Consistent error responses across all endpoints

## Known Limitations and Future Enhancements

### Current Limitations:
- No authentication/authorization implemented yet
- No pagination for large datasets
- No search/filtering capabilities
- Limited test coverage

### Planned Enhancements:
- [ ] Auth0 integration for authentication
- [ ] RBAC (Role-Based Access Control) implementation
- [ ] Pagination and filtering
- [ ] Actor-Movie relationship endpoints
- [ ] Comprehensive unit and integration tests
- [ ] CI/CD pipeline
- [ ] API documentation with Swagger/OpenAPI

## Submission Checklist

- ✅ PostgreSQL database with proper models
- ✅ Flask API with CRUD endpoints for actors and movies
- ✅ Data validation using Pydantic
- ✅ Error handling for all endpoints
- ✅ Deployed to Heroku with PostgreSQL addon
- ✅ README with comprehensive documentation
- ✅ Code follows PEP 8 style guidelines
- ✅ Type hints and modern Python practices
- ✅ Environment configuration properly handled
- ✅ Git repository with meaningful commit messages

## Contact Information

**Student:** Fabio Lima
**Email:** lima.fisico@gmail.com
**Heroku App:** https://fsnd-capstone-fabio-efc9d4953f5a.herokuapp.com/
**GitHub:** [To be added after pushing to GitHub]

---

**Declaration:** I confirm that this is my own work and I have not plagiarized any part of it. I have properly cited all sources used in the development of this project.

**Date:** October 30, 2025
