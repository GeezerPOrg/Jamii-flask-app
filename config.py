import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    parent/base configurations class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or '376ce0a09277bdbbb7479f45a93ed754'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """
    development configurations
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    production configurations
    """
    DEBUG = False

class TestingConfig(Config):
    """
    testing configurations
    """
    TESTING = True
