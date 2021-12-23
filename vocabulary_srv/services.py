'''Every (singleton) service should be declared here.'''


from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from flask import g, current_app
from flask.cli import with_appcontext

import click

from .dbrepository import DbWordListStorage, FeedbackStorage
from .dbmodels import Base

# https://nestedsoftware.com/2018/06/11/flask-and-sqlalchemy-without-the-flask-sqlalchemy-extension-3cf8.34704.html
engine = None
Session = scoped_session(sessionmaker())


def get_word_lists_dao() -> DbWordListStorage:
    if "word_lists_dao" not in g:
        g.word_lists_dao = DbWordListStorage(get_db_session())
    return g.word_lists_dao


def get_feedback_storage() -> FeedbackStorage:
    if "feedback_storage" not in g:
        g.feedback_storage = FeedbackStorage(get_db_session())
    return g.feedback_storage


def get_engine():
    # Lazy loading for the engine
    # This will be a singleton object throughout the whole life of the app
    # App context occasionally gets destroyed and then the in-memory sqlite db is recreated
    # That's why I used global variables
    global engine
    if engine is None:
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
        Session.configure(bind=engine)
    return engine


def get_db_session():
    get_engine()
    return Session # Session is a class factory, Session() is a class


def close_session(e=None):
    """If this request connected to the database, close the
    connection.
    """
    Session.remove() 
    # scoped_session will automatically create 
    # a new session after the removal if needed


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_session)
    app.cli.add_command(init_db_command)


def init_db():
    """Clear existing data and create new tables."""

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.drop_all(get_engine())
    Base.metadata.create_all(get_engine())


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


