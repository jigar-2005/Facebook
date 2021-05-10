from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32767), nullable=False)
    lastname = db.Column(db.String(32767), nullable=False)
    email = db.Column(db.String(32767), unique=True, nullable=False)
    password = db.Column(db.String(32767), nullable=False)
    date_of_birth = db.Column(db.String(32767), nullable=False)
    gender = db.Column(db.String(32767), nullable=False)
    profile_image = db.Column(
        db.String(32767), nullable=False, default='user_profile_img.jpg')
    cover_image = db.Column(
        db.String(32767), nullable=False, default='user_cover_img.jpg')
    register_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posts = db.relationship('Post', backref='author', lazy=True)


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_sender = db.Column(db.Integer, nullable=False)
    sentto = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), nullable=False, default='0')
    request_sent_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    post_description = db.Column(db.String(180), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_image = db.Column(db.String(32767), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reaction = db.Column(db.String(1), nullable=False, default='1')
    reaction_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(32767), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
