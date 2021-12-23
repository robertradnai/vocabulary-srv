from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UnicodeText

Base = declarative_base()

class WordListsTable(Base):
    __tablename__ = 'word_lists_table'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    available_word_list_id = Column(Integer, index=True)
    is_addable = Column(Boolean, index=True)
    created_at = Column(DateTime)
    last_modified_at = Column(DateTime)

    word_list_display_name = Column(String) #
    description = Column(String)
    lang1 = Column(String) #
    lang2 = Column(String) #
    flashcards_csv = Column(UnicodeText) #
    learning_progress_json = Column(UnicodeText) #


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    submitted_at = Column(DateTime)
    name = Column(String)
    email = Column(String)
    is_subscribe = Column(Boolean)
    subject = Column(String)
    message = Column(String)