"""
Database models and schemas using SQLAlchemy and Pydantic
"""
import os
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Initialize SQLAlchemy
db = SQLAlchemy()

# Database URI configuration
database_path = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/capstone')

# Fix for Heroku postgres:// to postgresql://
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)


def setup_db(app, database_path=database_path):
    """
    Binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


# ============================================================================
# SQLAlchemy Models
# ============================================================================

class Movie(db.Model):
    """Movie SQLAlchemy Model"""
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    release_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    actors: Mapped[List["MovieActor"]] = relationship(
        "MovieActor",
        back_populates="movie",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Movie {self.id}: {self.title}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class Actor(db.Model):
    """Actor SQLAlchemy Model"""
    __tablename__ = 'actors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    movies: Mapped[List["MovieActor"]] = relationship(
        "MovieActor",
        back_populates="actor",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Actor {self.id}: {self.name}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat()
        }


class MovieActor(db.Model):
    """Association table for Movies and Actors"""
    __tablename__ = 'movie_actors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(
        Integer,
        db.ForeignKey('movies.id'),
        nullable=False
    )
    actor_id: Mapped[int] = mapped_column(
        Integer,
        db.ForeignKey('actors.id'),
        nullable=False
    )

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="actors")
    actor: Mapped["Actor"] = relationship("Actor", back_populates="movies")

    def __repr__(self):
        return f'<MovieActor movie_id={self.movie_id} actor_id={self.actor_id}>'


# ============================================================================
# Pydantic Schemas for Validation and Serialization
# ============================================================================

class ActorBase(BaseModel):
    """Base Actor Schema"""
    name: str = Field(..., min_length=1, max_length=120)
    age: int = Field(..., gt=0, lt=150)
    gender: str = Field(..., min_length=1, max_length=20)

    model_config = ConfigDict(from_attributes=True)


class ActorCreate(ActorBase):
    """Schema for creating an Actor"""
    pass


class ActorUpdate(BaseModel):
    """Schema for updating an Actor (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    age: Optional[int] = Field(None, gt=0, lt=150)
    gender: Optional[str] = Field(None, min_length=1, max_length=20)

    model_config = ConfigDict(from_attributes=True)


class ActorResponse(ActorBase):
    """Schema for Actor response"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieBase(BaseModel):
    """Base Movie Schema"""
    title: str = Field(..., min_length=1, max_length=120)
    release_date: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieCreate(MovieBase):
    """Schema for creating a Movie"""
    pass


class MovieUpdate(BaseModel):
    """Schema for updating a Movie (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    release_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MovieResponse(MovieBase):
    """Schema for Movie response"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieWithActors(MovieResponse):
    """Schema for Movie with actors"""
    actors: List[ActorResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ActorWithMovies(ActorResponse):
    """Schema for Actor with movies"""
    movies: List[MovieResponse] = []

    model_config = ConfigDict(from_attributes=True)
