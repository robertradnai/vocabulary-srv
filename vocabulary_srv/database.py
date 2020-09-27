from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import click
from flask import g
from flask.cli import with_appcontext

engine = create_engine('sqlite:////tmp/test.db',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()





def get_db_session():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """

    if "db_session" not in g:
        Base.query = db_session.query_property()
        Base.metadata.create_all(bind=engine)
        g.db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=engine))
    return db_session


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db_session", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models


    #db = get_db_session()
    Base.metadata.drop_all(engine)
    #with current_app.open_resource("schema.sql") as f:
        #db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)