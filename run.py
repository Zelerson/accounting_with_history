from app import create_app
from flask_alembic import Alembic

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)