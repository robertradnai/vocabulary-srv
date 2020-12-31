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

    def __repr__(self):
        return f"<User id={self.id}, user_id={self.username}, created_at={self.created_at}, last_modified_at={self.last_modified_at}>"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    is_subscribe = db.Column(db.Boolean())
    subject = db.Column(db.String())
    message = db.Column(db.String())