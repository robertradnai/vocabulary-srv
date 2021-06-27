from .database import db


class WordListsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    available_word_list_id = db.Column(db.Integer, index=True)
    is_addable = db.Column(db.Boolean(), index=True)
    created_at = db.Column(db.DateTime())
    last_modified_at = db.Column(db.DateTime())

    word_list_display_name = db.Column(db.String) #
    description = db.Column(db.String)
    lang1 = db.Column(db.String) #
    lang2 = db.Column(db.String) #
    flashcards_csv = db.Column(db.UnicodeText()) #
    learning_progress_json = db.Column(db.UnicodeText()) #


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submitted_at = db.Column(db.DateTime)
    name = db.Column(db.String())
    email = db.Column(db.String())
    is_subscribe = db.Column(db.Boolean())
    subject = db.Column(db.String())
    message = db.Column(db.String())