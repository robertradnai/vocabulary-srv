from datetime import datetime
from typing import Optional

import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from vocabulary import WordList
from vocabulary.dataaccess import build_word_list, save_word_list_learning_progress_json

from vocabulary_srv.dataaccess import IWordCollectionsDao
from vocabulary_srv.models import WordListMeta


db: SQLAlchemy = SQLAlchemy()


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

    db.drop_all()
    db.create_all()


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

    def get_item(self, element_id: int) -> object:
        from .dbmodels import WordCollections
        row = WordCollections \
            .query.filter_by(id=element_id).first()
        return row.wc_object, row.user_id

    def create_item(self, element_id: int, item_to_store: object,
                    available_word_list_id: int) -> int:
        from .dbmodels import WordCollections
        entry = WordCollections(user_id=element_id,
                                created_at=datetime.now(),
                                last_modified_at=datetime.now(),
                                wc_object=item_to_store,
                                collection_name="",
                                collection_display_name="",
                                available_word_list_id=available_word_list_id)
        db.session.add(entry)
        db.session.commit()
        return entry.id

    def update_item(self, element_id: int, item_to_store: object) -> None:

        from .dbmodels import WordCollections
        entry: WordCollections = WordCollections \
            .query.filter_by(id=element_id).first()
        entry.wc_object = item_to_store
        db.session.commit()

    def get_already_existing_user_word_list_id(self, user_id, available_word_list_id) \
            -> Optional[int]:
        from .dbmodels import WordCollections
        entry: WordCollections = WordCollections \
            .query.filter_by(user_id=user_id,
                             available_word_list_id=available_word_list_id).first()
        if entry is None:
            return None
        else:
            return entry.user_word_list_id


class DbWordListStorage:

    def create_item(self, word_list_meta: WordListMeta, csv_str: str, user_id: str, is_addable: bool) -> int:
        from .dbmodels import WordListsTable

        entry = WordListsTable(
            is_addable=is_addable,
            available_word_list_id=word_list_meta.available_word_list_id,
            word_list_display_name=word_list_meta.word_list_display_name,
            description=word_list_meta.description,
            lang1=word_list_meta.lang1,
            lang2=word_list_meta.lang2,
            user_id=user_id,
            flashcards_csv=csv_str,
            learning_progress_json=None
        )

        db.session.add(entry)
        db.session.commit()
        return entry.id

    def get_word_list(self, user_word_list_id, user_id) -> WordList:
        from .dbmodels import WordListsTable
        entry = WordListsTable \
            .query.filter_by(id=user_word_list_id, user_id=user_id).first()

        word_list = build_word_list(lang1=entry.lang1,
                                    lang2=entry.lang2,
                                    flashcards_csv_str=entry.flashcards_csv)

        return word_list

    def update_learning_progress(self, user_word_list_id, user_id, word_list: WordList):
        from .dbmodels import WordListsTable
        entry = WordListsTable \
            .query.filter_by(id=user_word_list_id, user_id=user_id).first()

        entry.learning_progress_json = \
            save_word_list_learning_progress_json(word_list.learning_progress_codes)

        db.session.commit()


class FeedbackStorage:
    @staticmethod
    def insert(name, email, is_subscribe, subject, message):
        from .dbmodels import Feedback
        entry = Feedback(name=name,
                         submitted_at=datetime.now(),
                         email=email,
                         is_subscribe=is_subscribe,
                         subject=subject,
                         message=message)
        db.session.add(entry)
        db.session.commit()

    @staticmethod
    def get_count():
        from .dbmodels import Feedback
        return db.session.query(Feedback.name).count()
