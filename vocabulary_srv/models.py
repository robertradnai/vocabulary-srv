from .database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

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
 