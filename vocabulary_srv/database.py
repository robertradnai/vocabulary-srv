from datetime import datetime
from typing import Optional, List

import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from vocabulary import WordList, wordlistquiz
from vocabulary.dataaccess import build_word_list_csv, save_word_list_learning_progress_json

from vocabulary_srv.dataaccess import IWordCollectionsDao
from vocabulary_srv.models import WordListMeta, UserWordListMeta, WordListEntry

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


def build_word_list_entry(entry):

    word_list = build_word_list_csv(lang1=entry.lang1,
                                    lang2=entry.lang2,
                                    flashcards_csv_str=entry.flashcards_csv,
                                    learning_progress_json_str=entry.learning_progress_json)

    meta = UserWordListMeta(
        available_word_list_id=entry.available_word_list_id,
        word_list_display_name=entry.word_list_display_name,
        description=entry.description,
        lang1=entry.lang1,
        lang2=entry.lang2,
        is_added_to_user_word_lists=True,
        user_word_list_id=entry.id,
        csv_filename=None,
        progress=wordlistquiz.get_learning_progress(word_list),
        created_at=entry.created_at,
        last_opened_at=entry.last_modified_at)

    return WordListEntry(word_list=word_list, meta=meta)


class DbWordListStorage:
    def __init__(self):
        from .dbmodels import WordListsTable
        self.word_lists_table = WordListsTable

    def create_item(self, word_list_meta: WordListMeta, csv_str: str, user_id: str, is_addable: bool)\
            -> UserWordListMeta:

        entry = self.word_lists_table(
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
        return build_word_list_entry(entry).meta

    def get_word_list_entries(self, user_id, user_word_list_id=None, available_word_list_id=None)\
            -> List[WordListEntry]:

        filters = {"user_id": user_id}
        if user_word_list_id is not None:
            filters["id"] = user_word_list_id
        if available_word_list_id is not None:
            filters["available_word_list_id"] = available_word_list_id

        entries = self.word_lists_table .query.filter_by(**filters)
        return [build_word_list_entry(entry) for entry in entries]

    def update_learning_progress(self, user_word_list_id, user_id, word_list: WordList):

        entry = self.word_lists_table \
            .query.filter_by(id=user_word_list_id, user_id=user_id).first()

        if entry is None:
            raise LookupError("Word list doesn't exist with the given user id and word list id")

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
