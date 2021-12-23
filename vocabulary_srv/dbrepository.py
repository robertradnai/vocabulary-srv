from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from vocabulary import WordList, wordlistquiz
from vocabulary.dataaccess import build_word_list_csv, save_word_list_learning_progress_json

from .models import WordListMeta, UserWordListMeta, WordListEntry
from .dbmodels import Base, WordListsTable, Feedback

engine = None
Session = scoped_session(sessionmaker())
# https://nestedsoftware.com/2018/06/11/flask-and-sqlalchemy-without-the-flask-sqlalchemy-extension-3cf8.34704.html


def configure_db(conn_str):
    global engine
    global Session
    engine = create_engine(conn_str, echo=False)
    Session.configure(bind=engine)


def close_session(e=None):
    """If this request connected to the database, close the
    connection.
    """
    # scoped_session will automatically create a new session after the removal if needed
    Session.remove() 


def init_db():
    """Clear existing data and create new tables."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def _build_word_list_entry(entry):

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


class WLRepository:
    @staticmethod
    def create_item(word_list_meta: WordListMeta, csv_str: str, user_id: str, is_addable: bool)\
            -> UserWordListMeta:

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

        Session().add(entry)
        Session().commit()
        return _build_word_list_entry(entry).meta

    @staticmethod
    def get_word_list_entries(user_id, user_word_list_id=None, available_word_list_id=None)\
            -> List[WordListEntry]:

        filters = {"user_id": user_id}
        if user_word_list_id is not None:
            filters["id"] = user_word_list_id
        if available_word_list_id is not None:
            filters["available_word_list_id"] = available_word_list_id

        entries = Session().query(WordListsTable).filter_by(**filters)
        return [_build_word_list_entry(entry) for entry in entries]

    @staticmethod
    def update_learning_progress(user_word_list_id, user_id, word_list: WordList):

        entry = Session() \
            .query(WordListsTable).filter_by(id=user_word_list_id, user_id=user_id).first()

        if entry is None:
            raise LookupError("Word list doesn't exist with the given user id and word list id")

        entry.learning_progress_json = \
            save_word_list_learning_progress_json(word_list.learning_progress_codes)

        Session().commit()


class FeedbackRepository:
    @staticmethod
    def insert(name, email, is_subscribe, subject, message):
        entry = Feedback(name=name,
                            submitted_at=datetime.now(),
                            email=email,
                            is_subscribe=is_subscribe,
                            subject=subject,
                            message=message)
        Session().add(entry)
        Session().commit()
    
    @staticmethod
    def get_count():
        return Session().query(Feedback).count()
