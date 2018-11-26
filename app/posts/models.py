from datetime import datetime

from sqlalchemy import inspect

from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String())
    uploaded = db.Column(db.DateTime)
    image= db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    premium = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Integer, default=-7.797068)
    longitude= db.Column(db.Integer, default=110.370529)

    def __str__(self):
        return 'Post by :{}'.format(self.author.username)

    def toDict(self):
        return {c.key: getattr(self. c.key)
                for c in inspect(self).mapper.column_attrs}
