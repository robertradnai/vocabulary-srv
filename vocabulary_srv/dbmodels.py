from .database import db


class WordCollections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # The unique constraint stays until login and collection management is implemented
    user_id = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.String())
    last_modified_at = db.Column(db.DateTime())
    wc_object = db.Column(db.PickleType())
    collection_name = db.Column(db.String())
    collection_display_name = db.Column(db.String())
    available_word_list_id = db.Column(db.Integer)


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