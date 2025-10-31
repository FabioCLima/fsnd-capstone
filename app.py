"""
Full Stack Nanodegree Capstone Project - Casting Agency API
"""
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import (
    setup_db, db,
    Movie, Actor, MovieActor,
    MovieCreate, MovieUpdate, MovieResponse,
    ActorCreate, ActorUpdate, ActorResponse
)
from pydantic import ValidationError


def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Setup database
    setup_db(app)

    # Setup migrations
    migrate = Migrate(app, db)

    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
        )
        return response

    # ========================================================================
    # Routes
    # ========================================================================

    @app.route('/')
    def index():
        """Health check endpoint"""
        return jsonify({
            'success': True,
            'message': 'Casting Agency API is running!',
            'endpoints': {
                'movies': '/api/movies',
                'actors': '/api/actors'
            }
        })

    @app.route('/api/movies', methods=['GET'])
    def get_movies():
        """Get all movies"""
        try:
            movies = Movie.query.order_by(Movie.id).all()
            movies_data = [movie.to_dict() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies_data,
                'total_movies': len(movies_data)
            })
        except Exception as e:
            abort(500)

    @app.route('/api/movies/<int:movie_id>', methods=['GET'])
    def get_movie(movie_id):
        """Get a specific movie by ID"""
        movie = Movie.query.get_or_404(movie_id)

        return jsonify({
            'success': True,
            'movie': movie.to_dict()
        })

    @app.route('/api/movies', methods=['POST'])
    def create_movie():
        """Create a new movie"""
        try:
            # Get request data
            data = request.get_json()

            # Validate with Pydantic
            movie_data = MovieCreate(**data)

            # Create movie
            movie = Movie(
                title=movie_data.title,
                release_date=movie_data.release_date
            )

            db.session.add(movie)
            db.session.commit()

            return jsonify({
                'success': True,
                'movie': movie.to_dict()
            }), 201

        except ValidationError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.errors()
            }), 422
        except Exception as e:
            db.session.rollback()
            abort(500)

    @app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        """Update a movie"""
        try:
            movie = Movie.query.get_or_404(movie_id)
            data = request.get_json()

            # Validate with Pydantic
            movie_update = MovieUpdate(**data)

            # Update only provided fields
            update_data = movie_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(movie, key, value)

            db.session.commit()

            return jsonify({
                'success': True,
                'movie': movie.to_dict()
            })

        except ValidationError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.errors()
            }), 422
        except Exception as e:
            db.session.rollback()
            abort(500)

    @app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        """Delete a movie"""
        try:
            movie = Movie.query.get_or_404(movie_id)

            db.session.delete(movie)
            db.session.commit()

            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        except Exception as e:
            db.session.rollback()
            abort(500)

    @app.route('/api/actors', methods=['GET'])
    def get_actors():
        """Get all actors"""
        try:
            actors = Actor.query.order_by(Actor.id).all()
            actors_data = [actor.to_dict() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actors_data,
                'total_actors': len(actors_data)
            })
        except Exception as e:
            abort(500)

    @app.route('/api/actors/<int:actor_id>', methods=['GET'])
    def get_actor(actor_id):
        """Get a specific actor by ID"""
        actor = Actor.query.get_or_404(actor_id)

        return jsonify({
            'success': True,
            'actor': actor.to_dict()
        })

    @app.route('/api/actors', methods=['POST'])
    def create_actor():
        """Create a new actor"""
        try:
            # Get request data
            data = request.get_json()

            # Validate with Pydantic
            actor_data = ActorCreate(**data)

            # Create actor
            actor = Actor(
                name=actor_data.name,
                age=actor_data.age,
                gender=actor_data.gender
            )

            db.session.add(actor)
            db.session.commit()

            return jsonify({
                'success': True,
                'actor': actor.to_dict()
            }), 201

        except ValidationError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.errors()
            }), 422
        except Exception as e:
            db.session.rollback()
            abort(500)

    @app.route('/api/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        """Update an actor"""
        try:
            actor = Actor.query.get_or_404(actor_id)
            data = request.get_json()

            # Validate with Pydantic
            actor_update = ActorUpdate(**data)

            # Update only provided fields
            update_data = actor_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(actor, key, value)

            db.session.commit()

            return jsonify({
                'success': True,
                'actor': actor.to_dict()
            })

        except ValidationError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.errors()
            }), 422
        except Exception as e:
            db.session.rollback()
            abort(500)

    @app.route('/api/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        """Delete an actor"""
        try:
            actor = Actor.query.get_or_404(actor_id)

            db.session.delete(actor)
            db.session.commit()

            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        except Exception as e:
            db.session.rollback()
            abort(500)

    # ========================================================================
    # Error Handlers
    # ========================================================================

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app


# Create the app instance
APP = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    APP.run(host='0.0.0.0', port=port, debug=True)
