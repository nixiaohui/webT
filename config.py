import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/blog"
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = 200
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/blog"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
}

if __name__ == '__main__':
    config_name = 'development'
    print(config.get(config_name, 'default'))