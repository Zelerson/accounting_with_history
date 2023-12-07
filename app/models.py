from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Balance(db.Model):
    __tablename__ = 'balance'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(255), nullable=False)
