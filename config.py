class Config():
    SECRET_KEY = 'hfjdisoolfjd=-20394opz;'
    QUOTE_API = 'http://quotes.stormconsultancy.co.uk/random.json'

    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    pass  


class TestConfig(Config):
    pass 

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig

}
