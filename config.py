import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or f'postgresql://'
        f'{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@'
        f'{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}'
    )


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
