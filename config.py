class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:pa$$w0rd@integradoradb.c0i2k8ilqa3a.us-east-1.rds.amazonaws.com/integradoradb'
#    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/parkingmap'
    SQLALCHEMY_TRACK_MODIFICATIONS = False