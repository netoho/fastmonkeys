from app import db
from datetime import datetime
from sqlalchemy_searchable import Searchable
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from app.tags.models import Tag

__author__ = 'netoho'

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class PostQuery(BaseQuery, SearchQueryMixin):
    pass

class Post(db.Model, Searchable):
    query_class = PostQuery
    __searchable_columns__ = ['title', 'body', 'pub_date']
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, tags, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.tags = tags

    def __repr__(self):
        return "<Post('%s', '%s', '%s')>" % (self.title, self.body, self.pub_date)