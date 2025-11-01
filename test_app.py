"""
Unit tests for the Casting Agency API
"""
import os
import unittest
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """Test case for the Casting Agency API"""

    def setUp(self):
        """Setup test fixtures before each test"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get(
            'DATABASE_URL_TEST',
            'postgresql://localhost:5432/capstone_test'
        )

        # Fix Heroku postgres:// to postgresql://
        if self.database_path.startswith("postgres://"):
            self.database_path = self.database_path.replace(
                "postgres://", "postgresql://", 1
            )

        setup_db(self.app, self.database_path)

        # Sample test data
        self.new_actor = {
            "name": "Tom Hanks",
            "age": 67,
            "gender": "Male"
        }

        self.new_movie = {
            "title": "Forrest Gump",
            "release_date": "1994-07-06T00:00:00"
        }

        # JWT tokens for different roles
        # These should be set as environment variables
        # In production tests, get these from Auth0
        self.assistant_token = os.environ.get('ASSISTANT_TOKEN', '')
        self.director_token = os.environ.get('DIRECTOR_TOKEN', '')
        self.producer_token = os.environ.get('PRODUCER_TOKEN', '')

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()
            # Add sample data for testing
            self._seed_data()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _seed_data(self):
        """Add sample data to the test database"""
        actor = Actor(name="Sample Actor", age=30, gender="Male")
        movie = Movie(title="Sample Movie", release_date=datetime(2020, 1, 1))

        db.session.add(actor)
        db.session.add(movie)
        db.session.commit()

    def _get_auth_header(self, token):
        """Helper method to create authorization header"""
        return {'Authorization': f'Bearer {token}'}

    # =========================================================================
    # Tests for Public Endpoints (No Authentication Required)
    # =========================================================================

    def test_001_health_check(self):
        """Test the health check endpoint"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('message', data)

    # =========================================================================
    # Tests for GET /api/actors
    # =========================================================================

    def test_002_get_actors_without_token(self):
        """Test GET actors without authentication - should fail"""
        res = self.client().get('/api/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertIn('code', data)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_003_get_actors_with_assistant_token(self):
        """Test GET actors with assistant token - should succeed"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().get(
            '/api/actors',
            headers=self._get_auth_header(self.assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('actors', data)
        self.assertIsInstance(data['actors'], list)

    def test_004_get_actors_with_director_token(self):
        """Test GET actors with director token - should succeed"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().get(
            '/api/actors',
            headers=self._get_auth_header(self.director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('actors', data)

    def test_005_get_actors_with_producer_token(self):
        """Test GET actors with producer token - should succeed"""
        if not self.producer_token:
            self.skipTest("PRODUCER_TOKEN not set")

        res = self.client().get(
            '/api/actors',
            headers=self._get_auth_header(self.producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('actors', data)

    # =========================================================================
    # Tests for GET /api/movies
    # =========================================================================

    def test_006_get_movies_without_token(self):
        """Test GET movies without authentication - should fail"""
        res = self.client().get('/api/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertIn('code', data)

    def test_007_get_movies_with_assistant_token(self):
        """Test GET movies with assistant token - should succeed"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().get(
            '/api/movies',
            headers=self._get_auth_header(self.assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('movies', data)

    # =========================================================================
    # Tests for POST /api/actors
    # =========================================================================

    def test_008_create_actor_without_token(self):
        """Test POST actor without authentication - should fail"""
        res = self.client().post(
            '/api/actors',
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_009_create_actor_with_assistant_token(self):
        """Test POST actor with assistant token - should fail (no permission)"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().post(
            '/api/actors',
            headers=self._get_auth_header(self.assistant_token),
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_010_create_actor_with_director_token(self):
        """Test POST actor with director token - should succeed"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().post(
            '/api/actors',
            headers=self._get_auth_header(self.director_token),
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertIn('actor', data)

    def test_011_create_actor_with_producer_token(self):
        """Test POST actor with producer token - should succeed"""
        if not self.producer_token:
            self.skipTest("PRODUCER_TOKEN not set")

        res = self.client().post(
            '/api/actors',
            headers=self._get_auth_header(self.producer_token),
            json={"name": "Brad Pitt", "age": 60, "gender": "Male"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_012_create_actor_with_invalid_data(self):
        """Test POST actor with invalid data - should fail validation"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        invalid_actor = {
            "name": "Test Actor",
            "age": "invalid",  # Should be integer
            "gender": "Male"
        }

        res = self.client().post(
            '/api/actors',
            headers=self._get_auth_header(self.director_token),
            json=invalid_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # =========================================================================
    # Tests for POST /api/movies
    # =========================================================================

    def test_013_create_movie_with_assistant_token(self):
        """Test POST movie with assistant token - should fail (no permission)"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().post(
            '/api/movies',
            headers=self._get_auth_header(self.assistant_token),
            json=self.new_movie
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_014_create_movie_with_director_token(self):
        """Test POST movie with director token - should fail (no permission)"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().post(
            '/api/movies',
            headers=self._get_auth_header(self.director_token),
            json=self.new_movie
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_015_create_movie_with_producer_token(self):
        """Test POST movie with producer token - should succeed"""
        if not self.producer_token:
            self.skipTest("PRODUCER_TOKEN not set")

        res = self.client().post(
            '/api/movies',
            headers=self._get_auth_header(self.producer_token),
            json=self.new_movie
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertIn('movie', data)

    # =========================================================================
    # Tests for PATCH /api/actors/<id>
    # =========================================================================

    def test_016_update_actor_without_token(self):
        """Test PATCH actor without authentication - should fail"""
        res = self.client().patch(
            '/api/actors/1',
            json={"age": 68}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_017_update_actor_with_assistant_token(self):
        """Test PATCH actor with assistant token - should fail (no permission)"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().patch(
            '/api/actors/1',
            headers=self._get_auth_header(self.assistant_token),
            json={"age": 68}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_018_update_actor_with_director_token(self):
        """Test PATCH actor with director token - should succeed"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().patch(
            '/api/actors/1',
            headers=self._get_auth_header(self.director_token),
            json={"age": 31}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_019_update_nonexistent_actor(self):
        """Test PATCH nonexistent actor - should return 404"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().patch(
            '/api/actors/9999',
            headers=self._get_auth_header(self.director_token),
            json={"age": 31}
        )

        self.assertEqual(res.status_code, 404)

    # =========================================================================
    # Tests for PATCH /api/movies/<id>
    # =========================================================================

    def test_020_update_movie_with_assistant_token(self):
        """Test PATCH movie with assistant token - should fail (no permission)"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().patch(
            '/api/movies/1',
            headers=self._get_auth_header(self.assistant_token),
            json={"title": "Updated Title"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_021_update_movie_with_director_token(self):
        """Test PATCH movie with director token - should succeed"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().patch(
            '/api/movies/1',
            headers=self._get_auth_header(self.director_token),
            json={"title": "Updated Movie Title"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_022_update_movie_with_producer_token(self):
        """Test PATCH movie with producer token - should succeed"""
        if not self.producer_token:
            self.skipTest("PRODUCER_TOKEN not set")

        res = self.client().patch(
            '/api/movies/1',
            headers=self._get_auth_header(self.producer_token),
            json={"title": "Producer Updated Title"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # =========================================================================
    # Tests for DELETE /api/actors/<id>
    # =========================================================================

    def test_023_delete_actor_without_token(self):
        """Test DELETE actor without authentication - should fail"""
        res = self.client().delete('/api/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_024_delete_actor_with_assistant_token(self):
        """Test DELETE actor with assistant token - should fail (no permission)"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().delete(
            '/api/actors/1',
            headers=self._get_auth_header(self.assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_025_delete_actor_with_director_token(self):
        """Test DELETE actor with director token - should succeed"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        # Create an actor first
        create_res = self.client().post(
            '/api/actors',
            headers=self._get_auth_header(self.director_token),
            json={"name": "To Delete", "age": 40, "gender": "Male"}
        )
        actor_id = json.loads(create_res.data)['actor']['id']

        # Now delete it
        res = self.client().delete(
            f'/api/actors/{actor_id}',
            headers=self._get_auth_header(self.director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_026_delete_nonexistent_actor(self):
        """Test DELETE nonexistent actor - should return 404"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().delete(
            '/api/actors/9999',
            headers=self._get_auth_header(self.director_token)
        )

        self.assertEqual(res.status_code, 404)

    # =========================================================================
    # Tests for DELETE /api/movies/<id>
    # =========================================================================

    def test_027_delete_movie_with_assistant_token(self):
        """Test DELETE movie with assistant token - should fail (no permission)"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().delete(
            '/api/movies/1',
            headers=self._get_auth_header(self.assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_028_delete_movie_with_director_token(self):
        """Test DELETE movie with director token - should fail (no permission)"""
        if not self.director_token:
            self.skipTest("DIRECTOR_TOKEN not set")

        res = self.client().delete(
            '/api/movies/1',
            headers=self._get_auth_header(self.director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_029_delete_movie_with_producer_token(self):
        """Test DELETE movie with producer token - should succeed"""
        if not self.producer_token:
            self.skipTest("PRODUCER_TOKEN not set")

        # Create a movie first
        create_res = self.client().post(
            '/api/movies',
            headers=self._get_auth_header(self.producer_token),
            json={"title": "To Delete", "release_date": "2020-01-01T00:00:00"}
        )
        movie_id = json.loads(create_res.data)['movie']['id']

        # Now delete it
        res = self.client().delete(
            f'/api/movies/{movie_id}',
            headers=self._get_auth_header(self.producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # =========================================================================
    # Tests for GET /api/actors/<id>
    # =========================================================================

    def test_030_get_single_actor(self):
        """Test GET single actor by ID - should succeed"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().get(
            '/api/actors/1',
            headers=self._get_auth_header(self.assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('actor', data)

    def test_031_get_nonexistent_actor(self):
        """Test GET nonexistent actor - should return 404"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().get(
            '/api/actors/9999',
            headers=self._get_auth_header(self.assistant_token)
        )

        self.assertEqual(res.status_code, 404)

    # =========================================================================
    # Tests for GET /api/movies/<id>
    # =========================================================================

    def test_032_get_single_movie(self):
        """Test GET single movie by ID - should succeed"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().get(
            '/api/movies/1',
            headers=self._get_auth_header(self.assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIn('movie', data)

    def test_033_get_nonexistent_movie(self):
        """Test GET nonexistent movie - should return 404"""
        if not self.assistant_token:
            self.skipTest("ASSISTANT_TOKEN not set")

        res = self.client().get(
            '/api/movies/9999',
            headers=self._get_auth_header(self.assistant_token)
        )

        self.assertEqual(res.status_code, 404)

    # =========================================================================
    # Tests for Invalid Token
    # =========================================================================

    def test_034_invalid_token(self):
        """Test request with invalid token - should fail"""
        res = self.client().get(
            '/api/actors',
            headers={'Authorization': 'Bearer invalid_token_string'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertIn('code', data)

    # =========================================================================
    # Tests for Malformed Authorization Header
    # =========================================================================

    def test_035_malformed_auth_header(self):
        """Test request with malformed authorization header - should fail"""
        res = self.client().get(
            '/api/actors',
            headers={'Authorization': 'InvalidFormat token'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')


# Run the tests
if __name__ == "__main__":
    unittest.main()
