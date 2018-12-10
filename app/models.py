from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime
from sqlalchemy import inspect

from app import db


def to_dict(model):
        return {c.key: getattr(model, c.key)
                for c in inspect(model).mapper.column_attrs}

subscribers = db.Table('subscribers',
                     db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('subscribed_id', db.Integer, db.ForeignKey('user.id'))
                    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String())
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    about = db.Column(db.Text, default='Hello World')
    poin = db.Column(db.Integer, default=50)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    subscribed = db.relationship(
        'User', secondary=subscribers,
        primaryjoin=(subscribers.c.subscriber_id == id),
        secondaryjoin=(subscribers.c.subscribed_id==id),
        backref=db.backref('subscribers', lazy='dynamic'), lazy='dynamic'
    )

    def __str__(self):
        return 'Username: {}'.format(self.username)

    def __repr__(self):
        return 'Username: {}'.format(self.username)

    def subscribe(self, user):
        if not self.is_subscribing(user):
            self.subscribed.append(user)
            db.session.commit()

    def unsubscribe(self, user):
        if self.is_subscribing(user):
            self.subscribed.remove(user)
            db.session.commit()

    def is_subscribing(self, target):
        return self.subscribed.filter(
            subscribers.c.subscribed_id == target.id).count() > 0

    def subscribed_post(self):
        return Post.query.join(
            subscribers, (subscribers.c.subscribed_id== Post.user_id)).filter(
                subscribers.c.subscriber_id==self.id, premium=True).order_by(
                    Post.uploaded.desc()
                ).limit(4)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def is_phone_exists(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @staticmethod
    def hash_password(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hash):
        return sha256.verify(password, hash)


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


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
