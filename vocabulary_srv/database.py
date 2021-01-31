from datetime import datetime

import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from vocabulary_srv.dataaccess import IWordCollectionsDao

db: SQLAlchemy = SQLAlchemy()


def get_db_session():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """

    if "db_session" not in g:
        pass
    return None


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

    #db = get_db_session()
    db.drop_all()
    db.create_all()

    # Base.metadata.drop_all(engine)
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


class DbWordCollectionStorage(IWordCollectionsDao):

    def get_item(self, element_id: str) -> object:
        from .models import WordCollections
        return WordCollections\
            .query.filter_by(user_id=element_id).first().wc_object

    def create_item(self, element_id: str, item_to_store: object) -> None:
        from .models import WordCollections
        entry = WordCollections(user_id=element_id,
                                created_at=datetime.now(),
                                last_modified_at=datetime.now(),
                                wc_object=item_to_store,
                                collection_name="",
                                collection_display_name="")
        db.session.add(entry)
        db.session.commit()

    def update_item(self, element_id: str, item_to_store: object) -> None:

        from .models import WordCollections
        entry: WordCollections = WordCollections \
            .query.filter_by(user_id=element_id).first()
        entry.wc_object = item_to_store
        db.session.commit()


class FeedbackStorage:
    @staticmethod
    def insert(name, email, is_subscribe, subject, message):
        from .models import Feedback
        entry = Feedback(name=name,
                         submitted_at = datetime.now(),
                         email=email,
                         is_subscribe=is_subscribe,
                         subject=subject,
                         message=message)
        db.session.add(entry)
        db.session.commit()

    @staticmethod
    def get_count():
        from .models import Feedback
        return db.session.query(Feedback.name).count()
