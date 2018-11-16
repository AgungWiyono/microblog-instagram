from datetime import datetime

from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String())
    uploaded = db.Column(db.DateTime)
    large = db.Column(db.String())
    thumbnail = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return 'Post by :{}'.format(self.author.username)
