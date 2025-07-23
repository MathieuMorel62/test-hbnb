import os


class Config:
    """
    Configuration de l'application.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Configuration de développement.
    """
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
