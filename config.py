class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///warehouse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'testkey'