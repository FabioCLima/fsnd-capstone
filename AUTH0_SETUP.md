# Auth0 RBAC Setup Guide

This document provides step-by-step instructions for configuring Auth0 authentication and Role-Based Access Control (RBAC) for the Casting Agency API.

## Overview

The Casting Agency API implements three roles with different permission levels:

### Roles and Permissions

| Role | Permissions | Description |
|------|------------|-------------|
| **Casting Assistant** | `get:actors`, `get:movies` | Can view actors and movies |
| **Casting Director** | `get:actors`, `get:movies`, `post:actors`, `patch:actors`, `delete:actors`, `patch:movies` | Can view all resources, add/delete actors, and modify movies |
| **Executive Producer** | All permissions | Full access to all resources |

### Permission Details

- `get:actors` - View actors list and individual actor details
- `get:movies` - View movies list and individual movie details
- `post:actors` - Create new actors
- `post:movies` - Create new movies
- `patch:actors` - Update existing actors
- `patch:movies` - Update existing movies
- `delete:actors` - Delete actors
- `delete:movies` - Delete movies

## Auth0 Configuration Steps

### 1. Create an Auth0 Account

1. Go to [Auth0](https://auth0.com/) and sign up for a free account
2. Choose a tenant domain (e.g., `your-casting-agency.auth0.com`)
3. Complete the account setup

### 2. Create an API

1. Navigate to **Applications → APIs** in the Auth0 Dashboard
2. Click **Create API**
3. Fill in the details:
   - **Name**: `Casting Agency API`
   - **Identifier**: `casting-agency` (this will be your `API_AUDIENCE`)
   - **Signing Algorithm**: `RS256`
4. Click **Create**

### 3. Enable RBAC

1. In your API settings, go to the **Settings** tab
2. Scroll down to **RBAC Settings**
3. Enable the following options:
   - ✅ **Enable RBAC**
   - ✅ **Add Permissions in the Access Token**
4. Click **Save**

### 4. Define Permissions

1. In your API, go to the **Permissions** tab
2. Add the following permissions one by one:

| Permission | Description |
|------------|-------------|
| `get:actors` | View actors |
| `get:movies` | View movies |
| `post:actors` | Create actors |
| `post:movies` | Create movies |
| `patch:actors` | Update actors |
| `patch:movies` | Update movies |
| `delete:actors` | Delete actors |
| `delete:movies` | Delete movies |

### 5. Create Roles

1. Navigate to **User Management → Roles** in the Auth0 Dashboard
2. Click **Create Role**

#### Casting Assistant Role

1. **Name**: `Casting Assistant`
2. **Description**: `Can view actors and movies`
3. Click **Create**
4. Go to the **Permissions** tab
5. Click **Add Permissions**
6. Select your API (`Casting Agency API`)
7. Select the following permissions:
   - ✅ `get:actors`
   - ✅ `get:movies`
8. Click **Add Permissions**

#### Casting Director Role

1. **Name**: `Casting Director`
2. **Description**: `Can manage actors and modify movies`
3. Click **Create**
4. Go to the **Permissions** tab
5. Click **Add Permissions**
6. Select your API (`Casting Agency API`)
7. Select the following permissions:
   - ✅ `get:actors`
   - ✅ `get:movies`
   - ✅ `post:actors`
   - ✅ `patch:actors`
   - ✅ `delete:actors`
   - ✅ `patch:movies`
8. Click **Add Permissions**

#### Executive Producer Role

1. **Name**: `Executive Producer`
2. **Description**: `Full access to all resources`
3. Click **Create**
4. Go to the **Permissions** tab
5. Click **Add Permissions**
6. Select your API (`Casting Agency API`)
7. Select all permissions:
   - ✅ `get:actors`
   - ✅ `get:movies`
   - ✅ `post:actors`
   - ✅ `post:movies`
   - ✅ `patch:actors`
   - ✅ `patch:movies`
   - ✅ `delete:actors`
   - ✅ `delete:movies`
8. Click **Add Permissions**

### 6. Create Test Users

1. Navigate to **User Management → Users**
2. Click **Create User**
3. Create three test users (one for each role):

#### User 1: Casting Assistant
- **Email**: `assistant@casting-agency.com`
- **Password**: Create a secure password
- **Connection**: `Username-Password-Authentication`
- After creation, go to the **Roles** tab and assign the `Casting Assistant` role

#### User 2: Casting Director
- **Email**: `director@casting-agency.com`
- **Password**: Create a secure password
- **Connection**: `Username-Password-Authentication`
- After creation, go to the **Roles** tab and assign the `Casting Director` role

#### User 3: Executive Producer
- **Email**: `producer@casting-agency.com`
- **Password**: Create a secure password
- **Connection**: `Username-Password-Authentication`
- After creation, go to the **Roles** tab and assign the `Executive Producer` role

### 7. Create an Application for Testing

1. Navigate to **Applications → Applications**
2. Click **Create Application**
3. Fill in the details:
   - **Name**: `Casting Agency Test Client`
   - **Application Type**: Choose **Machine to Machine Applications**
4. Click **Create**
5. Select your API (`Casting Agency API`)
6. Click **Authorize**
7. Note down the following from the **Settings** tab:
   - **Domain** (e.g., `your-casting-agency.auth0.com`)
   - **Client ID**
   - **Client Secret**

### 8. Configure Environment Variables

Update your `.env` file or environment variables:

```bash
# Auth0 Configuration
AUTH0_DOMAIN=your-casting-agency.auth0.com
API_AUDIENCE=casting-agency
ALGORITHMS=RS256
```

For production (Heroku):
```bash
heroku config:set AUTH0_DOMAIN=your-casting-agency.auth0.com
heroku config:set API_AUDIENCE=casting-agency
heroku config:set ALGORITHMS=RS256
```

## Obtaining JWT Tokens for Testing

### Method 1: Using Auth0 Authentication API Explorer

1. Go to your API in Auth0 Dashboard
2. Click on **Test** tab
3. Use the provided `curl` command or test interface
4. Copy the access token

### Method 2: Using cURL (Password Grant)

**Note**: This requires enabling the Password grant type in your application.

```bash
curl --request POST \
  --url https://YOUR_DOMAIN.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{
    "grant_type": "password",
    "username": "assistant@casting-agency.com",
    "password": "USER_PASSWORD",
    "audience": "casting-agency",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
  }'
```

### Method 3: Using Postman

1. Create a new request in Postman
2. Go to the **Authorization** tab
3. Select **OAuth 2.0**
4. Configure:
   - **Grant Type**: `Password Credentials`
   - **Access Token URL**: `https://YOUR_DOMAIN.auth0.com/oauth/token`
   - **Username**: Your test user email
   - **Password**: Your test user password
   - **Client ID**: Your client ID
   - **Client Secret**: Your client secret
   - **Scope**: Leave empty or use specific scopes
   - **Audience**: `casting-agency`
5. Click **Get New Access Token**
6. Use the token in your requests

### Method 4: Python Script

Create a `get_token.py` script:

```python
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_AUDIENCE = os.getenv('API_AUDIENCE')
CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

def get_token(username, password):
    """Get JWT token for a user"""
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'audience': API_AUDIENCE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

# Get tokens for each role
assistant_token = get_token('assistant@casting-agency.com', 'YOUR_PASSWORD')
director_token = get_token('director@casting-agency.com', 'YOUR_PASSWORD')
producer_token = get_token('producer@casting-agency.com', 'YOUR_PASSWORD')

print("Casting Assistant Token:")
print(assistant_token)
print("\nCasting Director Token:")
print(director_token)
print("\nExecutive Producer Token:")
print(producer_token)
```

## Testing the API with Authentication

### Example: Get Movies (Requires `get:movies` permission)

```bash
curl -X GET https://your-app.herokuapp.com/api/movies \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Example: Create Actor (Requires `post:actors` permission)

```bash
curl -X POST https://your-app.herokuapp.com/api/actors \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tom Hanks",
    "age": 67,
    "gender": "Male"
  }'
```

### Example: Delete Movie (Requires `delete:movies` permission)

```bash
curl -X DELETE https://your-app.herokuapp.com/api/movies/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Expected Error Responses

### Missing Authorization Header (401)

```json
{
  "code": "authorization_header_missing",
  "description": "Authorization header is expected."
}
```

### Invalid Token (401)

```json
{
  "code": "token_expired",
  "description": "Token expired."
}
```

### Insufficient Permissions (403)

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

## Testing RBAC Functionality

### Test 1: Casting Assistant
- ✅ Should be able to GET `/api/actors`
- ✅ Should be able to GET `/api/movies`
- ❌ Should NOT be able to POST `/api/actors` (403)
- ❌ Should NOT be able to DELETE `/api/movies` (403)

### Test 2: Casting Director
- ✅ Should be able to GET `/api/actors`
- ✅ Should be able to POST `/api/actors`
- ✅ Should be able to PATCH `/api/movies`
- ✅ Should be able to DELETE `/api/actors`
- ❌ Should NOT be able to POST `/api/movies` (403)
- ❌ Should NOT be able to DELETE `/api/movies` (403)

### Test 3: Executive Producer
- ✅ Should be able to perform ALL operations
- ✅ Should be able to POST `/api/movies`
- ✅ Should be able to DELETE `/api/movies`

## Troubleshooting

### Token is not working
1. Check if the token is expired (JWT tokens expire after 24 hours by default)
2. Verify the `AUTH0_DOMAIN` and `API_AUDIENCE` in your environment variables
3. Ensure RBAC is enabled and permissions are added to the access token
4. Decode the JWT at [jwt.io](https://jwt.io) to verify the permissions are present

### Permissions not in token
1. Go to your API settings in Auth0
2. Ensure "Add Permissions in the Access Token" is enabled
3. Generate a new token

### 401 Unauthorized errors
1. Check if the Authorization header is formatted correctly: `Bearer <token>`
2. Verify the token hasn't expired
3. Ensure the `AUTH0_DOMAIN` matches your tenant domain

### 403 Forbidden errors
1. Verify the user has the correct role assigned
2. Check if the role has the required permissions
3. Generate a fresh token after role/permission changes

## Additional Resources

- [Auth0 RBAC Documentation](https://auth0.com/docs/manage-users/access-control/rbac)
- [Auth0 APIs Documentation](https://auth0.com/docs/apis)
- [Auth0 Python Quickstart](https://auth0.com/docs/quickstart/backend/python)
- [JWT.io - Token Decoder](https://jwt.io)

## Security Best Practices

1. **Never commit tokens or secrets** to version control
2. **Use environment variables** for sensitive configuration
3. **Rotate secrets regularly** in production
4. **Use HTTPS** in production (Heroku provides this automatically)
5. **Set appropriate token expiration times** based on your security requirements
6. **Implement rate limiting** to prevent abuse
7. **Monitor authentication logs** in Auth0 dashboard
8. **Use different Auth0 tenants** for development and production

## Support

For issues with Auth0 configuration:
- Check the [Auth0 Community](https://community.auth0.com/)
- Review [Auth0 Documentation](https://auth0.com/docs)
- Contact Auth0 support if you have a paid plan
