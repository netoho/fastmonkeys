from app import db
from datetime import datetime
from sqlalchemy_searchable import Searchable
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin

__author__ = 'netoho'

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.String(30))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, body, pub_date=None):
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow().strftime('%d %b %Y')
        self.pub_date = pub_date

    def __repr__(self):
        return "<Post('%s', '%s')>" % (self.body, self.pub_date)