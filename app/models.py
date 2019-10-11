from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    samples = db.relationship('Sample', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        #return '<User {'.format(self.email)
        return '< User '+str(self.username)+' '+self.email+'>'


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    composition = db.Column(db.String(100), default='', index=True)
    fab_method = db.Column(db.String(100), default='', index=True)
    fab_date = db.Column(db.String(10), default='', index=True)
    notes = db.Column(db.String(200), default='')
    experiments = db.Column(db.PickleType(), default={}, index=True)
    ispublic = db.Column(db.Boolean(), default=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Sample '+self.name+'>'

    
