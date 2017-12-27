"""rmon.config
"""

import os
class DevConfig:
    """DevConfig
    """

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True

class ProductConfig(DevConfig):
    """ProductConfig
    """
    DEBUG = False
    path = os.path.join(os.getwd(), 'rmon.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path
