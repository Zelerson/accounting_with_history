from flask import Flask
from config import Config
from .models import db, Balance
from .routes import warehouse_bp
from flask_alembic import Alembic

alembic = Alembic()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    alembic.init_app(app)

    app.register_blueprint(warehouse_bp)

    with app.app_context():
        db.create_all()
        initial_balance = Balance.query.first()
        if not initial_balance:
            initial_balance = Balance(balance=0)
            db.session.add(initial_balance)
            db.session.commit()

    return app
