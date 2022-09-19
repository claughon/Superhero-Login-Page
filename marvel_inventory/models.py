from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

import uuid

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    username = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    superhero = db.relationship('Superhero', backref = 'owner', lazy = True)


    def __init__(self, email, username = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(6)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.username} has been added to the database!"


class Superhero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(600), nullable = True)
    comics_appeared_in = db.Column(db.Integer, nullable = True)
    super_power = db.Column(db.String(200), nullable = True)
    date_established = db.Column(db.Integer, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, date_established, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_established = date_established
        self.user_token = user_token

    def __repr__(self):
        return f"The following superhero has been added: {self.name}"

    def set_id(self):
        return secrets.token_urlsafe()

class SuperheroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power', 'date_established']

hero_schema = SuperheroSchema()
heros_schema = SuperheroSchema(many = True)