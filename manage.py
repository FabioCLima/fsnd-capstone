"""
Optional management script for database tasks.

Usage examples:
  python manage.py create_db
  python manage.py drop_db
  python manage.py seed_db
"""
import click

from app import APP
from models import db, Actor, Movie


@click.group()
def cli():
    pass


@cli.command("create_db")
def create_db():
    """Create all database tables."""
    with APP.app_context():
        db.create_all()
        click.echo("Database tables created.")


@cli.command("drop_db")
def drop_db():
    """Drop all database tables (DANGEROUS)."""
    with APP.app_context():
        db.drop_all()
        click.echo("Database tables dropped.")


@cli.command("seed_db")
def seed_db():
    """Insert a small seed dataset for local testing."""
    with APP.app_context():
        if not Actor.query.first() and not Movie.query.first():
            actor = Actor(name="Sample Actor", age=30, gender="Other")
            movie = Movie(title="Sample Movie", release_date=db.func.now())
            db.session.add_all([actor, movie])
            db.session.commit()
            click.echo("Seed data inserted.")
        else:
            click.echo("Database already has data; skipping seed.")


if __name__ == "__main__":
    cli()


