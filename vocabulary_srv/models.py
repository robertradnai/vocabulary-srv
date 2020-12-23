from .database import db


class WordCollections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.String())
    last_modified_at = db.Column(db.DateTime())
    wc_object = db.Column(db.PickleType())
    collection_name = db.Column(db.String())
    collection_display_name = db.Column(db.String())

    def __repr__(self):
        return f"<User id={self.id}, user_id={self.username}, created_at={self.created_at}, last_modified_at={self.last_modified_at}>"
