# Quick Start Guide - Casting Agency API

This guide helps you quickly set up and test the Casting Agency API with Auth0 authentication.

## Step 1: Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Step 2: Set Up Databases

```bash
# Production database
createdb capstone

# Test database
createdb capstone_test
```

## Step 3: Configure Auth0

Follow the detailed guide in [AUTH0_SETUP.md](./AUTH0_SETUP.md) to:
1. Create an Auth0 account
2. Create an API with identifier `casting-agency`
3. Enable RBAC and add permissions to access token
4. Create 8 permissions (get:actors, get:movies, post:actors, post:movies, etc.)
5. Create 3 roles (Casting Assistant, Casting Director, Executive Producer)
6. Create test users and assign roles
7. Obtain JWT tokens for testing

## Step 4: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
nano .env
```

Required variables:
```bash
DATABASE_URL=postgresql://localhost:5432/capstone
AUTH0_DOMAIN=your-tenant.auth0.com
API_AUDIENCE=casting-agency
ALGORITHMS=RS256
```

For testing, also set:
```bash
DATABASE_URL_TEST=postgresql://localhost:5432/capstone_test
ASSISTANT_TOKEN=your_assistant_jwt_token
DIRECTOR_TOKEN=your_director_jwt_token
PRODUCER_TOKEN=your_producer_jwt_token
```

## Step 5: Run the Application

```bash
# Using UV
uv run python app.py

# Or if environment is activated
python app.py
```

The API will be available at: `http://localhost:8080`

## Step 6: Test the API

### Health Check (No Auth Required)
```bash
curl http://localhost:8080/
```

### Get Actors (Requires Token)
```bash
curl http://localhost:8080/api/actors \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create Actor (Requires Director or Producer Token)
```bash
curl -X POST http://localhost:8080/api/actors \
  -H "Authorization: Bearer YOUR_DIRECTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tom Hanks",
    "age": 67,
    "gender": "Male"
  }'
```

## Step 7: Run Tests

```bash
# Export tokens
export ASSISTANT_TOKEN="your_assistant_token"
export DIRECTOR_TOKEN="your_director_token"
export PRODUCER_TOKEN="your_producer_token"

# Run tests
python test_app.py -v
```

Expected output:
```
test_001_health_check ... ok
test_002_get_actors_without_token ... ok
...
Ran 35 tests in 2.156s

OK
```

## RBAC Quick Reference

### Casting Assistant
**Can:**
- View actors (GET /api/actors)
- View movies (GET /api/movies)

**Cannot:**
- Create, update, or delete anything

### Casting Director
**Can:**
- Everything Casting Assistant can do
- Create actors (POST /api/actors)
- Update actors (PATCH /api/actors/<id>)
- Delete actors (DELETE /api/actors/<id>)
- Update movies (PATCH /api/movies/<id>)

**Cannot:**
- Create movies (POST /api/movies)
- Delete movies (DELETE /api/movies/<id>)

### Executive Producer
**Can:**
- Everything - Full access to all endpoints

## Common Issues

### "authorization_header_missing"
- You forgot to include the Authorization header
- Add: `-H "Authorization: Bearer YOUR_TOKEN"`

### "unauthorized" (403)
- Your token doesn't have the required permission
- Check your role has the correct permissions in Auth0

### "token_expired" (401)
- Your JWT token has expired (default: 24 hours)
- Generate a new token from Auth0

### Tests are skipped
- JWT tokens are not set as environment variables
- Set ASSISTANT_TOKEN, DIRECTOR_TOKEN, and PRODUCER_TOKEN

## API Endpoints Summary

| Endpoint | Method | Permission | Roles |
|----------|--------|------------|-------|
| `/` | GET | None | All (public) |
| `/api/actors` | GET | `get:actors` | All roles |
| `/api/actors/<id>` | GET | `get:actors` | All roles |
| `/api/actors` | POST | `post:actors` | Director, Producer |
| `/api/actors/<id>` | PATCH | `patch:actors` | Director, Producer |
| `/api/actors/<id>` | DELETE | `delete:actors` | Director, Producer |
| `/api/movies` | GET | `get:movies` | All roles |
| `/api/movies/<id>` | GET | `get:movies` | All roles |
| `/api/movies` | POST | `post:movies` | Producer only |
| `/api/movies/<id>` | PATCH | `patch:movies` | Director, Producer |
| `/api/movies/<id>` | DELETE | `delete:movies` | Producer only |

## Next Steps

1. **Deploy to Heroku**: Follow deployment instructions in README.md
2. **Add More Tests**: Extend the test suite as needed
3. **Implement Pagination**: Add pagination for large datasets
4. **Add Search**: Implement search and filtering
5. **CI/CD Pipeline**: Set up automated testing and deployment

## Resources

- [README.md](./README.md) - Full documentation
- [AUTH0_SETUP.md](./AUTH0_SETUP.md) - Detailed Auth0 configuration
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Complete implementation details

## Support

For issues or questions:
- Check the troubleshooting section in AUTH0_SETUP.md
- Review error responses in README.md
- Verify Auth0 configuration matches the guide

---

**Happy coding! 🚀**
