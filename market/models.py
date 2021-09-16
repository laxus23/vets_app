from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Visit(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(length=24), nullable=False, unique=True)
    time = db.Column(db.String(length=14), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Visit {self.name}'


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=2048), nullable=False, unique=True)
    city = db.Column(db.String(length=24), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = db.relationship('Answer', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'Item {self.name}'


class Answer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=2048), nullable=False, unique=True)
    city = db.Column(db.String(length=24), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('item.id'))

    def __repr__(self):
        return f'Answer {self.name}'
