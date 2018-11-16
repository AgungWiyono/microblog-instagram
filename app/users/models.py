from passlib.hash import pbkdf2_sha256 as sha256

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __str__(self):
        return '{} : {}'.format(self.username, self.password)

    def __repr__(self):
        return '{} : {}'.format(self.username, self.password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def hash_password(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hash):
        return sha256.verify(password, hash)

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