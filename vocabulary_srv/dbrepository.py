from datetime import datetime
from typing import Optional, List

from vocabulary import WordList, wordlistquiz
from vocabulary.dataaccess import build_word_list_csv, save_word_list_learning_progress_json

from vocabulary_srv.models import WordListMeta, UserWordListMeta, WordListEntry


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
    def __init__(self, session):
        from .dbmodels import WordListsTable
        self.word_lists_table = WordListsTable
        self._session = session

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

        self._session.add(entry)
        self._session.commit()
        return build_word_list_entry(entry).meta

    def get_word_list_entries(self, user_id, user_word_list_id=None, available_word_list_id=None)\
            -> List[WordListEntry]:

        filters = {"user_id": user_id}
        if user_word_list_id is not None:
            filters["id"] = user_word_list_id
        if available_word_list_id is not None:
            filters["available_word_list_id"] = available_word_list_id

        entries = self._session.query(self.word_lists_table).filter_by(**filters)
        return [build_word_list_entry(entry) for entry in entries]

    def update_learning_progress(self, user_word_list_id, user_id, word_list: WordList):

        entry = self._session \
            .query(self.word_lists_table).filter_by(id=user_word_list_id, user_id=user_id).first()

        if entry is None:
            raise LookupError("Word list doesn't exist with the given user id and word list id")

        entry.learning_progress_json = \
            save_word_list_learning_progress_json(word_list.learning_progress_codes)

        self._session.commit()


class FeedbackStorage:

    def __init__(self, session):
        self._session = session
        from .dbmodels import Feedback
        self._feedback_table = Feedback

    def insert(self, name, email, is_subscribe, subject, message):
        entry = self._feedback_table(name=name,
                         submitted_at=datetime.now(),
                         email=email,
                         is_subscribe=is_subscribe,
                         subject=subject,
                         message=message)
        self._session.add(entry)
        self._session.commit()

    def get_count(self):
        return self._session.query(self._feedback_table.name).count()
