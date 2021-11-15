import os ,re

class Config():
    SECRET_KEY = 'hfjdisoolfjd=-20394opz;'
    QUOTE_API = 'http://quotes.stormconsultancy.co.uk/random.json'
    UPLOADED_PHOTOS_DEST ='app/static/images'

    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI .startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI  = SQLALCHEMY_DATABASE_URI .replace("postgres://", "postgresql://", 1)



class TestConfig(Config):
    pass 

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:czar@localhost/blogs'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig

}
